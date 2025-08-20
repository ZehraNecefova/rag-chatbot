# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import os
from dotenv import load_dotenv
import json
import time
from fastapi.responses import StreamingResponse

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")

# FastAPI app
app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bedrock clients
kb_client = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)
llm_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

class Query(BaseModel):
    question: str
    model: str = "Claude 3.7 Sonnet"
    system_instruction: str = ""

@app.post("/chat-stream")
async def chat_stream(query: Query):
    # 1️⃣ Retrieve docs from knowledge base
    response = kb_client.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={"text": query.question}
    )
    docs = [d["content"]["text"] for d in response["retrievalResults"]]
    context = "\n".join(docs)

    # 2️⃣ Prepare prompt
    prompt_text = (
        f"Human: Answer using company knowledge:\n{context}\n\n"
        f"Question: {query.question}\n\n"
        "Assistant:"
    )

    # 3️⃣ Invoke LLM
    llm_response = llm_client.invoke_model(
        modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": query.system_instruction or "You are a helpful assistant.",
            "messages": [{"role": "user", "content": prompt_text}],
            "max_tokens": 10240
        }).encode("utf-8")
    )

    # 4️⃣ Parse response
    response_text = llm_response["body"].read().decode("utf-8")
    response_json = json.loads(response_text)
    assistant_text = response_json["content"][0]["text"]

    # 5️⃣ Stream character by character
    def generate():
        for char in assistant_text:
            yield char
            time.sleep(0.01)  # adjust speed if needed

    return StreamingResponse(generate(), media_type="text/plain")
