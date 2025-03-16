import streamlit as st

class ConversationMemory:
    """
    Handles storing and retrieving conversation history
    """
    
    def __init__(self, max_history=20):
        """
        Initialize the conversation memory
        
        Args:
            max_history (int): Maximum number of exchanges to keep in memory
        """
        self.max_history = max_history
    
    def add_exchange(self, user_message, assistant_response):
        """
        Add a new exchange to the conversation history
        
        Args:
            user_message (str): The user's message
            assistant_response (str): The assistant's response
        """
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Add the new exchange
        st.session_state.chat_history.append({
            "user": user_message,
            "assistant": assistant_response
        })
        
        # Trim history if it exceeds max_history
        if len(st.session_state.chat_history) > self.max_history:
            st.session_state.chat_history = st.session_state.chat_history[-self.max_history:]
    
    def get_conversation_history(self):
        """
        Get the current conversation history
        
        Returns:
            list: List of conversation exchanges
        """
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        return st.session_state.chat_history
    
    def clear(self):
        """Clear the conversation history"""
        st.session_state.chat_history = []
