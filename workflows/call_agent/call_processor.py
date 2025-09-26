"""
Call Agent - Transcribes and summarizes phone calls
"""

import os
import logging
import tempfile
from typing import Dict, List, Optional
from datetime import datetime

import whisper
from pydub import AudioSegment
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class CallTranscription(BaseModel):
    text: str
    confidence: float
    language: str
    duration: float

class CallSummary(BaseModel):
    summary: str
    key_points: List[str]
    action_items: List[str]
    sentiment: str
    duration: float

class CallProcessor:
    """Processes audio calls for transcription and summarization"""
    
    def __init__(self):
        self.llm = OpenAI(temperature=0.3)
        self.whisper_model = None
        self.setup_prompts()
        self.load_whisper_model()
        
    def setup_prompts(self):
        """Initialize LangChain prompts for call processing"""
        
        # Call summarization prompt
        self.summary_prompt = PromptTemplate(
            input_variables=["transcription", "call_type", "business_context"],
            template="""
            Analyze this phone call transcription and provide a comprehensive summary.
            
            Transcription: {transcription}
            Call Type: {call_type}
            Business Context: {business_context}
            
            Please provide:
            1. A brief summary of the call
            2. Key points discussed
            3. Any action items or next steps
            4. Overall sentiment of the call (positive, negative, neutral)
            
            Format your response as JSON:
            {{
                "summary": "Brief summary of the call",
                "key_points": ["point1", "point2", "point3"],
                "action_items": ["action1", "action2"],
                "sentiment": "positive/negative/neutral"
            }}
            """
        )
        
        # Call classification prompt
        self.classification_prompt = PromptTemplate(
            input_variables=["transcription"],
            template="""
            Classify this phone call into one of these categories:
            - customer_support: Customer needs help or has issues
            - sales_inquiry: Potential customer interested in products/services
            - complaint: Customer complaint or dissatisfaction
            - appointment: Scheduling or appointment-related
            - general: General inquiry or other
            
            Transcription: {transcription}
            
            Respond with just the category name:
            """
        )
    
    def load_whisper_model(self):
        """Load Whisper model for transcription"""
        try:
            # Use base model for faster processing, can upgrade to larger models
            self.whisper_model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            self.whisper_model = None
    
    async def transcribe_audio(self, audio_file_path: str) -> CallTranscription:
        """Transcribe audio file to text"""
        try:
            if not self.whisper_model:
                raise Exception("Whisper model not loaded")
            
            # Check if file exists
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            # Convert audio to the right format if needed
            processed_audio_path = await self._preprocess_audio(audio_file_path)
            
            # Transcribe using Whisper
            result = self.whisper_model.transcribe(processed_audio_path)
            
            # Get audio duration
            audio = AudioSegment.from_file(processed_audio_path)
            duration = len(audio) / 1000.0  # Convert to seconds
            
            # Clean up temporary file if created
            if processed_audio_path != audio_file_path:
                os.remove(processed_audio_path)
            
            return CallTranscription(
                text=result["text"].strip(),
                confidence=result.get("confidence", 0.8),
                language=result.get("language", "en"),
                duration=duration
            )
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise
    
    async def summarize_call(self, audio_file_path: str) -> CallSummary:
        """Summarize a call from audio file"""
        try:
            # First transcribe the audio
            transcription = await self.transcribe_audio(audio_file_path)
            
            # Then summarize the transcription
            return await self._summarize_transcription(transcription.text)
            
        except Exception as e:
            logger.error(f"Call summarization error: {e}")
            raise
    
    async def _summarize_transcription(self, transcription_text: str) -> CallSummary:
        """Summarize a call transcription"""
        try:
            # Classify the call type
            call_type = await self._classify_call(transcription_text)
            
            # Get business context
            business_context = self._get_business_context()
            
            # Create summary chain
            summary_chain = self.summary_prompt | self.llm
            
            # Generate summary
            result = await summary_chain.ainvoke({
                "transcription": transcription_text,
                "call_type": call_type,
                "business_context": business_context
            })
            
            # Parse JSON response
            import json
            summary_data = json.loads(result.strip())
            
            return CallSummary(
                summary=summary_data["summary"],
                key_points=summary_data["key_points"],
                action_items=summary_data["action_items"],
                sentiment=summary_data["sentiment"],
                duration=0.0  # Will be filled by caller
            )
            
        except Exception as e:
            logger.error(f"Transcription summarization error: {e}")
            # Return basic summary
            return CallSummary(
                summary="Call transcription completed but summarization failed.",
                key_points=["Transcription available for manual review"],
                action_items=["Review transcription manually"],
                sentiment="neutral",
                duration=0.0
            )
    
    async def _classify_call(self, transcription: str) -> str:
        """Classify the type of call"""
        try:
            classification_chain = self.classification_prompt | self.llm
            result = await classification_chain.ainvoke({"transcription": transcription})
            return result.strip().lower()
        except Exception as e:
            logger.error(f"Call classification error: {e}")
            return "general"
    
    def _get_business_context(self) -> str:
        """Get business context for call analysis"""
        return """
        We are a small business focused on customer service excellence.
        We handle customer support, sales inquiries, and general business questions.
        Our goal is to provide helpful, professional service to all callers.
        """
    
    async def _preprocess_audio(self, audio_file_path: str) -> str:
        """Preprocess audio file for Whisper"""
        try:
            # Load audio file
            audio = AudioSegment.from_file(audio_file_path)
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Convert to 16kHz sample rate (Whisper's preferred rate)
            if audio.frame_rate != 16000:
                audio = audio.set_frame_rate(16000)
            
            # Check if conversion is needed
            if (audio.channels == 1 and audio.frame_rate == 16000 and 
                audio_file_path.endswith('.wav')):
                return audio_file_path
            
            # Create temporary file for converted audio
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_path = temp_file.name
            temp_file.close()
            
            # Export converted audio
            audio.export(temp_path, format="wav")
            
            return temp_path
            
        except Exception as e:
            logger.error(f"Audio preprocessing error: {e}")
            return audio_file_path  # Return original if preprocessing fails
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported audio formats"""
        return ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.mp4']
    
    def validate_audio_file(self, file_path: str) -> bool:
        """Validate if audio file is supported"""
        if not os.path.exists(file_path):
            return False
        
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in self.get_supported_formats()
    
    async def process_call_batch(self, audio_files: List[str]) -> List[Dict]:
        """Process multiple audio files in batch"""
        results = []
        
        for audio_file in audio_files:
            try:
                if not self.validate_audio_file(audio_file):
                    results.append({
                        "file": audio_file,
                        "status": "error",
                        "message": "Unsupported audio format"
                    })
                    continue
                
                # Transcribe and summarize
                transcription = await self.transcribe_audio(audio_file)
                summary = await self._summarize_transcription(transcription.text)
                
                results.append({
                    "file": audio_file,
                    "status": "success",
                    "transcription": transcription.dict(),
                    "summary": summary.dict()
                })
                
            except Exception as e:
                logger.error(f"Error processing {audio_file}: {e}")
                results.append({
                    "file": audio_file,
                    "status": "error",
                    "message": str(e)
                })
        
        return results
