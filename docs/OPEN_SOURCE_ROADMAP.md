# Open Source Roadmap

This roadmap describes how the Dongseong-ro Startup Support Chatbot can grow as an open-source project.

## Project Vision

The goal of this project is to provide a reusable RAG chatbot template for local startup-support information. Although the first target area is Dongseong-ro in Daegu, the same structure can be adapted to other local districts, university entrepreneurship centers, and public startup-support programs.

The project combines:

- local business and startup-status data;
- policy and support-program retrieval;
- trend-analysis responses;
- a FastAPI backend;
- a React chatbot frontend;
- deployment and documentation assets.

## Current Maintainer Focus

The current maintainer focus is to improve the project from a successful team-built prototype into a cleaner open-source reference implementation.

Priority areas:

1. clearer setup and deployment documentation;
2. safer handling of environment variables and external API keys;
3. reproducible sample data and example questions;
4. better category-classification evaluation;
5. retrieval-quality improvement for startup, policy, and trend questions;
6. improved frontend accessibility and mobile responsiveness.

## Short-Term Tasks

- Add more sample questions and expected behaviors.
- Add a minimal public sample dataset for local testing.
- Add backend smoke tests for `/api/chat`.
- Add documentation for category-routing behavior.
- Add troubleshooting notes for model loading and API-key setup.
- Replace placeholder deployment URLs with verified links or remove them.

## Mid-Term Tasks

- Add evaluation scripts for category classification accuracy.
- Add retrieval-evaluation examples for policy and startup questions.
- Add a small benchmark set for local-business QA.
- Add Docker-based quickstart instructions.
- Improve CI checks for backend and frontend builds.
- Add issue templates for bugs, documentation requests, and data-source requests.

## Long-Term Tasks

- Generalize the system so other local districts can reuse the chatbot structure.
- Support multiple regional datasets through configuration files.
- Improve policy-source refresh workflows.
- Add admin documentation for maintaining local datasets.
- Add multilingual or bilingual response options if needed.
- Provide a stable release package for educational and public-sector use cases.

## OpenAI / Codex Usage Plan

OpenAI tools and API credits would be used to accelerate practical open-source maintenance tasks:

- generating and reviewing tests for backend and retrieval logic;
- improving documentation quality and setup reproducibility;
- refactoring service modules without changing public behavior;
- creating safer prompt templates for policy and startup-analysis answers;
- building evaluation scripts for classification and retrieval quality;
- supporting issue triage and release-note generation.

The goal is not only to improve a single chatbot, but to turn the project into a reusable template for local startup-support information systems.

## Contribution Opportunities

Contributors can help with:

- documentation cleanup;
- sample-data creation;
- RAG retrieval experiments;
- prompt and response-quality evaluation;
- frontend UI improvement;
- deployment and CI/CD reliability;
- local startup-policy data-source integration.
