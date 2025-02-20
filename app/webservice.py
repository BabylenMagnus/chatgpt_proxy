import os
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
from typing import Optional


app = FastAPI()


@app.post("/v1/chat/completions")
async def proxy_chat_completion(
        request: Request,
        authorization: Optional[str] = Header(None)
):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Отсутствует заголовок Authorization или он некорректен.")

    OPENAI_API_KEY = authorization.split("Bearer ")[-1].strip()

    if not OPENAI_API_KEY:
        raise HTTPException(status_code=401, detail="OPENAI_API_KEY не может быть пустым.")

    body = await request.json()

    if "model" not in body:
        raise HTTPException(status_code=400, detail="Параметр 'model' является обязательным.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    async with httpx.AsyncClient() as client:
        try:
            if body.get("stream"):
                async with client.stream(
                    "POST",
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=body,
                    timeout=None
                ) as response:
                    if response.status_code != 200:
                        content = await response.aread()
                        raise HTTPException(status_code=response.status_code, detail=content.decode())

                    async def event_generator():
                        async for chunk in response.aiter_bytes():
                            yield chunk

                    return StreamingResponse(event_generator(), media_type=response.headers.get("content-type"))
            else:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=body,
                )
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=response.text)

                return JSONResponse(status_code=response.status_code, content=response.json())
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе к OpenAI API: {str(exc)}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Непредвиденная ошибка: {str(exc)}")
