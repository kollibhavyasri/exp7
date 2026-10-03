from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI(title="AI Agent REST API")

# Reads the key from environment variables configured in cloud settings
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "default-placeholder-key"))

class Query(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

@app.post("/ask")
def ask_agent(query: Query):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": query.question}
            ]
        )
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
