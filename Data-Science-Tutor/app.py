import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.conversation import DataScienceTutor
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🚨 GOOGLE_API_KEY not found. Please check your .env file.")
    st.stop()

# Configure Google AI
genai.configure(api_key=api_key)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

# Initialize session state
def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "tutor" not in st.session_state:
        st.session_state.tutor = DataScienceTutor()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "thinking" not in st.session_state:
        st.session_state.thinking = False
    if "header_rendered" not in st.session_state:
        st.session_state.header_rendered = False

# Function to display chat messages
def display_chat_messages():
    for chat in reversed(st.session_state.chat_history):
        with st.chat_message("user"):
            st.markdown(f"**You:** {chat['user']}")
        with st.chat_message("assistant"):
            st.markdown(f"**AI:** {chat['ai']}")

def main():
    st.set_page_config(
        page_title="Data Science Tutor AI",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Data Science Tutor AI powered by Gemini 1.5 Pro"
        }
    )
    
    # Apply custom CSS before any elements are rendered
    try:
        with open("static/css/style.css") as f:
            st.markdown(f"""
            <style>
            {f.read()}
            </style>
            """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Style file not found. UI may not display properly.")
    
    # Initialize session state
    initialize_session_state()
    
    # Only render the title if we're not in the middle of processing a response
    if not st.session_state.thinking:
        # App title
        col1, col2 = st.columns([1, 9])
        with col1:
            try:
                st.markdown("")
                st.image("static/img/logo.svg", width=80)
            except FileNotFoundError:
                st.warning("Logo file not found.")
        with col2:
            st.markdown('<h1 class="main-title">Data Science Tutor AI</h1>', unsafe_allow_html=True)
            st.markdown('<h3 class="subtitle">Your personal AI assistant for data science learning</h3>', unsafe_allow_html=True)
        
        # Mark headers as rendered
        st.session_state.header_rendered = True
    
    # Render sidebar with options
    render_sidebar()
    
    # Render main chat interface
    render_chat_interface()
    
    # Process assistant response if user input was just added
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and not st.session_state.thinking:
        st.session_state.thinking = True
        
        # Get the user's message
        user_message = st.session_state.messages[-1]["content"]
        
        # Create a placeholder for the assistant response below the last message
        with st.chat_message("assistant", avatar="static/img/logo.jpg"):
            message_placeholder = st.empty()
            message_placeholder.markdown('<div class="message assistant-message">Thinking...</div>', unsafe_allow_html=True)
            
            # Generate response
            try:
                # Step 1: AI Checks If the Question is Related to Data Science
                check_prompt = f"""sgt
                You are an AI tutor for data science.
                - Check if the following question is **strictly** related to data science.
                - Answer with just **YES** or **NO** (no explanations).

                Question: "{user_message}"
                """
                check_response = llm.invoke(check_prompt).content.strip().lower()

                if check_response == "yes":
                    # Step 2: AI Answers the Question (Only if Related to Data Science)
                    response = llm.invoke(user_message).content

                    # Stream the response
                    displayed_response = ""
                    for chunk in response.split():
                        displayed_response += chunk + " "
                        message_placeholder.markdown(
                            f'<div class="message assistant-message">{displayed_response}▌</div>', 
                            unsafe_allow_html=True
                        )
                        time.sleep(0.01)
                    
                    # Display final response
                    message_placeholder.markdown(
                        f'<div class="message assistant-message">{response}</div>', 
                        unsafe_allow_html=True
                    )
                    
                    # Save chat history
                    st.session_state.chat_history.append({"user": user_message, "ai": response})
                else:
                    # Step 3: AI Rejects Non-Data Science Questions
                    rejection_message = "I can only answer data science-related questions. Please ask something related to data science. 😊"
                    message_placeholder.markdown(
                        f'<div class="message assistant-message">{rejection_message}</div>', 
                        unsafe_allow_html=True
                    )
                    st.session_state.chat_history.append({"user": user_message, "ai": rejection_message})

            except Exception as e:
                error_message = f"Sorry, I encountered an error: {str(e)}"
                message_placeholder.markdown(
                    f'<div class="message assistant-message">{error_message}</div>', 
                    unsafe_allow_html=True
                )
                st.session_state.chat_history.append({"role": "assistant", "content": error_message})
        
        # Reset thinking state
        st.session_state.thinking = False
        st.session_state.header_rendered = False
        
        # Rerun to clean up the UI state
        st.experimental_rerun()

    # Clear chat history button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()