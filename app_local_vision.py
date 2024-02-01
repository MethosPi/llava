import streamlit as st
import torch
from transformers import pipeline

pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")

# Set app title
st.title("DeltaPi Chatbot")

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

    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    # Get assistant response
    response = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)

    assistant_response = response[0]["generated_text"].split("<|assistant|>")[1]

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    
        # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
