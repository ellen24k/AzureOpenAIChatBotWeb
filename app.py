import os
import streamlit as st
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate

# Azure OpenAI 설정
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

llm = AzureOpenAI(api_key=api_key, endpoint=endpoint)

def app_page():
    st.title('3행시 갤러리 using TTS, STT, Dall-E3, Chat-GPT4o with VTube')
    user_input = st.text_input('3행시를 만들 3글자를 입력하세요:')

    if st.button('시작'):
        if user_input:
            st.write(f"[사용자]\n{user_input}\n")
            st.write('인공지능이 단어를 가지고 삼행시를 생성 중 입니다.')

            # Azure OpenAI에 질의
            prompt = PromptTemplate(template="Create a poem with the following three characters: {input}", input_variables=["input"])
            query = prompt.format(input=user_input)
            response = llm(query)

            st.write(f"[챗봇]\n{response}\n\n")

if __name__ == '__main__':
    app_page()