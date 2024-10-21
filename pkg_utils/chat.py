from langchain_openai import AzureChatOpenAI


def make_poem(user_input):
    chat_model = AzureChatOpenAI()
    # st.write(f"[사용자]\n")
    # st.write(f"{user_input}\n\n")
    result = chat_model.invoke(input=user_input + "의 3글자로 3행시 만들어. 형식은 반드시 ['글자': 내용, '글자': 내용, '글자': 내용.] 으로 작성해")
    # st.write(f"[챗봇]\n")
    # st.write(f"{result.content}\n\n")
    return result.content
