import openai
import os
from dotenv import load_dotenv

class SummaryMessage:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')

        if self.api_key is None:
            raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

        openai.api_key = self.api_key

        self.model_settings = {
            "model": "gpt-4-turbo",
            "role_message": {
                "role": "system",
                "content": "너는 문자 데이터를 받으면 그 데이터를 내가 알기 쉽게 요약을 해서 줄꺼야. 나는 너가 육하원칙에 맞게 요약해줬으면 좋겠어."
            }    
        }

    def initmodel(self):
        try:
            response = openai.chat.completions.create(
                model=self.model_settings["model"],
                messages=[self.model_settings["role_message"]],
                temperature=0
            )
            return response
        except openai.error.OpenAIError as e:
            print(f"OpenAI API 오류: {e}")
            return None

    def summary(self, data: str) -> str:
        try:
            response = openai.chat.completions.create(
                model=self.model_settings["model"],
                messages=[
                    self.model_settings["role_message"],
                    {"role": "user", "content": data}
                ],
                temperature=0
            )

            result = response.choices[0].message.content
            return result
        except openai.error.OpenAIError as e:
            print(f"OpenAI API 오류: {e}")
            return "오류 발생"

# 테스트 코드
if __name__ == "__main__":
    text = """[국제발신]
    오빠는 친구가 될 수 있나요? 한국에서 만나고 싶은데, 내 LINE:m203036"""

    summary = SummaryMessage()
    summary.initmodel()
    print(summary.summary(text))
