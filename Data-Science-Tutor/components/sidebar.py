import streamlit as st

def render_sidebar():
    """Render the sidebar with options and information"""
    with st.sidebar:
        # Center logo
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("static/img/logo.svg", width=130)
        
        st.markdown('<h2 class="sidebar-header">About</h2>', unsafe_allow_html=True)
        st.markdown(
            '<p class="sidebar-text">Data Science Tutor AI is powered by Google\'s Gemini 1.5 Pro model and '
            'designed to help you learn data science concepts and solve related problems.</p>',
            unsafe_allow_html=True
        )
        
        st.markdown('<h2 class="sidebar-header">Features</h2>', unsafe_allow_html=True)
        features = [
            "Conversational memory",
            "Code examples",
            "Data visualization explanations",
            "Statistical concepts",
            "Machine learning guidance"
        ]
        
        for feature in features:
            st.markdown(f'<li class="sidebar-list-item">{feature}</li>', unsafe_allow_html=True)
        
        # Example questions
        st.markdown('<h2 class="sidebar-header">Example Questions</h2>', unsafe_allow_html=True)
        example_questions = [
            "Explain the difference between supervised and unsupervised learning",
            "How do I handle missing data in pandas?",
            "What's the best way to visualize a correlation matrix?",
            "Explain the bias-variance tradeoff",
            "How do I implement k-means clustering in Python?"
        ]
        
        def add_example_to_chat(example):
            st.session_state.messages.append({"role": "user", "content": example})
            st.session_state.thinking = True  # Set thinking state before generating response
            #with st.spinner("Thinking..."):
            response = st.session_state.tutor.get_response(example)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.thinking = False  # Reset thinking state after response is generated
        
        for example in example_questions:
            st.button(
                example, 
                key=f"example_{hash(example)}", 
                on_click=add_example_to_chat, 
                args=(example,),
                use_container_width=True
            )
        
        # Clear conversation button
        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Conversation", key="clear_conversation", use_container_width=True):
            st.session_state.messages = []
            response = st.session_state.tutor.clear_conversation()
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.success("Conversation cleared!")
