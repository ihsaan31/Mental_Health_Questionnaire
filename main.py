import streamlit as st
import joblib  # To load the .pkl model

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
    /* Make submit button wider and more prominent */
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

# Load the model
@st.cache_resource
def load_model():
    with open('random_forest_model.pkl', 'rb') as file:
        return joblib.load(file)

# Load the model only once
model = load_model()

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
        
        # Prepare the data for prediction
        model_input = [1 if response == "Ya" else 0 for response in responses]
        
        # Make the prediction using the loaded model
        prediction = model.predict([model_input])

        # Create a more prominent prediction display
        if prediction == 0:
            st.success(
                "### 🌟 Prediksi: Tidak ada gangguan mental health\n\n"
                "Anda tampaknya dalam kondisi mental yang baik. Tetap jaga kesehatan mental Anda!"
            )
        else: 
            st.warning(
                "### ⚠️ Prediksi: Ada gangguan mental health\n\n"
                "Kami menyarankan Anda untuk berkonsultasi dengan profesional kesehatan mental. "
                "Ingat, mencari bantuan adalah tanda kekuatan, bukan kelemahan."
            )

if __name__ == "__main__":
    main()