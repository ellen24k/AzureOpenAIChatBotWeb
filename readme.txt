## git bash terminal

## .git/hooks/post-commit 파일 생성
#!/bin/bash

# version.txt 파일에서 현재 버전 값을 읽음
version=$(cat version.txt)

# 버전 값을 '.'으로 분리하여 배열로 저장
IFS='.' read -r -a version_parts <<< "$version"

# 마지막 자리 값을 1 증가시킴
last_index=$((${#version_parts[@]} - 1))
version_parts[$last_index]=$((${version_parts[$last_index]} + 1))

# 증가된 버전 값을 다시 문자열로 결합
new_version=$(IFS='.'; echo "${version_parts[*]}")

# 새로운 버전 값을 version.txt 파일에 저장
echo "$new_version" > version.txt

## git bash terminal
chmod +x post-commit
--