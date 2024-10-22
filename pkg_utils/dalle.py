import asyncio
import json

import streamlit as st
from openai import AzureOpenAI

client = AzureOpenAI(
    api_version=st.secrets["OPENAI_API_VERSION_EASTUS"],
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT_EASTUS"],
    api_key=st.secrets["AZURE_OPENAI_API_KEY_EASTUS"],
)


def generate_image(prompt: str):
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

async def generate_image_async(prompt: str,test=False):
    if test:
        img_url = 'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_img.png'
        await asyncio.sleep(15)
        return img_url

    prompt = prompt + "\nA vibrant painting in the style of a famous artist."

    try:
        result = await client.images.generate(
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
