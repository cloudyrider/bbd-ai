from openai import OpenAI
import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

if api_key is None:
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

client = OpenAI(api_key=api_key)

model_settings = {
    "model": "gpt-4o-mini",
    "role_message": {"role": "system",
                      "content":
                      "너는 보안을 담당하고 스미싱이라는 스팸 문자 데이터들을 분류하는 역할을 할꺼야. 앞으로 너가 받는 문자 데이터들을 분석해서 스미싱 데이터인지 아닌지 판별해줘"
                    }    
}

def initmodel():
    global model_settings
    try:
        response = client.chat.completions.create(
            model=model_settings["model"],
            messages=[model_settings["role_message"]],
            temperature=0
        )
        return response
    except openai.error.OpenAIError as e:
        print(f"OpenAI API 오류: {e}")
        return None

def isSpam(data: str) -> str:
    global model_settings
    try:
        response = client.chat.completions.create(
            model=model_settings["model"],
            messages=[
                model_settings["role_message"],
                {"role": "user", "content" : data}
            ],
            temperature=0
        )

        result = response.choices[0].message.content
        return result

    except openai.error.OpenAIError as e:
        print(f"OpenAI API 오류: {e}")
        return None


text = """[국제발신]
오빠는 친구가 될 수 있나요?한국에서 만나고 싶은데, 내 LINE:m203036"""

initmodel()
print(isSpam(text))