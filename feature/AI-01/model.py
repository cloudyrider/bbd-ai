import openai
import os
from dotenv import load_dotenv

class SpamClassifier:
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
                "content": "너는 보안을 담당하고 스미싱이라는 스팸 문자 데이터들을 분류하는 역할을 할꺼야. 앞으로 너가 받는 문자 데이터들을 분석해서 스미싱 데이터인지 아닌지 판별해줘. 응답은 '예' 또는 '아니오' 형태로만 해줘."
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

    def is_spam(self, data: str) -> str:
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

    classifier = SpamClassifier()
    classifier.initmodel()
    print(classifier.isSpam(text))
