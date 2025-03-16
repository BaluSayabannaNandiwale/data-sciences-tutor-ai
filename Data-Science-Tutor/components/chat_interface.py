import streamlit as st
import time
import re

def render_chat_interface():
    """Render the main chat interface for the Data Science Tutor"""
    
    # Display welcome message if this is a new session
    if len(st.session_state.messages) == 0:
        greeting = "👋 Hello! I'm your Data Science Tutor. I can help you understand data science concepts, explain algorithms, and provide code examples. What would you like to learn about today?"
        st.session_state.messages.append({"role": "assistant", "content": greeting})
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        content = message["content"]
        
        # Process message content to remove language indicators after code blocks
        # This is a more comprehensive pattern to remove any language identifier
        content = re.sub(r'```(?:python|java|javascript|html|css|json|bash|sql|r|any language tag)\n', r'```\n', content, flags=re.IGNORECASE)
        
        with st.chat_message(message["role"], avatar="static/img/logo.svg" if message["role"] == "assistant" else None):
            st.markdown(f'<div class="message {message["role"]}-message">{content}</div>', unsafe_allow_html=True)
    
    # This must be directly in the main app flow, not in any container, column, etc.
    prompt = st.chat_input("Ask a data science question...")
    
    # Process user input
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Force a rerun to display the user message before generating response
        st.rerun()
