import asyncio
import json
import os
import webbrowser

from openai import AzureOpenAI


client = AzureOpenAI(
    api_version=os.environ["OPENAI_API_VERSION_EASTUS"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT_EASTUS"],
    api_key=os.environ["AZURE_OPENAI_API_KEY_EASTUS"],
)


async def generate_image(prompt: str):
    prompt = prompt + "\nExcept words that violate policy. A vibrant painting in the style of a famous artist."
    print(prompt)
    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(client.images.generate, model="Dalle3", prompt=prompt, n=1), timeout=15
        )
        #client.images.generate는 동기함수이고, 블럭킹 IO 작업임.
        #asyncio.to_thread를 사용하여 동기함수를 비동기로 실행함.
        #asyncio.wait_for를 사용하여 비동기함수의 실행시간을 제한함.
        #asyncio.wait_for를 사용하면 result값이 반환될 때까지 기다림.
        #이렇게 함으로써, 비동기함수의 실행시간이 오래걸려도 메인스레드가 블럭되지 않음.
        #이미지 생성이 15초 이상 걸리면 TimeoutError 발생.
        #이미지 생성이 성공하면 이미지 URL을 반환함.
        #이미지 생성이 실패하면 Exception 발생.
        #이미지 생성이 실패하면 None을 반환함.
        #asyncio.to_thread를 사용하는 이유는, 비동기함수에서 동기함수를 호출할 때 사용함.
        #asyncio.to_thread를 사용하면, 동기함수를 비동기로 실행하기 위해 별도의 쓰레드에서 실행함.
        #별도의 쓰레드로 실행하는 이유는 이벤트루프가 블럭되지 않도록 하기 위함.
        # -> 블럭되면 다른 비동기함수가 실행되지 않음. -> 비동기로 만드는 의미가 없어짐.

        image_url = json.loads(result.model_dump_json())['data'][0]['url']
        webbrowser.open(image_url)
        print(f"Image generated: {image_url}")
        return image_url
    except asyncio.TimeoutError:
        print("Error: Image generation timed out.")
        return None
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


# def generate_image(prompt: str):
#     prompt = prompt + "\nExcept words that violate policy. A vibrant painting in the style of a famous artist."
#
#     def target():
#         try:
#             result = client.images.generate( # 1 단계코드 블럭킹 IO 작업
#                 model="Dalle3",
#                 prompt=prompt,
#                 n=1,
#             )
#             image_url = json.loads(result.model_dump_json())['data'][0]['url']
#             print(f"Image generated: {image_url}")
#             webbrowser.open(image_url)
#             return image_url
#         except Exception as e:
#             print(f"Error generating image: {e}")
#             return None
#
#     thread = threading.Thread(target=target)
#     thread.start() # 2 단계코드 넌블럭킹 IO 작업


# asyncio 모듈에는 다양한 유용한 함수들이 있습니다. 몇 가지 주요 함수들을 소개하겠습니다:
#
# asyncio.run(coro):
# 주어진 코루틴을 실행하고 완료될 때까지 기다립니다. 주로 메인 함수에서 사용됩니다.
# asyncio.create_task(coro):
# 코루틴을 태스크로 스케줄링하여 백그라운드에서 실행합니다. 여러 코루틴을 동시에 실행할 때 유용합니다.
# asyncio.gather(*coros):
# 여러 코루틴을 동시에 실행하고, 모든 코루틴이 완료될 때까지 기다립니다. 모든 코루틴의 결과를 리스트로 반환합니다.
# asyncio.sleep(delay):
# 주어진 시간 동안 비동기적으로 대기합니다. 주로 테스트나 지연을 시뮬레이션할 때 사용됩니다.
# asyncio.Queue:
# 비동기적으로 사용할 수 있는 큐를 제공합니다. 여러 태스크 간에 데이터를 안전하게 공유할 수 있습니다.
# asyncio.Event:
# 비동기 이벤트 객체를 제공합니다. 한 태스크가 이벤트를 설정하면 다른 태스크가 이를 기다릴 수 있습니다.
# asyncio.Lock:
# 비동기적으로 사용할 수 있는 락을 제공합니다. 여러 태스크가 동일한 리소스를 안전하게 접근할 수 있도록 합니다.
# asyncio.Semaphore:
# 비동기 세마포어를 제공합니다. 제한된 리소스를 여러 태스크가 동시에 접근할 수 있도록 합니다.

# 이미지 생성 작업이 네트워크 요청을 포함한 I/O 바운드 작업이라면 asyncio 버전이 더 효율적일 가능성이 높습니다.
# 반면에, 이미지 생성이 CPU 바운드 작업이라면 스레딩 버전이 더 적합할 수 있습니다.
# << 하지만 GIL 때문에 AI가 하는 말은 거짓말임. >>