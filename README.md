# Chatbot using Gemini Pro & Streamlit

A chatbot built with Google's **Gemini Pro API** for natural language processing and **Streamlit** for an interactive UI.

## 🚀 Features

- Uses **Gemini Pro API** for AI-powered responses
- Interactive UI with **Streamlit**
- Secure API key handling with **python-dotenv**

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/pramodgiri2468/chatbot.git
cd chatbot-gemini-pro
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the root directory and add:

```plaintext
GOOGLE_API_KEY=your_api_key_here
```

## 🎮 Usage

Run the chatbot:

```bash
streamlit run app.py
```

## 🛠 Technologies Used

- **Google Gemini Pro API** (`google-generativeai`)
- **Streamlit** (UI framework)
- **Python-dotenv** (Environment variable management)
