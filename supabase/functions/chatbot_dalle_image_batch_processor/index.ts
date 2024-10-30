import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import { createClient } from "https://cdn.skypack.dev/@supabase/supabase-js"

const LOG_PREFIX = "[CHATBOT][IMAGE_BATCH_PROCESSOR]";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_KEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const BUCKET_NAME = 'ChatBotFiles';
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

console.log(`${LOG_PREFIX} Starting the chatbot_dalle_image_batch_processor function.`);

// async function updateMovedStatus(): Promise<any> {
//     const { data, error } = await supabase.rpc('update_moved_status_default_image');
//     if (error) {
//         throw new Error(`Failed to call update_moved_status_default_image: ${error.message}`);
//     }
//     console.log(`${LOG_PREFIX} update_moved_status_default_image result:`, data);
//     return data;
// }

async function fetchItems(): Promise<any[]> {
    const { data, error } = await supabase
        .from('data')
        .select('*')
        .eq('moved', false);
    if (error) {
        throw new Error(`Failed to query items: ${error.message}`);
    }
    return data;
}

function extractFileName(url: string): string | null {
    const pattern = /\/([^\/]+)\.[a-zA-Z0-9]+\?/;
    const match = url.match(pattern);
    return match ? `${match[1]}.png` : null;
}

async function downloadAndUploadFile(img_url: string, bucket_name: string, file_name: string): Promise<any> {
    const response = await fetch(img_url);
    if (!response.ok) {
        throw new Error(`Failed to download file: ${response.statusText}`);
    }
    const fileContent = await response.arrayBuffer();
    const { data, error } = await supabase.storage
        .from(bucket_name)
        .upload(file_name, new Blob([fileContent]));
    if (error) {
        throw new Error(`Failed to upload file to Supabase Storage: ${error.message}`);
    }
    return data;
}

async function updateItem(item: any, file_name: string): Promise<void> {
    const { error } = await supabase
        .from('data')
        .update({
            img_url: `https://uzefbkvgsuzmopxjxymz.supabase.co/storage/v1/object/public/${BUCKET_NAME}/${file_name}`,
            moved: true
        })
        .eq('date', item.date);
    if (error) {
        throw new Error(`Failed to update item: ${error.message}`);
    }
    console.log(`${LOG_PREFIX} Item ${item.date} - ${item.title} updated successfully`);
}

Deno.serve(async (req) => {
    try {
        // await updateMovedStatus();
        const items = await fetchItems();

        for (const item of items) {
            const file_name = extractFileName(item.wav_url);
            if (!file_name) {
                console.error(`${LOG_PREFIX} Failed to extract file name from URL:`, item.img_url);
                continue;
            }

            console.log(`${LOG_PREFIX} URL : ${item.img_url}`);
            console.log(`${LOG_PREFIX} FILENAME : ${file_name}`);

            try {
                await downloadAndUploadFile(item.img_url, BUCKET_NAME, file_name);
                await updateItem(item, file_name);
            } catch (error) {
                console.error(`${LOG_PREFIX} An error occurred during download or update:`, error);
            }
        }

        return new Response(
            JSON.stringify({ message: "Process completed successfully" }),
            { headers: { "Content-Type": "application/json" } }
        );
    } catch (error) {
        console.error(`${LOG_PREFIX} An unexpected error occurred:`, error);
        return new Response(
            JSON.stringify({ error: "An unexpected error occurred" }),
            { status: 500, headers: { "Content-Type": "application/json" } }
        );
    }
});