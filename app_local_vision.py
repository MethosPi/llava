import streamlit as st
import ollama

# Set app title
st.title("DeltaPi AI - Local LLM Vision")

st.sidebar.title("Upload Image")

# Upload multiple files
uploaded_images = st.sidebar.file_uploader("Upload images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# Display uploaded images
if uploaded_images:
    for uploaded_file in uploaded_images:
        # Display the uploaded image
        st.sidebar.image(uploaded_file)

# Create chat message
message = st.chat_message("assistant")
message.write("Hello I'm DeltaPi Chatbot, what can I do for you?")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Prompt:"):

# Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})   

     

   # Send user prompt to OpenAI
    prompt = f"User prompt: {prompt}"
    
    if uploaded_images:
        # Get assistant response
        response = ollama.generate(model='llava', prompt = prompt, images= uploaded_images)
        assistant_response = response['response']

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        
            # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    else:
        response = ollama.chat(model='llava', messages=[
                {"role": "user", "content": f"{prompt}"}
            ])

        assistant_response = response['message']['content']

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        
            # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
