import os
import requests
from datetime import datetime

# 시크릿 변수 읽기
FUNCTIONS_BEARER_TOKEN = os.getenv('FUNCTIONS_BEARER_TOKEN')

if not FUNCTIONS_BEARER_TOKEN:
    raise ValueError("FUNCTIONS_BEARER_TOKEN 환경 변수가 설정되지 않았습니다.")

# Supabase Edge Function 호출
# url = 'https://your-supabase-url/functions/v1/your-function-name'
# headers = {
#     'Authorization': f'Bearer {FUNCTIONS_BEARER_TOKEN}'
# }
# response = requests.post(url, headers=headers)

# 결과 파일에 쓰기
# with open('result.txt', 'w') as file:
#     if response.status_code == 200:
#         file.write(f"실행시간 : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ok\n")
#     else:
#         file.write(f"실행시간 : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 실패\n")

if FUNCTIONS_BEARER_TOKEN:
        print(f"FUNCTIONS_BEARER_TOKEN 값이 존재합니다: \n")


