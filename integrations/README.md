# 🚀 Advanced Integrations

This directory contains enhanced integrations for the AI Workflow Playground, including n8n workflows, ElevenLabs voice synthesis, and advanced LangChain agents.

## 📁 Directory Structure

```
integrations/
├── n8n_workflows/           # Visual workflow automation
│   ├── email_automation.json
│   └── voice_automation.json
├── elevenlabs/             # Voice synthesis and cloning
│   └── voice_agent.py
├── advanced_langchain/     # Multi-tool AI agents
│   └── ai_agent.py
├── enhanced_api.py         # Enhanced API endpoints
├── setup_guide.md         # Comprehensive setup guide
└── README.md              # This file
```

## 🎯 What's Included

### 1. n8n Workflows
- **Email Automation**: Automated email processing and response
- **Voice Automation**: Voice call handling and response generation
- **Visual Workflow Builder**: Drag-and-drop automation

### 2. ElevenLabs Integration
- **Voice Synthesis**: Convert text to natural speech
- **Voice Cloning**: Create custom business voices
- **Call Response**: Generate voice responses for calls

### 3. Advanced LangChain
- **Multi-Tool Agents**: AI agents with multiple capabilities
- **Memory Management**: Conversation context and history
- **Tool Integration**: Email, calendar, task management

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
# Run the advanced deployment script
python scripts/deploy_advanced.py setup

# Start all services
./start_advanced.sh
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Start services
python main.py                    # AI Workflow API
docker-compose -f n8n-docker-compose.yml up  # n8n
```

## 🔧 Configuration

### Required API Keys
```bash
# Add to your .env file
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=your_voice_id
```

### n8n Configuration
- **URL**: http://localhost:5678
- **Username**: admin
- **Password**: password

### Enhanced API Endpoints
- **Base URL**: http://localhost:8000/enhanced/
- **Status**: http://localhost:8000/enhanced/status

## 📊 Workflow Examples

### Email Automation
1. **Trigger**: IMAP email check
2. **Process**: AI classification
3. **Action**: Draft replies
4. **Notification**: Slack alerts

### Voice Automation
1. **Trigger**: Audio webhook
2. **Process**: Speech transcription
3. **Generate**: AI response
4. **Synthesize**: Voice response
5. **Return**: Audio file

## 🎙️ Voice Features

### Voice Synthesis
```python
# Basic synthesis
audio = await voice_agent.synthesize_speech(
    text="Hello, how can I help you?",
    voice_id="21m00Tcm4TlvDq8ikWAM"
)
```

### Voice Cloning
```python
# Create custom voice
voice_id = await voice_agent.create_voice_clone(
    name="Business Voice",
    description="Professional voice for business",
    files=["sample1.wav", "sample2.wav"]
)
```

## 🤖 AI Agent Features

### Multi-Tool Capabilities
- **Email Management**: Send and draft emails
- **Calendar Integration**: Schedule meetings
- **Task Creation**: Create and manage tasks
- **Sentiment Analysis**: Analyze text sentiment
- **Knowledge Search**: Search business knowledge

### Example Usage
```python
# Chat with AI agent
response = await ai_agent.process_request(
    message="Schedule a meeting with John tomorrow at 2 PM",
    context={"user": "admin", "business": "consulting"}
)
```

## 🔗 API Endpoints

### Voice Endpoints
- `POST /enhanced/voice/synthesize` - Text to speech
- `GET /enhanced/voice/voices` - Available voices
- `POST /enhanced/voice/clone` - Create voice clone
- `POST /enhanced/voice/call-response` - Generate call response

### AI Agent Endpoints
- `POST /enhanced/ai-agent/chat` - Chat with agent
- `GET /enhanced/ai-agent/history` - Conversation history
- `DELETE /enhanced/ai-agent/clear` - Clear memory

### n8n Webhooks
- `POST /enhanced/n8n/email-webhook` - Email automation
- `POST /enhanced/n8n/voice-webhook` - Voice automation

## 🧪 Testing

### Test Voice Synthesis
```bash
curl -X POST http://localhost:8000/enhanced/voice/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test of the voice system."}'
```

### Test AI Agent
```bash
curl -X POST http://localhost:8000/enhanced/ai-agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me schedule a meeting"}'
```

### Check Integration Status
```bash
curl http://localhost:8000/enhanced/status
```

## 🏢 Business Use Cases

### 1. Automated Customer Service
- **Input**: Customer calls or emails
- **Process**: AI transcribes and understands
- **Output**: Professional voice/email responses

### 2. Meeting Management
- **Input**: "Schedule a meeting with John tomorrow"
- **Process**: AI agent creates calendar event
- **Output**: Meeting scheduled with confirmation

### 3. Voice Branding
- **Input**: Custom voice samples
- **Process**: ElevenLabs voice cloning
- **Output**: Your business's unique AI voice

### 4. Task Automation
- **Input**: "Create a task to follow up with client"
- **Process**: AI agent creates task with details
- **Output**: Task created in your system

## 🚀 Deployment Options

### Local Development
```bash
python main.py                    # AI Workflow API
docker-compose -f n8n-docker-compose.yml up  # n8n
```

### Docker Deployment
```bash
python scripts/deploy_advanced.py docker
```

### Production Deployment
- Deploy to VPS or cloud
- Configure proper authentication
- Set up monitoring and logging

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

## 📚 Documentation

- **Setup Guide**: `integrations/setup_guide.md`
- **API Documentation**: http://localhost:8000/docs
- **n8n Documentation**: https://docs.n8n.io
- **ElevenLabs Documentation**: https://docs.elevenlabs.io

This integration setup gives you a powerful, scalable AI automation platform that can grow with your business!
