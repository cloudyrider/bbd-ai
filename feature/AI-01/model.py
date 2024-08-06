
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def get_llm_answer(data, MODEL = "gpt-4o-mini", NAME = '효민'):
    # GPT API 호출

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "당신은 원격 은행원이자 금융 비서입니다. 당신은 최신 기술에 서툰 노인과 대화하고 있습니다. 그들이 원하는 것을 파악해서 응대하세요."},
            {"role": "assistant", "content": "누구신가요?"},
            {"role": "user", "content": f"{NAME}입니다."},
        ],
        temperature=0,
    )

    return response.choices[0].message.content