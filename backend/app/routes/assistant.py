import os
import logging
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import httpx
import json

router = APIRouter()

TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = os.getenv("TOGETHER_AI_API_KEY")

logger = logging.getLogger("assistant_stream")
logging.basicConfig(level=logging.INFO)


@router.get("/ask_assistant_stream")
async def ask_assistant_stream(
    question: str,
    history: str = Query(
        default="",
        description='Диалог в JSON-строке, например [{"role":"user","content":"..."}, ...]',
    ),
):
    logger.info(f"Received question: {question}")
    logger.info(f"Received history (truncated): {history[:200]}")

    if not API_KEY:
        logger.error("API key is not set")
        raise HTTPException(status_code=500, detail="API key not set")

    # Восстановим историю, если есть
    try:
        messages = json.loads(history) if history else []
        if not isinstance(messages, list):
            raise ValueError("History must be a list of messages")
    except Exception as e:
        logger.warning(f"Failed to parse history JSON: {e}")
        messages = []

    # Добавим новый вопрос пользователя
    messages.append({"role": "user", "content": question})

    # Системное сообщение с инструкцией
    system_msg = {
        "role": "system",
        "content": (
            "Ты - шуточный ассистент для мед сайта OSCORP. "
            "Отвечай в шуточной форме, пример: Пациент: ... Ты: ... "
            "Список врачей:\n"
            'Билли Херингтон — Проктолог (Специалист по "задним делам")\n'
            "Чокколата — Хирург (Знает всё о внутренностях человека (узнал на не врачебном опыте))\n"
            "Грегори Хаус — Инфекционные заболевания и нефрология (мудак)\n"
            'Шон Мёрфи — Хирург (Постоянно кричит "I AM A SURGEON")\n'
            "Мэтт Смит — Терапевт общей практики\n"
            "Дэвид Тенант — Педиатр-иммунолог"
        ),
    }

    data = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "messages": [system_msg] + messages,
        "stream": True,
        "temperature": 0.4,
        "max_tokens": 350,
    }

    client = httpx.AsyncClient(timeout=None)
    try:
        response = await client.post(
            TOGETHER_API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json=data,
        )
        response.raise_for_status()
    except Exception as e:
        await client.aclose()
        logger.error(f"Request to Together API failed: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to fetch assistant response"
        )

    async def event_generator():
        try:
            async for line in response.aiter_lines():
                line = line.strip()
                if not line:
                    continue
                if line in ("data: [DONE]", "[DONE]"):
                    logger.info("Stream finished (received [DONE])")
                    yield "data: [DONE]\n\n"
                    break
                if line.startswith("data: "):
                    json_data = line[len("data: ") :]
                else:
                    json_data = line
                try:
                    chunk = json.loads(json_data)
                except json.JSONDecodeError:
                    continue
                content = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
                if content:
                    yield f"data: {content}\n\n"
        finally:
            await client.aclose()

    return StreamingResponse(event_generator(), media_type="text/event-stream")
