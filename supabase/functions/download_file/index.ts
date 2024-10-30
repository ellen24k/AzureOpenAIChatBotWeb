import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import { createClient } from "https://cdn.skypack.dev/@supabase/supabase-js"

const LOG_PREFIX = "[CHATBOT][DOWNLOAD_IMAGE_FILE]";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_KEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

console.log(`${LOG_PREFIX} Starting the download_file function.`);

interface RequestData {
  img_url: string;
  bucket_name: string;
  file_name: string;
}

async function fetchFile(img_url: string): Promise<ArrayBuffer> {
  const response = await fetch(img_url);
  if (!response.ok) {
    throw new Error(`Failed to download file: ${response.statusText}`);
  }
  return await response.arrayBuffer();
}

async function uploadFile(bucket_name: string, file_name: string, fileContent: ArrayBuffer): Promise<any> {
  const { data, error } = await supabase.storage
    .from(bucket_name)
    .upload(file_name, new Blob([fileContent]));

  if (error) {
    throw new Error(`Failed to upload file to Supabase Storage: ${error.message}`);
  }
  return data;
}

Deno.serve(async (req) => {
  try {
    const { img_url, bucket_name, file_name }: RequestData = await req.json();
    console.log(`${LOG_PREFIX} Request received:`, { img_url, bucket_name, file_name });

    const fileContent = await fetchFile(img_url);
    const data = await uploadFile(bucket_name, file_name, fileContent);

    console.log(`${LOG_PREFIX} File uploaded successfully:`, data);
    return new Response(
      JSON.stringify({ message: "File uploaded successfully", data }),
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