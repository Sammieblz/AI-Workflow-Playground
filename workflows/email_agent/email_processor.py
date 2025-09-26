"""
Email Agent - Handles email triage and drafting
"""

import asyncio
import imaplib
import email
import json
import logging
import os
from typing import Dict, List, Optional
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class EmailClassification(BaseModel):
    category: str  # "support", "sales", "spam", "urgent"
    priority: int  # 1-5 scale
    sentiment: str  # "positive", "negative", "neutral"
    action_required: bool
    suggested_response: str

class EmailProcessor:
    """Processes emails using AI for classification and drafting responses"""
    
    def __init__(self):
        self.llm = OpenAI(temperature=0.3)
        self.setup_prompts()
        
    def setup_prompts(self):
        """Initialize LangChain prompts for email processing"""
        
        # Email classification prompt
        self.classification_prompt = PromptTemplate(
            input_variables=["email_subject", "email_body", "sender"],
            template="""
            Analyze this email and classify it:
            
            From: {sender}
            Subject: {email_subject}
            Body: {email_body}
            
            Classify the email into one of these categories:
            - support: Customer needs help with a product/service
            - sales: Potential customer inquiry or sales opportunity
            - spam: Unwanted or promotional content
            - urgent: Requires immediate attention
            
            Also determine:
            - Priority level (1-5, where 5 is most urgent)
            - Sentiment (positive, negative, neutral)
            - Whether action is required (true/false)
            - Brief suggested response
            
            Respond in JSON format:
            {{
                "category": "category_name",
                "priority": priority_number,
                "sentiment": "sentiment",
                "action_required": true/false,
                "suggested_response": "brief response suggestion"
            }}
            """
        )
        
        # Email reply drafting prompt
        self.reply_prompt = PromptTemplate(
            input_variables=["original_email", "classification", "business_context"],
            template="""
            Draft a professional email reply based on this information:
            
            Original Email: {original_email}
            Classification: {classification}
            Business Context: {business_context}
            
            Guidelines:
            - Be professional and helpful
            - Address the customer's specific needs
            - Keep it concise but complete
            - Use appropriate tone based on sentiment
            - Include next steps if needed
            
            Draft the reply:
            """
        )
    
    async def process_emails(self) -> Dict:
        """Process new emails from the inbox"""
        try:
            # Connect to email server
            mail = imaplib.IMAP4_SSL(
                os.getenv("EMAIL_HOST"),
                int(os.getenv("EMAIL_PORT", 993))
            )
            mail.login(
                os.getenv("EMAIL_USERNAME"),
                os.getenv("EMAIL_PASSWORD")
            )
            mail.select("INBOX")
            
            # Search for unread emails
            status, messages = mail.search(None, "UNSEEN")
            email_ids = messages[0].split()
            
            processed_emails = []
            
            for email_id in email_ids[:int(os.getenv("MAX_EMAILS_PER_BATCH", 10))]:
                try:
                    # Fetch email
                    status, msg_data = mail.fetch(email_id, "(RFC822)")
                    raw_email = msg_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    
                    # Extract email data
                    email_data = self._extract_email_data(email_message)
                    
                    # Classify email
                    classification = await self._classify_email(email_data)
                    
                    # Store processed email
                    processed_email = {
                        "id": email_id.decode(),
                        "data": email_data,
                        "classification": classification.dict(),
                        "processed_at": datetime.now().isoformat()
                    }
                    
                    processed_emails.append(processed_email)
                    
                except Exception as e:
                    logger.error(f"Error processing email {email_id}: {e}")
                    continue
            
            mail.close()
            mail.logout()
            
            return {
                "count": len(processed_emails),
                "emails": processed_emails
            }
            
        except Exception as e:
            logger.error(f"Email processing error: {e}")
            raise
    
    def _extract_email_data(self, email_message) -> Dict:
        """Extract relevant data from email message"""
        return {
            "sender": email_message.get("From", ""),
            "subject": email_message.get("Subject", ""),
            "date": email_message.get("Date", ""),
            "body": self._get_email_body(email_message),
            "to": email_message.get("To", ""),
            "cc": email_message.get("Cc", "")
        }
    
    def _get_email_body(self, email_message) -> str:
        """Extract text body from email message"""
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            if email_message.get_content_type() == "text/plain":
                body = email_message.get_payload(decode=True).decode()
        
        return body
    
    async def _classify_email(self, email_data: Dict) -> EmailClassification:
        """Classify email using AI"""
        try:
            # Create classification chain
            classification_chain = self.classification_prompt | self.llm
            
            # Get classification
            result = await classification_chain.ainvoke({
                "email_subject": email_data["subject"],
                "email_body": email_data["body"],
                "sender": email_data["sender"]
            })
            
            # Parse JSON response
            classification_data = json.loads(result.strip())
            
            return EmailClassification(**classification_data)
            
        except Exception as e:
            logger.error(f"Email classification error: {e}")
            # Return default classification
            return EmailClassification(
                category="support",
                priority=3,
                sentiment="neutral",
                action_required=True,
                suggested_response="Please review this email manually."
            )
    
    async def draft_reply(self, email_data: Dict) -> str:
        """Draft a reply to an email"""
        try:
            # Get classification first
            classification = await self._classify_email(email_data)
            
            # Create reply chain
            reply_chain = self.reply_prompt | self.llm
            
            # Get business context (you can customize this)
            business_context = """
            You are a helpful customer service representative for a small business.
            Be professional, friendly, and solution-oriented.
            If you cannot fully answer a question, offer to connect them with a human representative.
            """
            
            # Draft reply
            reply = await reply_chain.ainvoke({
                "original_email": f"From: {email_data['sender']}\nSubject: {email_data['subject']}\n\n{email_data['body']}",
                "classification": classification.dict(),
                "business_context": business_context
            })
            
            return reply.strip()
            
        except Exception as e:
            logger.error(f"Reply drafting error: {e}")
            return "I apologize, but I'm having trouble drafting a response. Please review this email manually."
    
    async def send_reply(self, to_email: str, subject: str, body: str) -> bool:
        """Send a reply email (requires SMTP configuration)"""
        try:
            # This would require SMTP configuration
            # For now, just return the draft
            logger.info(f"Reply drafted for {to_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending reply: {e}")
            return False