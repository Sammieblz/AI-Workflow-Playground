"""
Enhanced API endpoints for advanced integrations
"""

import os
import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio

# Import our integrations
from integrations.elevenlabs.voice_agent import ElevenLabsVoiceAgent
from integrations.advanced_langchain.ai_agent import AIAgent

logger = logging.getLogger(__name__)

# Create router for enhanced endpoints
router = APIRouter(prefix="/enhanced", tags=["Enhanced Features"])

# Initialize integrations
voice_agent = ElevenLabsVoiceAgent()
ai_agent = AIAgent()

# Pydantic models
class VoiceRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None
    voice_settings: Optional[Dict] = None

class AIAgentRequest(BaseModel):
    message: str
    context: Optional[Dict] = None

class VoiceCloneRequest(BaseModel):
    name: str
    description: str
    files: List[str]

# ElevenLabs Voice Endpoints
@router.post("/voice/synthesize")
async def synthesize_speech(request: VoiceRequest):
    """Synthesize speech using ElevenLabs"""
    try:
        audio_data = await voice_agent.synthesize_speech(
            text=request.text,
            voice_id=request.voice_id
        )
        
        # Save audio file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_file.write(audio_data)
            audio_path = tmp_file.name
        
        return {
            "status": "success",
            "audio_file": audio_path,
            "text": request.text,
            "voice_id": request.voice_id or voice_agent.voice_id
        }
        
    except Exception as e:
        logger.error(f"Voice synthesis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/voice/voices")
async def get_available_voices():
    """Get available ElevenLabs voices"""
    try:
        voices = await voice_agent.get_available_voices()
        return {"status": "success", "voices": voices}
    except Exception as e:
        logger.error(f"Error fetching voices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice/clone")
async def create_voice_clone(request: VoiceCloneRequest):
    """Create a custom voice clone"""
    try:
        voice_id = await voice_agent.create_voice_clone(
            name=request.name,
            description=request.description,
            files=request.files
        )
        return {
            "status": "success",
            "voice_id": voice_id,
            "name": request.name
        }
    except Exception as e:
        logger.error(f"Voice cloning error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice/call-response")
async def generate_call_response(transcription: str, context: str = ""):
    """Generate voice response for call handling"""
    try:
        audio_data = await voice_agent.generate_call_response(transcription, context)
        
        # Save response audio
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_file.write(audio_data)
            audio_path = tmp_file.name
        
        return {
            "status": "success",
            "response_audio": audio_path,
            "transcription": transcription
        }
    except Exception as e:
        logger.error(f"Call response generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Advanced AI Agent Endpoints
@router.post("/ai-agent/chat")
async def chat_with_agent(request: AIAgentRequest):
    """Chat with the advanced AI agent"""
    try:
        result = await ai_agent.process_request(
            user_input=request.message,
            context=request.context
        )
        return {
            "status": "success",
            "response": result["response"],
            "tools_used": result["tools_used"],
            "timestamp": result["timestamp"]
        }
    except Exception as e:
        logger.error(f"AI agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai-agent/history")
async def get_conversation_history():
    """Get conversation history with the AI agent"""
    try:
        history = ai_agent.get_conversation_history()
        return {"status": "success", "history": history}
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/ai-agent/clear")
async def clear_agent_memory():
    """Clear the AI agent's memory"""
    try:
        ai_agent.clear_memory()
        return {"status": "success", "message": "Memory cleared"}
    except Exception as e:
        logger.error(f"Error clearing memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# N8N Integration Endpoints
@router.post("/n8n/email-webhook")
async def n8n_email_webhook(email_data: Dict):
    """Webhook endpoint for N8N email automation"""
    try:
        # Process email data from N8N
        from workflows.email_agent.email_processor import EmailProcessor
        email_processor = EmailProcessor()
        
        # Classify email
        classification = await email_processor._classify_email(email_data)
        
        # Draft reply if needed
        if classification.action_required:
            reply = await email_processor.draft_reply(email_data)
            return {
                "status": "success",
                "classification": classification.dict(),
                "draft_reply": reply
            }
        else:
            return {
                "status": "success",
                "classification": classification.dict(),
                "action_required": False
            }
            
    except Exception as e:
        logger.error(f"N8N email webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/n8n/voice-webhook")
async def n8n_voice_webhook(audio_file: str):
    """Webhook endpoint for N8N voice automation"""
    try:
        # Transcribe audio
        from workflows.call_agent.call_processor import CallProcessor
        call_processor = CallProcessor()
        
        transcription = await call_processor.transcribe_audio(audio_file)
        
        # Generate response
        from workflows.faq_agent.faq_processor import FAQProcessor
        faq_processor = FAQProcessor()
        
        answer = await faq_processor.answer_question(
            transcription.text,
            "Voice call inquiry"
        )
        
        # Synthesize response
        voice_response = await voice_agent.synthesize_speech(answer.answer)
        
        return {
            "status": "success",
            "transcription": transcription.dict(),
            "answer": answer.dict(),
            "voice_response": "Generated"
        }
        
    except Exception as e:
        logger.error(f"N8N voice webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Integration Status Endpoints
@router.get("/status")
async def get_integration_status():
    """Get status of all integrations"""
    try:
        status = {
            "elevenlabs": {
                "configured": bool(voice_agent.api_key),
                "voice_id": voice_agent.voice_id,
                "voice_settings": voice_agent.get_voice_settings()
            },
            "ai_agent": {
                "tools_count": len(ai_agent.tools),
                "memory_size": len(ai_agent.memory.chat_memory.messages),
                "available_tools": [tool.name for tool in ai_agent.tools]
            },
            "n8n": {
                "webhooks_configured": True,
                "workflows": ["email_automation", "voice_automation"]
            }
        }
        
        return {"status": "success", "integrations": status}
        
    except Exception as e:
        logger.error(f"Error getting integration status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
