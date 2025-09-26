# Advanced Integrations Setup Guide

This guide shows you how to integrate your AI Workflow Playground with powerful tools like n8n, ElevenLabs, and advanced LangChain features.

## 🎯 Overview

- **n8n**: Visual workflow automation platform
- **ElevenLabs**: AI voice synthesis and cloning
- **Advanced LangChain**: Multi-tool AI agents with memory

## 🔧 Prerequisites

### Required API Keys
```bash
# Add to your .env file
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=your_preferred_voice_id
```

### Required Software
- Docker (for n8n)
- Python 3.11+
- Node.js (for n8n)

## 🚀 Setup Instructions

### 1. ElevenLabs Integration

#### Get ElevenLabs API Key
1. Go to [ElevenLabs](https://elevenlabs.io)
2. Sign up for an account
3. Get your API key from the dashboard
4. Choose a voice ID (or use the default)

#### Configure Voice Settings
```python
# In your .env file
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Default voice
```

#### Test ElevenLabs Integration
```bash
# Test voice synthesis
curl -X POST http://localhost:8000/enhanced/voice/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test of the voice synthesis system."}'
```

### 2. n8n Setup

#### Install n8n with Docker
```bash
# Create n8n directory
mkdir n8n-data
cd n8n-data

# Run n8n with Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

#### Access n8n Interface
1. Open http://localhost:5678
2. Create your first workflow
3. Import the provided workflow JSON files

#### Import Workflows
```bash
# Copy workflow files to n8n
cp integrations/n8n_workflows/*.json ~/.n8n/workflows/

# Or import manually through the n8n interface
```

### 3. Advanced LangChain Setup

#### Install Additional Dependencies
```bash
pip install langchain-openai langchain-community
```

#### Configure AI Agent
```python
# The AI agent is automatically configured with:
# - Email sending tools
# - Meeting scheduling tools
# - Task creation tools
# - Sentiment analysis tools
# - Knowledge base search
```

## 🔄 Workflow Examples

### Email Automation with n8n

1. **Trigger**: IMAP email check every minute
2. **Process**: Send to AI for classification
3. **Action**: Draft replies for urgent emails
4. **Notification**: Slack alerts for urgent items

```json
{
  "workflow": "email_automation",
  "steps": [
    "Check IMAP inbox",
    "Classify emails with AI",
    "Draft replies for urgent emails",
    "Send Slack notifications"
  ]
}
```

### Voice Automation with n8n

1. **Trigger**: Webhook receives audio file
2. **Process**: Transcribe with Whisper
3. **Generate**: AI response using FAQ system
4. **Synthesize**: Convert response to speech
5. **Return**: Audio response to caller

```json
{
  "workflow": "voice_automation",
  "steps": [
    "Receive audio webhook",
    "Transcribe with AI",
    "Generate response",
    "Synthesize voice",
    "Return audio response"
  ]
}
```

## 🎙️ Voice Features

### Voice Synthesis
```python
# Basic voice synthesis
response = await voice_agent.synthesize_speech(
    text="Hello, how can I help you today?",
    voice_id="21m00Tcm4TlvDq8ikWAM"
)
```

### Voice Cloning
```python
# Create custom voice
voice_id = await voice_agent.create_voice_clone(
    name="Business Voice",
    description="Professional business voice",
    files=["sample1.wav", "sample2.wav"]
)
```

### Call Response Generation
```python
# Generate voice response for calls
response = await voice_agent.generate_call_response(
    transcription="What are your business hours?",
    context="Customer inquiry"
)
```

## 🤖 Advanced AI Agent

### Multi-Tool Capabilities
The AI agent can:
- Send emails automatically
- Schedule meetings
- Create tasks
- Analyze sentiment
- Search knowledge base
- Remember conversation context

### Example Usage
```python
# Chat with the AI agent
response = await ai_agent.process_request(
    message="Schedule a meeting with John for tomorrow at 2 PM",
    context={"user": "admin", "business": "consulting"}
)
```

### Available Tools
1. **search_knowledge_base**: Search FAQ and business info
2. **send_email**: Send emails to customers
3. **schedule_meeting**: Book meetings with attendees
4. **create_task**: Create and manage tasks
5. **analyze_sentiment**: Analyze text sentiment

## 🔗 API Endpoints

### Enhanced Endpoints
- `POST /enhanced/voice/synthesize` - Voice synthesis
- `GET /enhanced/voice/voices` - Available voices
- `POST /enhanced/voice/clone` - Create voice clone
- `POST /enhanced/ai-agent/chat` - Chat with AI agent
- `GET /enhanced/ai-agent/history` - Conversation history
- `POST /enhanced/n8n/email-webhook` - N8N email webhook
- `POST /enhanced/n8n/voice-webhook` - N8N voice webhook

### Testing Endpoints
```bash
# Test voice synthesis
curl -X POST http://localhost:8000/enhanced/voice/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'

# Test AI agent
curl -X POST http://localhost:8000/enhanced/ai-agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me schedule a meeting"}'

# Check integration status
curl http://localhost:8000/enhanced/status
```

## 🏢 Business Use Cases

### 1. Automated Customer Service
- **Input**: Customer calls or emails
- **Process**: AI transcribes, understands, and responds
- **Output**: Professional voice/email responses

### 2. Meeting Management
- **Input**: "Schedule a meeting with John tomorrow"
- **Process**: AI agent creates calendar event
- **Output**: Meeting scheduled with confirmation

### 3. Task Automation
- **Input**: "Create a task to follow up with client"
- **Process**: AI agent creates task with details
- **Output**: Task created in your system

### 4. Voice Branding
- **Input**: Custom voice samples
- **Process**: ElevenLabs voice cloning
- **Output**: Your business's unique AI voice

## 🚀 Deployment Options

### Local Development
```bash
# Start all services
python main.py                    # AI Workflow API
docker run n8nio/n8n            # n8n workflows
# ElevenLabs API (cloud-based)
```

### Docker Compose (Recommended)
```yaml
# Add to docker-compose.yml
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
```

### Cloud Deployment
- **ElevenLabs**: Cloud-based API
- **n8n**: Deploy to VPS or cloud
- **AI Workflows**: Deploy to your preferred cloud provider

## 🔧 Troubleshooting

### Common Issues

1. **ElevenLabs API Errors**
   - Check API key configuration
   - Verify voice ID exists
   - Check API quota limits

2. **n8n Connection Issues**
   - Verify webhook URLs
   - Check firewall settings
   - Test individual nodes

3. **AI Agent Memory Issues**
   - Clear memory if needed
   - Check conversation history
   - Restart agent if stuck

### Debug Commands
```bash
# Check integration status
curl http://localhost:8000/enhanced/status

# Test voice synthesis
python -c "from integrations.elevenlabs.voice_agent import ElevenLabsVoiceAgent; print('Voice agent loaded')"

# Test AI agent
python -c "from integrations.advanced_langchain.ai_agent import AIAgent; print('AI agent loaded')"
```

## 📈 Scaling Considerations

### Performance
- Use connection pooling for APIs
- Implement caching for voice synthesis
- Monitor API rate limits

### Cost Management
- ElevenLabs: Pay per character
- OpenAI: Pay per token
- Monitor usage and set limits

### Security
- Secure API keys
- Use environment variables
- Implement proper authentication

## 🎯 Next Steps

1. **Start Simple**: Begin with basic voice synthesis
2. **Add Workflows**: Import n8n workflows
3. **Customize**: Adapt to your business needs
4. **Scale**: Deploy to production
5. **Monitor**: Track usage and performance

This integration setup gives you a powerful, scalable AI automation platform that can grow with your business!
