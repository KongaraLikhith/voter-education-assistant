import os
import google.generativeai as genai

# Configure the model
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = """You are an expert India election education assistant. You help Indian citizens understand:
- Voter registration process on voters.eci.gov.in
- Lok Sabha, Rajya Sabha, and State Assembly elections
- Election phases and timelines
- EVM machines and VVPAT systems
- Model Code of Conduct
- How to find polling booths
- Voter ID (EPIC card) application and correction
- NOTA option and its significance
- Role of Election Commission of India
- Difference between President, PM, MP, MLA roles
Always respond in simple, clear English. If user writes in Hindi, respond in Hindi.
Be factual, neutral, and educational. Never support any political party."""

async def get_gemini_response(message: str, history: list) -> str:
    if not API_KEY:
        return "Gemini API key is not configured. Please set the GEMINI_API_KEY environment variable."
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=SYSTEM_PROMPT)
        
        formatted_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg["content"]]})
        
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(message)
        
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"
