# AI-Workflow-Playground

This project is about experimenting with AI-powered workflows that can help small and medium-sized businesses automate everyday tasks. The idea is to start small, running everything locally with free tools, and then scale up to a VPS and eventually the cloud as the workflows become more useful and businesses start adopting them.

## Vision

1. Start with simple workflows like:
   - Email triage and drafting replies
   - Answering common customer questions (FAQ bot)
   - Transcribing and summarizing phone calls

2. Package each workflow so it can run independently. That way, they can be reused or even sold later as plug-and-play modules.

3. Scale from local → VPS → cloud, only when needed.

## Tech Stack

- LangChain for workflow orchestration
- Docker for containerization
- MCP (Model Context Protocol) for modular tool integration
- SQLite for lightweight storage
- VS Code as the main development environment

## Repository Structure

```
workflows/
  email_agent/       # Handles email triage and drafting
  faq_agent/         # Answers customer questions from docs/website
  call_agent/        # Transcribes and summarizes calls

docker/
  Dockerfile
  docker-compose.yml

scripts/             # Setup and automation scripts
.env.example         # Example environment variables
README.md
```

## Example Workflow: Email Agent

- Connects to an IMAP inbox
- Classifies emails into categories (support, sales, spam)
- Generates a draft reply
- Optionally saves results to a local database

## Getting Started

1. Clone the repo:
   ```
   git clone https://github.com/your-username/ai-workflows.git
   cd ai-workflows
   ```

2. Copy the environment file:
   ```
   cp .env.example .env
   ```
   Fill in your API keys and email credentials.

3. Run with Docker:
   ```
   docker-compose up --build
   ```

4. Test locally:
   - Email agent: http://localhost:8000/email
   - FAQ agent: http://localhost:8000/faq
   - Call agent: http://localhost:8000/call

## Roadmap

- Add scheduling and calendar integration
- Build a simple web dashboard for SMBs
- Package workflows as installable modules
- Deploy to VPS (Hetzner, Fly.io, etc.)
- Scale to cloud with Kubernetes

## Business Use Cases

- Dentist’s office: AI answers calls and schedules appointments
- Real estate agent: AI drafts property descriptions and replies to inquiries
- E-commerce shop: AI handles order status questions

