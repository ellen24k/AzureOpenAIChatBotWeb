import json
import random
import time

import streamlit as st
from openai import AzureOpenAI

client = AzureOpenAI(
    api_version=st.secrets["OPENAI_API_VERSION_EASTUS"],
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT_EASTUS"],
    api_key=st.secrets["AZURE_OPENAI_API_KEY_EASTUS"],
)


def generate_image_sync(prompt, test=False):
    if test:
        img_url = None
        time.sleep(random.randint(10,15))
        return img_url

    prompt = prompt + "\nA vibrant painting in the style of a famous artist."

    try:
        result = client.images.generate(
            model="Dalle3",
            prompt=prompt,
            n=1,
        )
        image_url = json.loads(result.model_dump_json())['data'][0]['url']
        print(f"Image generated: {image_url}")
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

# async def generate_image_async(prompt: str,test=False):
#     if test:
#         img_url = None
#         await asyncio.sleep(random.randint(10,20))
#         return img_url
#
#     prompt = prompt + "\nA vibrant painting in the style of a famous artist."
#
#     try:
#         result = client.images.generate(
#             model="Dalle3",
#             prompt=prompt,
#             n=1,
#         )
#         image_url = json.loads(result.model_dump_json())['data'][0]['url']
#         print(f"Image generated: {image_url}")
#         return image_url
#     except Exception as e:
#         print(f"Error generating image: {e}")
#         return None

#
# async def generate_image_async(prompt: str, test=False):
#     if test:
#         img_url = None
#         await asyncio.sleep(random.randint(10, 20))
#         return img_url
#
#     loop = asyncio.get_event_loop()
#     with ThreadPoolExecutor() as pool:
#         image_url = await loop.run_in_executor(pool, generate_image_sync, prompt)
#     return image_url