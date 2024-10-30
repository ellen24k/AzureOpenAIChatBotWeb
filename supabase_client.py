import os
from datetime import datetime

import requests

if os.getenv('DEVENV'):
    print("Development environment detected. Loading environment variables from .env file.")
    from dotenv import load_dotenv
    load_dotenv()

FUNCTIONS_BEARER_TOKEN = os.getenv('FUNCTIONS_BEARER_TOKEN')

if not FUNCTIONS_BEARER_TOKEN:
    raise ValueError("FUNCTIONS_BEARER_TOKEN 환경 변수가 설정되지 않았습니다.")
    sys.exit(1)


# Supabase Edge Function 호출
def request_edge_function_chatbot_dalle_image_batch_processor():
    function_url = 'https://uzefbkvgsuzmopxjxymz.supabase.co/functions/v1/chatbot_dalle_image_batch_processor'

    headers = {
        'Authorization': f'Bearer {FUNCTIONS_BEARER_TOKEN}'
    }
    data = {
        'name': 'Functions',
    }
    response = requests.post(function_url, headers=headers, json=data)
    print(f"Request URL: {function_url}")
    print(f"Request Headers: {headers}")
    print(f"Request Data: {data}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ok\n")

    if response.status_code != 200:
        print(f"Error invoking function: {response.json().get('message', 'Unknown error')}")
        return None
    else:
        return response.json()


request_edge_function_chatbot_dalle_image_batch_processor()

# todo 호출은 내용을 바꿔. download_file 함수 호출은 안할거야. 환경변수 다 정리하고.
# edge function을 만들어 이름은 chatbot_dalle_image_batch_processor
# 함수는 호출되면
# data table에서 moved == False 인 리스트 쿼리해서
# img_url을 받아서 download_file 함수 호출 하고
# public_url 을 리턴 받아
# supabase에 img_url값으로 업데이트 하고
# moved == True로 업데이트 해.
# python supabase_client.py는 call만 하면 됨. 로그는 supabase에서 볼거야.
