import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pytz import timezone
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Fetch values from .env
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

# Page Configuration
st.set_page_config(page_title="Mental Health Questionnaire", page_icon="🧠", layout="wide")

# Custom CSS to center the content and style the submit button
st.markdown(
    """
    <style>
    .main {
        display: flex;
        justify-content: center;
    }
    .block-container {
        width: 80%;
        text-align: center;
    }
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to connect to Google Sheets
def connect_to_gsheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Load credentials from the environment variable
    creds_dict = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # Open the spreadsheet using its ID
    sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
    return sheet

# Function to save data to Google Sheets
def save_to_gsheet(sheet, data):
    sheet.append_row(data)

def main():
    st.title("Mental Health Questionnaire")
    st.write("Silakan jawab pertanyaan di bawah ini dengan 'Ya' atau 'Tidak'.")

    # Questions
    questions = [
        "Apakah Sdr sering sakit kepala?",
        "Apakah nafsu makan Sdr menurun?",
        "Apakah Sdr tidak bisa tidur nyenyak?",
        "Apakah Sdr mudah merasa takut?",
        "Apakah tangan Sdr gemetar?",
        "Apakah Sdr merasa cemas, tegang, atau khawatir?",
        "Apakah pencernaan Sdr buruk?",
        "Apakah Sdr mengalami kesulitan untuk berpikir jernih?",
        "Apakah Sdr merasa tidak bahagia?",
        "Apakah Sdr lebih sering menangis dari biasanya?",
        "Apakah Sdr sulit menikmati kegiatan sehari-hari?",
        "Apakah Sdr merasa kesulitan untuk mengambil keputusan?",
        "Apakah hasil kerja sehari-hari Sdr memburuk?",
        "Apakah Sdr merasa tidak bisa melakukan hal yang bermanfaat dalam hidup?",
        "Apakah Sdr kehilangan minat untuk melakukan berbagai macam hal?",
        "Apakah Sdr merasa sebagai orang yang tidak berharga?",
        "Apakah Sdr memiliki pemikiran untuk mengakhiri hidup?",
        "Apakah Sdr merasa lelah sepanjang waktu?",
        "Apakah Sdr merasakan perasaan tidak nyaman di perut?",
        "Apakah Sdr mudah merasa lelah?",
    ]

    # Organizing questions into columns
    col1, col2 = st.columns(2)
    responses = []

    with col1:
        for i, question in enumerate(questions[:len(questions)//2], 1):
            response = st.radio(f"{i}. {question}", ["Ya", "Tidak"], key=f"q{i}", index=None, horizontal=True)
            responses.append(response)

    with col2:
        for i, question in enumerate(questions[len(questions)//2:], len(questions)//2 + 1):
            response = st.radio(f"{i}. {question}", ["Ya", "Tidak"], key=f"q{i}", index=None, horizontal=True)
            responses.append(response)

    # Submit button
    if st.button("Submit"):
        # Check if all questions are answered
        if None in responses:
            st.error("Harap menjawab semua pertanyaan sebelum submit.")
            return

        # Display the user's responses
        with st.expander("Lihat Jawaban Anda"):
            for i, (question, response) in enumerate(zip(questions, responses), 1):
                st.write(f"{i}. {question} - **{response}**")
        
        # Count "Ya" responses
        ya_count = sum(1 for response in responses if response == "Ya")
        
        # Logic to determine mental health status
        prediction = "Ada gangguan mental health" if ya_count >= 6 else "Tidak ada gangguan mental health"
        if ya_count >= 6:
            st.warning(
                f"### ⚠️ Prediksi: {prediction}\n\n"
                "Kami menyarankan Anda untuk berkonsultasi dengan profesional kesehatan mental. "
                "Ingat, mencari bantuan adalah tanda kekuatan, bukan kelemahan."
            )
        else:
            st.success(
                f"### 🌟 Prediksi: {prediction}\n\n"
                "Anda tampaknya dalam kondisi mental yang baik. Tetap jaga kesehatan mental Anda!"
            )

        # Prepare data to save, with timestamp and prediction at the front
        jakarta_tz = timezone("Asia/Jakarta")
        timestamp = datetime.now(jakarta_tz).strftime("%Y-%m-%d %H:%M:%S")
        data_to_save = [timestamp, prediction] + responses

        # Save data to Google Sheets
        try:
            sheet = connect_to_gsheets()
            save_to_gsheet(sheet, data_to_save)
            st.success("Jawaban berhasil disimpan ke Google Sheets.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat menyimpan ke Google Sheets: {e}")

if __name__ == "__main__":
    main()
