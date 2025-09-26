# AI-Workflow-Playground

This project is about experimenting with AI-powered workflows that can help small and medium-sized businesses automate everyday tasks. The idea is to start small, running everything locally with free tools, and then scale up to a VPS and eventually the cloud as the workflows become more useful and businesses start adopting them.

## 🎯 Vision

1. **Start with simple workflows like:**
   - Email triage and drafting replies
   - Answering common customer questions (FAQ bot)
   - Transcribing and summarizing phone calls

2. **Package each workflow so it can run independently.** That way, they can be reused or even sold later as plug-and-play modules.

3. **Scale from local → VPS → cloud, only when needed.**

## 🛠️ Tech Stack

- **LangChain** for workflow orchestration
- **FastAPI** for REST API endpoints
- **Docker** for containerization
- **OpenAI GPT** for AI processing
- **Whisper** for audio transcription
- **SQLite** for lightweight storage
- **VS Code** as the main development environment

## 📁 Repository Structure

```
AI-Workflow-Playground/
├── workflows/
│   ├── email_agent/          # Email triage and drafting
│   │   └── email_processor.py
│   ├── faq_agent/            # Customer Q&A automation
│   │   └── faq_processor.py
│   └── call_agent/           # Call transcription and summarization
│       └── call_processor.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/
│   ├── setup.py              # Initial setup automation
│   ├── deploy.py             # Deployment scripts
│   └── test.py               # Testing automation
├── data/
│   └── knowledge_base/       # FAQ and business knowledge
├── main.py                   # FastAPI application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
└── README.md
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/ai-workflows.git
cd ai-workflows

# Run automated setup
python scripts/setup.py

# Edit your .env file with API keys
# Then start the application
python main.py
```

### Option 2: Docker Setup

```bash
# Clone and setup
git clone https://github.com/your-username/ai-workflows.git
cd ai-workflows

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Run with Docker
docker-compose -f docker/docker-compose.yml up --build
```

### Option 3: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p data/knowledge_base logs

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Start the application
python main.py
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Email Configuration (for email agent)
EMAIL_HOST=imap.gmail.com
EMAIL_PORT=993
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here

# Application Settings
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

### API Keys Required

- **OpenAI API Key**: For AI processing (email classification, FAQ answers, call summarization)
- **Email Credentials**: For email agent functionality
- **Optional**: Twilio for phone integration, webhook URLs for notifications

## 📡 API Endpoints

### Health Check
- `GET /health` - Service health status

### Email Workflow
- `POST /email/process` - Process new emails from inbox
- `POST /email/draft` - Draft a reply to an email

### FAQ Workflow  
- `POST /faq/answer` - Answer customer questions

### Call Workflow
- `POST /call/transcribe` - Transcribe audio files
- `POST /call/summarize` - Summarize call transcripts

## 🧪 Testing

```bash
# Run automated tests
python scripts/test.py

# Test specific endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/faq/answer \
  -H "Content-Type: application/json" \
  -d '{"question": "What are your business hours?"}'
```

## 📊 Workflow Examples

### Email Agent
- **Input**: IMAP email inbox
- **Process**: AI classifies emails (support, sales, spam, urgent)
- **Output**: Drafted replies, priority scoring, action items

### FAQ Agent  
- **Input**: Customer questions
- **Process**: Semantic search through knowledge base
- **Output**: Relevant answers with confidence scores

### Call Agent
- **Input**: Audio files (wav, mp3, m4a, etc.)
- **Process**: Whisper transcription + AI summarization
- **Output**: Transcripts, summaries, action items, sentiment analysis

## 🏢 Business Use Cases

### Small Business Examples
- **Dentist's office**: AI answers calls and schedules appointments
- **Real estate agent**: AI drafts property descriptions and replies to inquiries  
- **E-commerce shop**: AI handles order status questions
- **Consulting firm**: AI processes client emails and drafts responses
- **Restaurant**: AI takes reservations and answers menu questions

### Workflow Benefits
- **24/7 Availability**: Handle customer inquiries outside business hours
- **Consistency**: Standardized responses and processes
- **Scalability**: Handle multiple conversations simultaneously
- **Cost Efficiency**: Reduce manual customer service workload
- **Quality**: AI-powered insights and suggestions

## 🚀 Deployment Options

### Local Development
```bash
python main.py
# Access at http://localhost:8000
```

### Docker Deployment
```bash
python scripts/deploy.py docker
# Containerized deployment with docker-compose
```

### VPS Deployment (Future)
```bash
python scripts/deploy.py vps
# Deploy to VPS (Hetzner, DigitalOcean, etc.)
```

### Cloud Deployment (Future)
```bash
python scripts/deploy.py cloud
# Deploy to cloud (AWS, GCP, Azure)
```

## 🔮 Roadmap

### Phase 1: Core Workflows ✅
- [x] Email triage and drafting
- [x] FAQ automation
- [x] Call transcription and summarization

### Phase 2: Enhanced Features
- [ ] Calendar integration and scheduling
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Web dashboard for SMBs

### Phase 3: Scaling
- [ ] Package workflows as installable modules
- [ ] Marketplace for workflow templates
- [ ] Advanced deployment options
- [ ] Enterprise features

### Phase 4: Business Growth
- [ ] Workflow marketplace
- [ ] Custom workflow builder
- [ ] White-label solutions
- [ ] API monetization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join community discussions for questions and ideas

## 🙏 Acknowledgments

- **LangChain** for AI workflow orchestration
- **OpenAI** for powerful language models
- **FastAPI** for modern Python web framework
- **Docker** for containerization
- **Whisper** for audio transcription

