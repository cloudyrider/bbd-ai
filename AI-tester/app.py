from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class MessageRequest(BaseModel):
    message: str

# API 엔드포인트 정의
@app.post("/is_spam")
async def check_spam(request: MessageRequest):
    result = is_spam(request.message)
    if result is None:
        raise HTTPException(status_code=500, detail="스미싱 판별 중 오류가 발생했습니다.")
    return {"message": request.message, "is_spam": result}

# 테스트용 엔드포인트
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# FastAPI 애플리케이션 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)