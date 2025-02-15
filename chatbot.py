import streamlit as st 
import nltk
from transformers import pipeline
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


chatbot = pipeline("text-generation", model="distilgpt2")


def healthcare_chatbot (user_input):
    if "symptom" in user_input:
        return "Please consult Doctor for accurate advice"
    elif "appointment" in user_input:
        return "Would you like to schedule appointment with the Doctor?"

    elif "medication" in user_input:
        return "It's important to take prescribed medicines regularly. If you have concerns, consult your doctor. "
     
    else:
        response = chatbot(user_input,max_length=500, num_return_sequences=1)
        return response[0]['generated_text']


def main():
    st.title('healthcare assistant chatbot')
    user_input=st.text_input('enter your problem')
    print(user_input)
    if st.button('submit'):
        if user_input:
            st.write('user: ',user_input)
            with st.spinner('proccessing please wait......'):
                response=healthcare_chatbot(user_input)
            st.write('healthcare assistance: ',response)
            print(response)

        else:
            st.write('please enter message for response')

main()
