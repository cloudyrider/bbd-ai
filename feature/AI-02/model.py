import openai
import os
from dotenv import load_dotenv

class MessageSummary:
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
                "content": "너는 지금부터 문자 데이터들을 요약하는 역할을 할꺼야. 너가 받은 문자 데이터를 육하원칙에 최대한 맞춰서 요약해줘"
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

    def get_summary(self, data: str) -> str:
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

    summary = MessageSummary()
    summary.initmodel()
    print(summary.get_summary(text))
