import streamlit as st
import time
from transformers import pipeline
import nltk
from pathlib import Path
# Cache NLTK downloads
if not Path("nltk_cache").exists():
    nltk.download("punkt", download_dir="nltk_cache")
    nltk.download("stopwords", download_dir="nltk_cache")
nltk.data.path.append("nltk_cache")
# Load Healthcare-specific Model
@st.cache_resource
def load_chatbot():
    return pipeline("question-answering", model="deepset/roberta-base-squad2")
chatbot = load_chatbot()
# Manual Responses for Quick Answers (Hindi + English)
manual_responses = {
   "hello": {
    "en": "Namaste!! How can I assist you today?",
    },
    "fever": {
        "en": "A fever is usually a sign of infection. Stay hydrated, rest, and monitor your temperature. Consult a doctor if it persists for more than 3 days.",
    },
    "cough": {
        "en": "A dry cough could be due to allergies, while a wet cough may indicate infection. Drink warm fluids and consult a doctor if severe.",
    },
    "headache": {
        "en": "Headaches can be due to stress, dehydration, or lack of sleep. Try resting, drinking water, or taking a mild pain reliever.",
    },
    "appointment": {
        "en": "You can book an appointment by calling your nearest hospital or using an online healthcare booking service.",
    },
    "book appointment": {
        "en": "You can book an appointment by calling your nearest hospital or using an online healthcare booking service.",
    },
    
    "cancel appointment": {
        "en": "You can cancel your appointment by contacting the hospital or through the online booking platform you used.",
    },
    
    "reschedule appointment": {
        "en": "To reschedule, call the hospital or visit the website where you booked your appointment.",
    },
    
    "appointment documents": {
        "en": "You may need an ID proof, previous medical reports, and a referral letter if required.",
    },
    
    "walk-in appointment": {
        "en": "Some hospitals allow walk-in consultations, but booking an appointment is recommended to avoid long waiting times.",
    }
}
# Healthcare Chatbot Logic
def healthcare_chatbot(user_input):
    user_input = user_input.lower()
    lang = detect_language(user_input)
    
    # Check for quick responses first
    for key in manual_responses.keys():
        if key in user_input:
            return manual_responses[key][lang]
    
    # AI-generated response
    response = chatbot(question=user_input, context="This is a healthcare chatbot providing medical advice.")
    return response["answer"]
# Typing Animation Effect with st.empty()
def typing_effect(text):
    displayed_text = ""
    placeholder = st.empty()  # Create a placeholder to update text dynamically
    for char in text:
        displayed_text += char
        placeholder.markdown(f"**Healthcare Assistant:** {displayed_text}█", unsafe_allow_html=True)
        time.sleep(0.03)
# Streamlit Web App with Animation
def main():
    st.title("🚑 AI-Healthcare Assistant Chatbot (English)")
    # Custom Styling for Chat UI
    st.markdown(
        """
        <style>
        .stChatMessage {
            background-color: #f0f2f6;
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 8px;
        }
        .stChatInput input {
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    user_input = st.chat_input("How can I assist you today?)
    
    if user_input:
        st.write("👤 **User:**", user_input)
        
        with st.spinner("💡 Processing your query... ):
            time.sleep(1.5)  # Simulating processing time
            response = healthcare_chatbot(user_input)
        typing_effect(response)  # Display response with animation
if __name__ == "__main__":
    main()
