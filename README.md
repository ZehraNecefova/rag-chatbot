![Build Status](https://github.com/ZehraNecefova/project2/actions/workflows/ci-build.yaml/badge.svg)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![3.12](https://img.shields.io/badge/Python-3.12-green.svg)](https://shields.io/)


# 🤖 RAG Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot that answers questions using company knowledge stored in **AWS Bedrock**. The system consists of a **FastAPI** backend and a **Streamlit** frontend, containerized with **Docker**.

---


## 🗂 Project Structure

```bash
rag-chatbot/
├── backend/
│   ├── main.py
│   └── Dockerfile
├── frontend/
│   ├── app.py
│   └── Dockerfile
├── docker-compose.yml
└── .env
```



---


## 🛠 Features

- Real-time chat with AI-generated answers using company knowledge.
- Multiple chat sessions with chat history stored in session state.
- Model selection between different Bedrock models (e.g., Claude 3.7 Sonnet, Claude 2).
- System instructions for customizing AI behavior.
- Responsive web interface with a clean, styled chat interface.
- Containerized deployment with Docker and docker-compose.

---

## ⚡ Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd rag-chatbot
```




### 2. Create `.env` file

```env
AWS_REGION=<your-aws-region>
KNOWLEDGE_BASE_ID=<your-knowledge-base-id>
AWS_ACCESS_KEY_ID=<your-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
```


### 3. Start containers
```bash
docker-compose up --build
```

Access the apps:

- **Frontend:** `http://18.205.131.207:8501`
- **Backend:** `http://18.205.131.207:8000/docs`



## 🐳 Docker Compose Services

- **backend:** FastAPI server for handling chat requests.  
- **frontend:** Streamlit app for user interaction.  
- **network:** Docker bridge network connecting frontend and backend.  

---

## 🛠 Tech Stack

- **Frontend:** Streamlit, HTTPX, asyncio  
- **Backend:** FastAPI, boto3, Pydantic  
- **Deployment:** Docker, docker-compose, AWS EC2  
- **LLM & KB:** AWS Bedrock (Claude models)
  
