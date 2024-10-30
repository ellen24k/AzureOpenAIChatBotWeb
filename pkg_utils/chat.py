import streamlit as st
from langchain_openai import AzureChatOpenAI


def make_poem(user_input):
    chat_model = AzureChatOpenAI(
        api_key=st.secrets["AZURE_OPENAI_API_KEY_EASTUS"],
        api_version=st.secrets["AZURE_OPENAI_API_VERSION_EASTUS_GPT4"],
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT_EASTUS_GPT4"],
    )
    user_input_reformat = f"'{user_input[0]}' '{user_input[1]}' '{user_input[2]}'"
    messages = [
        {"role": "system", "content": "You're a poet with a lot of sensibility."},
        {"role": "system", "content": f"The output format must be '{user_input[0]}': content '{user_input[1]}': content '{user_input[2]}': content"},
        {"role": "system", "content": "Do not generate any response message other than the output format."},
        {"role": "user",
         "content": f"{user_input_reformat} 3글자로 3행시 만들어."},
    ]
    print(messages)
    # {"role": "system", "content": "You're a gang boss with scary charisma."},
    result = chat_model.invoke(input=messages)
    return result.content
# system_prompt="You're a philosopher with a lot of sensibility."
