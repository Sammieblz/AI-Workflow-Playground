"""
ElevenLabs Voice Agent Integration
Handles voice synthesis and call processing
"""

import os
import asyncio
import logging
from typing import Dict, Optional
import requests
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class VoiceSettings(BaseModel):
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True

class ElevenLabsVoiceAgent:
    """ElevenLabs integration for voice synthesis and call handling"""
    
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default voice
        self.voice_settings = VoiceSettings()
        
    async def synthesize_speech(self, text: str, voice_id: Optional[str] = None) -> bytes:
        """Convert text to speech using ElevenLabs"""
        try:
            if not self.api_key:
                raise Exception("ElevenLabs API key not configured")
            
            voice_id = voice_id or self.voice_id
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": self.voice_settings.dict()
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            return response.content
            
        except Exception as e:
            logger.error(f"ElevenLabs synthesis error: {e}")
            raise
    
    async def get_available_voices(self) -> list:
        """Get list of available voices"""
        try:
            url = f"{self.base_url}/voices"
            headers = {"xi-api-key": self.api_key}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json().get("voices", [])
            
        except Exception as e:
            logger.error(f"Error fetching voices: {e}")
            return []
    
    async def create_voice_clone(self, name: str, description: str, files: list) -> str:
        """Create a custom voice clone"""
        try:
            url = f"{self.base_url}/voices/add"
            headers = {"xi-api-key": self.api_key}
            
            data = {
                "name": name,
                "description": description
            }
            
            files_data = []
            for file_path in files:
                with open(file_path, 'rb') as f:
                    files_data.append(('files', f))
            
            response = requests.post(url, data=data, files=files_data, headers=headers)
            response.raise_for_status()
            
            return response.json().get("voice_id")
            
        except Exception as e:
            logger.error(f"Voice cloning error: {e}")
            raise
    
    async def generate_call_response(self, transcription: str, context: str = "") -> bytes:
        """Generate voice response for call handling"""
        try:
            # Use AI to generate appropriate response
            from workflows.faq_agent.faq_processor import FAQProcessor
            faq_processor = FAQProcessor()
            
            # Get AI response
            ai_response = await faq_processor.answer_question(transcription, context)
            
            # Convert to speech
            voice_response = await self.synthesize_speech(ai_response.answer)
            
            return voice_response
            
        except Exception as e:
            logger.error(f"Call response generation error: {e}")
            raise
    
    async def create_voice_memo(self, text: str, filename: str = None) -> str:
        """Create a voice memo file"""
        try:
            audio_data = await self.synthesize_speech(text)
            
            if not filename:
                filename = f"voice_memo_{int(asyncio.get_event_loop().time())}.mp3"
            
            file_path = f"data/audio_files/{filename}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "wb") as f:
                f.write(audio_data)
            
            return file_path
            
        except Exception as e:
            logger.error(f"Voice memo creation error: {e}")
            raise
    
    def get_voice_settings(self) -> Dict:
        """Get current voice settings"""
        return self.voice_settings.dict()
    
    def update_voice_settings(self, **kwargs):
        """Update voice settings"""
        for key, value in kwargs.items():
            if hasattr(self.voice_settings, key):
                setattr(self.voice_settings, key, value)
