# version_tracker.py

import os
import sys
from datetime import datetime

def create_version_file():
    # 버전 파일 경로 설정
    version_file = "version.txt"

    # 커밋 메시지 가져오기
    commit_message = sys.argv[1] if len(sys.argv) > 1 else "No commit message"

    # 현재 날짜와 시간 가져오기
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 새로운 버전 정보
    version_info = f"{timestamp} - {commit_message}\n"

    # 버전 파일에 추가
    with open(version_file, "a") as f:
        f.write(version_info)

def read_version_file():
    # 버전 파일 경로 설정
    version_file = "version.txt"

    # 버전 정보 읽기
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            content = f.read()
            print(content)
    else:
        print("No version information found.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        create_version_file()
    else:
        read_version_file()
