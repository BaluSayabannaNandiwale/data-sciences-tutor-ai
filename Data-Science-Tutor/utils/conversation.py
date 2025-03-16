from utils.gemini_handler import GeminiModelHandler
from utils.memory_handler import ConversationMemory
import streamlit as st
import re

class DataScienceTutor:
    """
    Main class for the Data Science Tutor application that coordinates
    the language model and memory components.
    """
    
    def __init__(self):
        """Initialize the tutor with the language model and memory"""
        self.model_handler = GeminiModelHandler()
        self.memory = ConversationMemory()
        self.system_prompt = """
        You are an expert Data Science Tutor specializing in helping users understand 
        concepts, solve problems, and learn about tools and techniques in data science.
        
        Your expertise includes:
        - Data analysis and visualization
        - Machine learning algorithms and models
        - Statistical analysis and hypothesis testing
        - Python libraries like pandas, numpy, scikit-learn, matplotlib, seaborn, tensorflow, PyTorch
        - Data cleaning and preprocessing
        - Feature engineering
        - Model evaluation and validation
        - Big data technologies
        
        Only answer questions related to data science. If asked about topics outside of 
        data science, politely redirect the conversation back to data science topics.
        
        When explaining concepts:
        - Start with simple explanations before getting technical
        - Use analogies when helpful
        - Provide code examples when appropriate, formatting them properly with code blocks
        - Break down complex topics into understandable parts
        - Refer to the conversation history for context
        
        IMPORTANT: Always format your code examples using the triple backtick markdown syntax with the language specified:
        ```python
        # Python code goes here
        import pandas as pd
        ```
        
        Make sure there is a clear separation between your explanatory text and code blocks.
        Never include regular text inside code blocks and ensure each code block starts and ends with its own line.
        
        If you include a plot or visualization in your explanation, describe what the user would see since you cannot generate actual images.
        
        Be encouraging, patient, and supportive throughout the learning process.
        """
    
    def get_response(self, user_query):
        """
        Get a response from the Data Science Tutor for the given user query
        while maintaining conversation context
        """
        # Get conversation history from memory
        conversation_history = self.memory.get_conversation_history()
        
        # Generate response using the model
        response = self.model_handler.generate_response(
            user_query, 
            self.system_prompt, 
            conversation_history
        )
        
        # Improve code block formatting
        response = self._format_code_blocks(response)
        
        # Add the current exchange to memory
        self.memory.add_exchange(user_query, response)
        
        return response
    
    def _format_code_blocks(self, text):
        """Ensure proper formatting of code blocks in the response"""
        # Check if text already has markdown code blocks
        if "```" in text:
            # Replace ```python with just ``` (remove language indicator)
            text = re.sub(r'```(?:python|java|javascript|html|css|json|bash|sql|r|any language tag)\n', r'```\n', text, flags=re.IGNORECASE)
            
            # Ensure code blocks are properly separated from text
            text = re.sub(r'([^\n])```', r'\1\n```', text)
            text = re.sub(r'```([^\n])', r'```\n\1', text)
            
            return text
        
        # Find potential code snippets without formatting and format them
        code_pattern = r'(\n|^)((?:from|import|def|class|if|for|while)\s+.+(?:\n\s+.+)*)'
        text = re.sub(code_pattern, r'\1```\n\2\n```', text)
        
        return text
    
    def clear_conversation(self):
        """Clear the conversation history"""
        self.memory.clear()
        return "Conversation history cleared. What data science topic would you like to learn about?"
