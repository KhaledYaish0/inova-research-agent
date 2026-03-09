# Inova Research Agent

## Overview

The **Inova Research Agent** is an AI-powered backend platform developed as part of the **Inova Solutions AI & DevOps Internship Program**.

The goal of this project is to build a **production-ready AI agent platform** capable of:

* Processing user queries
* Interacting with Large Language Models (LLMs)
* Using external tools (such as search)
* Maintaining conversational memory
* Running inside containerized infrastructure
* Deploying automatically through CI/CD pipelines
* Scaling using Kubernetes
* Providing monitoring and observability

This repository represents the **foundation of the system**, starting with a FastAPI backend and evolving toward a full **agentic AI infrastructure**.

---

# System Architecture (Planned)

The final architecture of the system is designed to support scalable AI agents.

```
User
 ↓
Frontend Interface
 ↓
FastAPI Backend
 ↓
Agent Orchestration Layer
 ↓
LLM + Tools + Memory
 ↓
Database
 ↓
Containerized Infrastructure
 ↓
Kubernetes Cluster
 ↓
Monitoring & Observability
```

---

# Project Goals

The project is designed to progressively implement the following capabilities:

* AI-powered query processing
* Agent-based workflows
* Persistent memory for conversations
* Tool usage (search, APIs, etc.)
* Containerized deployment
* Infrastructure automation
* Production monitoring

---

# Tech Stack

### Backend

* Python
* FastAPI
* Pydantic

### AI Layer

* OpenAI API
* LangGraph *(planned)*
* CrewAI *(possible extension)*

### Infrastructure

* Docker
* Docker Compose
* Linux Server

### DevOps

* GitHub
* CI/CD pipelines
* Ansible *(planned)*

### Data Layer

* PostgreSQL *(planned)*
* MongoDB *(alternative)*

### Observability

* Prometheus *(planned)*
* Grafana *(planned)*

---

# Project Structure

```
inova-research-agent
│
├── app
│   ├── main.py          # FastAPI application
│   ├── llm.py           # LLM integration logic
│   └── schemas.py       # API request/response models
│
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore
└── README.md
```

---

# API Endpoints

## Root

```
GET /
```

Returns a simple message confirming that the API is running.

Example response:

```
{
  "message": "Inova Research Agent API is running."
}
```

---

## Health Check

```
GET /health
```

Used to verify that the backend service is operational.

Example response:

```
{
  "status": "OK!"
}
```

---

## Query Endpoint

```
POST /query
```

Accepts a text prompt and returns an LLM-generated response.

Example request:

```
{
  "text": "What is artificial intelligence?"
}
```

Example response:

```
{
  "response": "Artificial intelligence (AI) refers to..."
}
```

---

# Running the Project Locally

### 1. Clone the repository

```
git clone https://github.com/AmrQamhieh/inova-research-agent.git
cd inova-research-agent
```

Checkout the development branch:

```
git checkout develop
```

---

### 2. Create a virtual environment

```
python -m venv venv
```

Activate it:

Windows:

```
venv\Scripts\activate
```

Linux / Mac:

```
source venv/bin/activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

### 5. Run the API

```
uvicorn app.main:app --reload
```

Open the interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

# Development Workflow

Development is performed on the **develop branch**.

Typical workflow:

```
git checkout develop
git pull origin develop
git add .
git commit -m "feat: implement feature"
git push origin develop
```

---

# Roadmap

Planned future milestones:

* Agent orchestration using LangGraph
* Search tool integration
* Persistent conversation memory
* Docker containerization
* Infrastructure automation with Ansible
* CI/CD pipeline implementation
* Kubernetes deployment
* Monitoring with Prometheus and Grafana

---

# Contributors

* **Khaled Yaish** – AI / Backend Development
* **Amr Qamhieh** – DevOps / Infrastructure

---

# License

This project is developed for educational and research purposes as part of the **Inova Solutions Internship Program**.
