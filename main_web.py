from streamlit import button, text_input, title, write
# import asyncio
# from pkg_azure_ai import chatbot
# from pkg_azure_ai.dalle import generate_image
# from pkg_db.db import DatabaseManager
# from pkg_utils.utils import make_history

# Streamlit 애플리케이션 설정
title('3행시 갤러리 using TTS, STT, Dall-E3, Chat-GPT4o with VTube')

# 데이터베이스 초기화
# db = DatabaseManager()

# 사용자 입력 받기
user_input = text_input('3행시를 만들 3글자를 입력하세요:')

if button('시작'):
    if user_input:
        write(f"[사용자]\n{user_input}\n")
        write('인공지능이 단어를 가지고 삼행시를 생성 중 입니다.')

        # 챗봇 응답 생성
        # generated_text = chatbot.chat(user_input)
        # st.write(f"[챗봇]\n{generated_text}\n\n")

        # 이미지 생성
        # img_url = asyncio.run(generate_image(generated_text))

        # if img_url is not None:
            # now = make_history(generated_text, img_url, f'temp/gen_text.wav')
        # else:
        #     st.write("부적절한 단어 사용등의 이유로 이미지 생성이 취소되었습니다. 기본이미지로 저장합니다.")
            # now = make_history(generated_text, 'default_img', f'temp/gen_text.wav')

        # 데이터베이스에 저장
        # db.add_data(now, user_input)

        # 생성된 이미지 표시
        # st.image(img_url if img_url else 'default_img', caption='Generated Image')

# 히스토리 표시
write('히스토리')
# all_data = db.select_all_data()
# for row in all_data:
#     st.write(row[1])