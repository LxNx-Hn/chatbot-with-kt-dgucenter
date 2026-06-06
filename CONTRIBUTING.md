# Contributing to Dongseong-ro Startup Support Chatbot

Thank you for your interest in contributing to this project. This repository is maintained as an open-source RAG chatbot project for startup-support information, local business trend analysis, and policy information retrieval in the Dongseong-ro / Daegu startup ecosystem.

## Project Scope

This project focuses on:

- RAG-based question answering for startup and policy information;
- local business data processing and trend analysis;
- category classification for startup, policy, and trend questions;
- FastAPI backend service improvement;
- React-based chatbot UI improvement;
- deployment, documentation, and reproducibility.

## How to Contribute

You can contribute by:

1. reporting bugs or unclear responses;
2. improving documentation and setup guides;
3. adding sample questions and expected behavior cases;
4. improving data preprocessing logic;
5. improving retrieval quality, prompt design, or category classification;
6. adding tests or validation scripts;
7. improving frontend accessibility and responsive UI behavior.

## Development Setup

Backend:

```bash
cd DSL_CHAT_BOT/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:

```bash
cd DSL_CHAT_BOT/frontend
npm install
npm start
```

Environment variables and API keys should be managed locally. Do not commit `.env` files or private credentials.

## Contribution Rules

- Keep public documentation free of private keys, personal data, and unreleased credentials.
- Do not fabricate evaluation metrics. If a metric is reported, include how it was measured.
- Keep examples reproducible with sample or public data.
- Explain the purpose of each pull request clearly.
- Prefer small, focused pull requests over large mixed changes.

## Suggested Pull Request Format

```md
## Summary
- What changed?

## Motivation
- Why is this change needed?

## Validation
- How did you test it?

## Notes
- Any limitations or follow-up tasks?
```

## Maintainer Role

The project is maintained by the repository owner, who served as project leader and was responsible for overall architecture, RAG system direction, service integration, deployment flow, documentation, and project coordination.
