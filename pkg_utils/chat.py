from langchain_openai import AzureChatOpenAI


def make_poem(user_input):
    chat_model = AzureChatOpenAI()
        # {"role": "system", "content": "You're a gang boss with scary charisma."},
    messages = [
        {"role": "system", "content": "You're a poet with a lot of sensibility."},
        {"role": "user", "content": "'" + user_input + "의 3글자로 3행시 만들어. 형식은 반드시 ['글자': 내용, '글자': 내용, '글자': 내용.] 으로 작성해"},
    ]
    result = chat_model.invoke(input=messages)
    return result.content
#system_prompt="You're a philosopher with a lot of sensibility."