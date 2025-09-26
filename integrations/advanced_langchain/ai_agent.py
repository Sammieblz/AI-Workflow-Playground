"""
Advanced LangChain AI Agent with Tools and Memory
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.agents import tool
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class AIAgent:
    """Advanced AI Agent with tools, memory, and multi-step reasoning"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.3,
            streaming=True
        )
        self.memory = ConversationBufferWindowMemory(
            k=10,  # Keep last 10 interactions
            return_messages=True
        )
        self.tools = self._create_tools()
        self.agent = self._create_agent()
        
    def _create_tools(self) -> List[Tool]:
        """Create tools for the AI agent"""
        
        @tool
        def search_knowledge_base(query: str) -> str:
            """Search the knowledge base for relevant information"""
            try:
                from workflows.faq_agent.faq_processor import FAQProcessor
                faq_processor = FAQProcessor()
                # This would need to be async in real implementation
                return "Knowledge base search functionality"
            except Exception as e:
                return f"Error searching knowledge base: {e}"
        
        @tool
        def send_email(to: str, subject: str, body: str) -> str:
            """Send an email to a recipient"""
            try:
                # This would integrate with your email system
                logger.info(f"Email sent to {to}: {subject}")
                return f"Email sent successfully to {to}"
            except Exception as e:
                return f"Error sending email: {e}"
        
        @tool
        def schedule_meeting(title: str, date: str, time: str, attendees: List[str]) -> str:
            """Schedule a meeting with attendees"""
            try:
                # This would integrate with calendar systems
                logger.info(f"Meeting scheduled: {title} on {date} at {time}")
                return f"Meeting '{title}' scheduled for {date} at {time}"
            except Exception as e:
                return f"Error scheduling meeting: {e}"
        
        @tool
        def create_task(title: str, description: str, priority: str = "medium") -> str:
            """Create a new task"""
            try:
                # This would integrate with task management systems
                logger.info(f"Task created: {title} (Priority: {priority})")
                return f"Task '{title}' created with priority {priority}"
            except Exception as e:
                return f"Error creating task: {e}"
        
        @tool
        def analyze_sentiment(text: str) -> str:
            """Analyze the sentiment of text"""
            try:
                # Simple sentiment analysis
                positive_words = ["good", "great", "excellent", "amazing", "wonderful"]
                negative_words = ["bad", "terrible", "awful", "horrible", "disappointing"]
                
                text_lower = text.lower()
                positive_count = sum(1 for word in positive_words if word in text_lower)
                negative_count = sum(1 for word in negative_words if word in text_lower)
                
                if positive_count > negative_count:
                    return "positive"
                elif negative_count > positive_count:
                    return "negative"
                else:
                    return "neutral"
            except Exception as e:
                return f"Error analyzing sentiment: {e}"
        
        return [
            Tool(name="search_knowledge_base", func=search_knowledge_base, 
                 description="Search the knowledge base for relevant information"),
            Tool(name="send_email", func=send_email,
                 description="Send an email to a recipient"),
            Tool(name="schedule_meeting", func=schedule_meeting,
                 description="Schedule a meeting with attendees"),
            Tool(name="create_task", func=create_task,
                 description="Create a new task with title, description, and priority"),
            Tool(name="analyze_sentiment", func=analyze_sentiment,
                 description="Analyze the sentiment of text")
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """Create the AI agent with tools and memory"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an advanced AI assistant for business automation. 
            You have access to various tools to help with:
            - Searching knowledge bases
            - Sending emails
            - Scheduling meetings
            - Creating tasks
            - Analyzing sentiment
            
            Always be helpful, professional, and efficient. Use the available tools when appropriate.
            If you're unsure about something, ask for clarification."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    async def process_request(self, user_input: str, context: Dict = None) -> Dict:
        """Process a user request with the AI agent"""
        try:
            # Add context to the input if provided
            if context:
                enhanced_input = f"Context: {context}\n\nUser Request: {user_input}"
            else:
                enhanced_input = user_input
            
            # Process with the agent
            result = await self.agent.ainvoke({
                "input": enhanced_input,
                "chat_history": self.memory.chat_memory.messages
            })
            
            return {
                "response": result["output"],
                "tools_used": self._extract_tools_used(result),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Agent processing error: {e}")
            return {
                "response": f"I apologize, but I encountered an error: {e}",
                "tools_used": [],
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_tools_used(self, result: Dict) -> List[str]:
        """Extract which tools were used in the response"""
        # This is a simplified extraction - in practice, you'd parse the agent's execution
        tools_used = []
        if "email" in result.get("output", "").lower():
            tools_used.append("send_email")
        if "meeting" in result.get("output", "").lower():
            tools_used.append("schedule_meeting")
        if "task" in result.get("output", "").lower():
            tools_used.append("create_task")
        return tools_used
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        messages = self.memory.chat_memory.messages
        return [
            {
                "type": "human" if isinstance(msg, HumanMessage) else "ai",
                "content": msg.content,
                "timestamp": datetime.now().isoformat()
            }
            for msg in messages
        ]
    
    def clear_memory(self):
        """Clear the conversation memory"""
        self.memory.clear()
    
    def add_custom_tool(self, name: str, func, description: str):
        """Add a custom tool to the agent"""
        custom_tool = Tool(name=name, func=func, description=description)
        self.tools.append(custom_tool)
        # Recreate agent with new tools
        self.agent = self._create_agent()
