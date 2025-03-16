import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import streamlit as st

class GeminiModelHandler:
    """
    Handler for interacting with the Gemini 1.5 Pro model through LangChain
    """
    
    def __init__(self):
        """Initialize the Gemini model handler"""
        self._initialize_api()
        self._initialize_model()
    
    def _initialize_api(self):
        """Initialize the Google Generative AI API"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("Google API Key not found. Please add it to your .env file.")
            st.stop()
        
        genai.configure(api_key=api_key)
    
    def _initialize_model(self):
        """Initialize the LangChain Gemini model"""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.3,
            max_output_tokens=2048,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ],
        )
    
    def generate_response(self, user_query, system_prompt, conversation_history):
        """
        Generate a response from the Gemini model using LangChain conversation chain
        
        Args:
            user_query (str): The user's query
            system_prompt (str): The system prompt for the model
            conversation_history (list): List of previous exchanges
        
        Returns:
            str: The model's response
        """
        # Create conversation memory with history
        memory = ConversationBufferMemory()
        
        # Add previous exchanges to memory
        for exchange in conversation_history:
            memory.save_context(
                {"input": exchange["user"]},
                {"output": exchange["assistant"]}
            )
        
        # Create a prompt template
        prompt_template = f"{system_prompt}\n\nCurrent conversation:\n{{history}}\nHuman: {{input}}\nAI:"
        prompt = PromptTemplate.from_template(prompt_template)
        
        # Create conversation chain
        conversation = ConversationChain(
            llm=self.llm,
            memory=memory,
            prompt=prompt,
            verbose=True
        )
        
        # Generate response
        response = conversation.predict(input=user_query)
        
        return response
