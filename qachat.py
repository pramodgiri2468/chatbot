from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime, timedelta
import re

# Load environment variables
load_dotenv()

# Configure Google Gemini API
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
except Exception as e:
    st.error("Error initializing Gemini model. Check your API key or setup.")

def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        return [{"text": "Error fetching response from Gemini model. Please try again later."}]

# Parse date from natural language
def parse_date(query):
    try:
        today = datetime.now()
        if "next" in query.lower():
            if "monday" in query.lower():
                days_ahead = (0 - today.weekday() + 7) % 7 or 7
                return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        elif "tomorrow" in query.lower():
            return (today + timedelta(days=1)).strftime("%Y-%m-%d")
        elif "today" in query.lower():
            return today.strftime("%Y-%m-%d")
        else:
            return "Error parsing date. Please specify a clear date."
    except Exception as e:
        return "Error parsing date. Please try again."

# Email validation
def validate_email(email):
    return re.match(r"^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$", email)

# Phone validation
def validate_phone(phone):
    return re.match(r"^\+?\d{10,15}$", phone)

# Initialize Streamlit app
st.set_page_config(page_title="Chatbot with Q&A and Conversational Form")
st.header("Chatbot")

# Initialize session states
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

if "form_data" not in st.session_state:
    st.session_state['form_data'] = {}

input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and input:
    # Check if the user wants to trigger the form
    if "call me" in input.lower() or "book an appointment" in input.lower():
        st.subheader("Fill in your details:")
        with st.form("user_form"):
            name = st.text_input("Name:")
            phone = st.text_input("Phone Number:")
            email = st.text_input("Email:")
            date_query = st.text_input("Preferred Date (e.g., next Monday, tomorrow):")
            submit_form = st.form_submit_button("Submit")

            if submit_form:
                date = parse_date(date_query)
                if not name.strip():
                    st.error("Name is required.")
                elif not validate_phone(phone):
                    st.error("Invalid phone number. Use a valid format (e.g., +1234567890).")
                elif not validate_email(email):
                    st.error("Invalid email address.")
                elif "Error" in date:
                    st.error(date)
                else:
                    st.success("Details submitted successfully!")
                    st.session_state['form_data'] = {
                        "Name": name,
                        "Phone": phone,
                        "Email": email,
                        "Date": date
                    }
                    st.write("Your Details:")
                    st.json(st.session_state['form_data'])
    else:
        # Handle regular questions
        response = get_gemini_response(input)
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The response is:")
        for chunk in response:
            if hasattr(chunk, "text"):  # Safely access the text attribute
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
