"""
FAQ Agent - Answers customer questions using knowledge base
"""

import json
import logging
import os
from typing import Dict, List, Optional
from datetime import datetime

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class FAQResponse(BaseModel):
    answer: str
    confidence: float
    source: str
    related_questions: List[str]

class FAQProcessor:
    """Processes customer questions using FAQ knowledge base"""
    
    def __init__(self):
        self.llm = OpenAI(temperature=0.3)
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.setup_prompts()
        self.load_knowledge_base()
        
    def setup_prompts(self):
        """Initialize LangChain prompts for FAQ processing"""
        
        # FAQ answer prompt
        self.faq_prompt = PromptTemplate(
            input_variables=["question", "context", "business_info"],
            template="""
            You are a helpful customer service representative. Answer this customer question based on the provided context and business information.
            
            Customer Question: {question}
            
            Relevant Context: {context}
            
            Business Information: {business_info}
            
            Guidelines:
            - Provide a clear, helpful answer
            - If you cannot find the answer in the context, say so politely
            - Be professional and friendly
            - Include relevant details but keep it concise
            - If appropriate, suggest next steps or additional resources
            
            Answer:
            """
        )
        
        # Question classification prompt
        self.classification_prompt = PromptTemplate(
            input_variables=["question"],
            template="""
            Classify this customer question into one of these categories:
            - product_info: Questions about products or services
            - support: Technical support or troubleshooting
            - billing: Questions about pricing, payments, or billing
            - general: General inquiries or other questions
            
            Question: {question}
            
            Respond with just the category name:
            """
        )
    
    def load_knowledge_base(self):
        """Load FAQ knowledge base from files"""
        try:
            # Create knowledge base directory if it doesn't exist
            kb_dir = "data/knowledge_base"
            os.makedirs(kb_dir, exist_ok=True)
            
            # Load FAQ documents
            documents = []
            faq_files = [
                "data/knowledge_base/faq.txt",
                "data/knowledge_base/products.txt",
                "data/knowledge_base/support.txt"
            ]
            
            for file_path in faq_files:
                if os.path.exists(file_path):
                    try:
                        loader = TextLoader(file_path)
                        docs = loader.load()
                        documents.extend(docs)
                    except Exception as e:
                        logger.warning(f"Could not load {file_path}: {e}")
            
            if documents:
                # Split documents into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                splits = text_splitter.split_documents(documents)
                
                # Create vector store
                self.vectorstore = FAISS.from_documents(splits, self.embeddings)
                logger.info(f"Loaded {len(splits)} document chunks into knowledge base")
            else:
                logger.warning("No FAQ documents found. Creating empty knowledge base.")
                self.vectorstore = None
                
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            self.vectorstore = None
    
    async def answer_question(self, question: str, context: str = "") -> FAQResponse:
        """Answer a customer question using the knowledge base"""
        try:
            # Classify the question
            question_type = await self._classify_question(question)
            
            # Get relevant context from knowledge base
            relevant_context = await self._get_relevant_context(question)
            
            # Combine contexts
            full_context = f"{context}\n\n{relevant_context}" if context else relevant_context
            
            # Get business information
            business_info = self._get_business_info()
            
            # Create answer chain
            answer_chain = self.faq_prompt | self.llm
            
            # Generate answer
            answer = await answer_chain.ainvoke({
                "question": question,
                "context": full_context,
                "business_info": business_info
            })
            
            # Calculate confidence based on context relevance
            confidence = self._calculate_confidence(question, relevant_context)
            
            # Get related questions
            related_questions = await self._get_related_questions(question)
            
            return FAQResponse(
                answer=answer.strip(),
                confidence=confidence,
                source="knowledge_base",
                related_questions=related_questions
            )
            
        except Exception as e:
            logger.error(f"FAQ processing error: {e}")
            return FAQResponse(
                answer="I apologize, but I'm having trouble processing your question. Please contact our support team for assistance.",
                confidence=0.0,
                source="error",
                related_questions=[]
            )
    
    async def _classify_question(self, question: str) -> str:
        """Classify the type of question"""
        try:
            classification_chain = self.classification_prompt | self.llm
            result = await classification_chain.ainvoke({"question": question})
            return result.strip().lower()
        except Exception as e:
            logger.error(f"Question classification error: {e}")
            return "general"
    
    async def _get_relevant_context(self, question: str) -> str:
        """Get relevant context from knowledge base"""
        if not self.vectorstore:
            return "No knowledge base available."
        
        try:
            # Search for similar documents
            docs = self.vectorstore.similarity_search(question, k=3)
            
            # Combine relevant documents
            context_parts = []
            for doc in docs:
                context_parts.append(doc.page_content)
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Context retrieval error: {e}")
            return "Error retrieving relevant information."
    
    def _get_business_info(self) -> str:
        """Get business information for context"""
        return """
        We are a small business focused on providing excellent customer service.
        Our business hours are Monday-Friday 9AM-5PM.
        We aim to respond to all inquiries within 24 hours.
        For urgent matters, please call our support line.
        """
    
    def _calculate_confidence(self, question: str, context: str) -> float:
        """Calculate confidence score for the answer"""
        if not context or context == "No knowledge base available.":
            return 0.3
        
        # Simple confidence calculation based on context length and relevance
        context_length = len(context.split())
        question_length = len(question.split())
        
        # Higher confidence for longer, more detailed context
        base_confidence = min(0.9, 0.5 + (context_length / 1000) * 0.4)
        
        # Adjust based on question complexity
        if question_length > 10:
            base_confidence *= 0.9  # Slightly lower for complex questions
        
        return round(base_confidence, 2)
    
    async def _get_related_questions(self, question: str) -> List[str]:
        """Get related questions from knowledge base"""
        if not self.vectorstore:
            return []
        
        try:
            # Find similar questions
            docs = self.vectorstore.similarity_search(question, k=5)
            
            # Extract potential questions (simple heuristic)
            related = []
            for doc in docs:
                # Look for question patterns in the content
                content = doc.page_content
                if "?" in content:
                    # Extract sentences with questions
                    sentences = content.split(".")
                    for sentence in sentences:
                        if "?" in sentence and len(sentence.strip()) > 10:
                            related.append(sentence.strip())
                            if len(related) >= 3:
                                break
            
            return related[:3]  # Return up to 3 related questions
            
        except Exception as e:
            logger.error(f"Related questions error: {e}")
            return []
    
    def add_faq_entry(self, question: str, answer: str, category: str = "general"):
        """Add a new FAQ entry to the knowledge base"""
        try:
            # Create FAQ entry
            faq_entry = f"Q: {question}\nA: {answer}\nCategory: {category}\n\n"
            
            # Append to FAQ file
            faq_file = "data/knowledge_base/faq.txt"
            os.makedirs(os.path.dirname(faq_file), exist_ok=True)
            
            with open(faq_file, "a", encoding="utf-8") as f:
                f.write(faq_entry)
            
            # Reload knowledge base
            self.load_knowledge_base()
            
            logger.info(f"Added FAQ entry: {question}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding FAQ entry: {e}")
            return False
    
    def get_knowledge_base_stats(self) -> Dict:
        """Get statistics about the knowledge base"""
        try:
            if not self.vectorstore:
                return {"status": "empty", "documents": 0}
            
            # Get document count
            doc_count = self.vectorstore.index.ntotal if hasattr(self.vectorstore.index, 'ntotal') else 0
            
            return {
                "status": "loaded",
                "documents": doc_count,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting knowledge base stats: {e}")
            return {"status": "error", "documents": 0}
