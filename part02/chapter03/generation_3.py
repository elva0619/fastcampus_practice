import os

import openai
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    temperature: float = 1


def request_user_info():
    # import requests
    # requests.get("https://api.xxx.com/users/username/info")
    return """
    - Like Asia food
    - Like to travel to Spain.
    - 30 years old.
    """


def request_planning_manual():
    return """
    - 30 years old man likes eating food.
    - 30 years old man likes walking.
    """


SYSTEM_MSG = f"""You are a helpful travel assistant, Your name is Jini, 27 years old

Current User:
{request_user_info()}

Planning Manual:
{request_planning_manual()}
"""


def classify_intent(msg):
    prompt = f"""Your job is to classify intent.

    Choose one of the following intents:
    - travel_plan
    - customer_support
    - reservation

    User: {msg}
    Intent:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


@app.post("/chat")
def chat(req: ChatRequest):
    intent = classify_intent(req.message)

    if intent == "travel_plan":
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_MSG},
                {"role": "user", "content": req.message},
            ],
            temperature=req.temperature,
        )
        return {"message": response.choices[0].message.content}

    elif intent == "customer_support":
        return {"message": "Here is customer support number: 1234567890"}

    elif intent == "reservation":
        return {"message": "Here is reservation number: 0987654321"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.0.29", port=8501)
