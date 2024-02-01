import streamlit as st
import torch
from PIL import Image
import requests
from transformers import AutoProcessor, LlavaForConditionalGeneration
from transformers import pipeline

model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf")
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")

# Set app title
st.title("DeltaPi AI - Local LLM Vision")

st.sidebar.title("Upload Image")

# Upload multiple files
uploaded_images = st.sidebar.file_uploader("Upload images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# Display uploaded images
if uploaded_images:
    for uploaded_file in uploaded_images:
        image = Image.open(requests.get(url, stream=True).raw)
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
    messages = [
    {"role": "user", "content": f"User prompt: {prompt}"},
    ]

    inputs = processor(text=prompt, images=image, return_tensors="pt")

    generate_ids = model.generate(**inputs, max_length=30)
    response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

#    assistant_response = response[0]["generated_text"].split("<|assistant|>")[1]

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    
        # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
