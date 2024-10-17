import os

import dotenv
from openai import AzureOpenAI

dotenv.load_dotenv()

deployment_name = os.environ['COMPLETIONS_MODEL_EASTUS']
api_key = os.environ["AZURE_OPENAI_API_KEY_EASTUS"]
azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT_EASTUS']
api_version = os.environ['OPENAI_API_VERSION_EASTUS']

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version
)


def chat(qry):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You're a philosopher with a lot of sensibility."},
                {"role": "system", "content": "The sentence you create will be drawn by AI into a nice picture."},
                {"role": "user", "content": "'" + qry + "'의 3글자로 3행시 만들어. 형식은 '글자: 내용,' 만 작성해"},
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    except Exception as e:
        print(f"An exception has occured. {e}")
