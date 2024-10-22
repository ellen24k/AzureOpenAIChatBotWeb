import os


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
