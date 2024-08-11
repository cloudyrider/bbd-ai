import os
import json
import time  # 시간 측정을 위해 time 모듈 추가
from openai import OpenAI
import requests
from dotenv import load_dotenv
import re

# 환경 변수 로드
load_dotenv()

# 환경 변수로 API 키 및 모델 설정
API_KEY_FOR_STANDARDIZATION = os.getenv("OPENAI_API_KEY_FOR_STANDARDIZATION")
API_KEY_FOR_EXTRACT = os.getenv("OPENAI_API_KEY_FOR_EXTRACT")
MODEL_STANDARDIZATION = os.getenv("GPT_4o_MODEL_STANDARDIZATION")  # Fine-tuning한 거
MODEL_EXTRACT = os.getenv("MODEL_EXTRACT", "gpt-4o-mini")  # 기본 모델

class TaskProcessor:
    def __init__(self):
        self.client_standardization = OpenAI(api_key=API_KEY_FOR_STANDARDIZATION)
        self.client_extract = OpenAI(api_key=API_KEY_FOR_EXTRACT)
        self.tasks = self.load_tasks('tasks.txt')
        self.messages = []  # 대화 기록을 저장할 리스트 초기화

    @staticmethod
    def load_tasks(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                tasks = file.read().splitlines()
            return tasks
        except Exception as e:
            print(f"An error occurred while loading tasks: {e}")
            return []

    def korean_standardization(self, command):
        try:
            # 대화 기록에 현재 입력된 사용자의 메시지를 추가
            self.messages.append({"role": "user", "content": command})

            # 대화 기록을 바탕으로 표준화 요청
            response = self.client_standardization.chat.completions.create(
                model=MODEL_STANDARDIZATION,
                messages=self.messages + [
                    {"role": "system", "content": "다음은 한국어를 소리 나는 대로 적은 것입니다. 만약 이것이 방언이라면 표준어로 바꾸세요."},
                    {"role": "user", "content": command},
                ],
                temperature=0,
            )

            # 표준화된 결과를 대화 기록에 추가
            standardized_response = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": standardized_response})

            return standardized_response
        
        except Exception as e:
            print(f"표준어화하는 도중에 에러가 발생함: {e}")
            return None

    def extract_request(self, command):
        try:
            tasks_string = ', '.join([f"{i+1}. {item}" for i, item in enumerate(self.tasks)])
            std_command = self.korean_standardization(command)

            if not std_command:
                return None, "Standardization failed"

            # 대화 기록을 바탕으로 요청 추출
            response = self.client_extract.chat.completions.create(
                model=MODEL_EXTRACT,
                messages=self.messages + [
                    {"role": "system", "content": f"고객이 원하는 것은 다음 가운데 무엇입니까? 다음 중 하나를 골라 번호만 답하세요. {tasks_string}. 반드시 번호를 답하셔야 합니다."},
                    {"role": "user", "content": std_command},
                ],
                temperature=0,
            )

            answer = response.choices[0].message.content.strip()

            # 정규 표현식 패턴 매칭
            if re.search(r'1|병원', answer):
                answer = "병원예약"
            elif re.search(r'2|택시', answer):
                answer = "택시예약"
            elif re.search(r'3|문자', answer):
                answer = "문자요약"
            else:
                answer = "답이 없음"

            # 추출된 결과를 대화 기록에 추가
            self.messages.append({"role": "assistant", "content": answer})

            return std_command, answer

        except Exception as e:
            print(f"요청 : {e}")
            return "답이 없음"
    
# TaskProcessor 클래스 사용 예시
if __name__ == "__main__":
    processor = TaskProcessor()

    while True:
        command = input("명령을 입력하세요 (종료하려면 'exit' 입력): ")
        if command.lower() == 'exit':
            break

        start_time = time.time()
        standardized_command, result = processor.extract_request(command)
        
        if standardized_command:
            print(f"Standardized Command: {standardized_command}")
        else:
            print("Standardization failed.")
        print(f"Extracted Request: {result}")

        end_time = time.time()
        print(f"Total Time: {end_time - start_time:.2f} seconds")