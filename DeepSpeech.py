import streamlit as st
import speech_recognition as sr
import pickle

# Load the pickled chatbot model
with open('Deep-chatbot.pkl', 'rb') as f:
    chatbot = pickle.load(f)

# Define the speech transcription function
def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            st.success(f"Transcribed Speech: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("Error in request to Google Speech API.")
            return None

# Define the function to get chatbot response
def get_response(user_input):
    if user_input:
        response = chatbot.respond(user_input.lower())
        return response
    return None

# Main function to run the Streamlit app
def main():
    st.title("Speech-Enabled Chatbot")

    # Choose input method (Text or Speech)
    input_method = st.selectbox("Choose your input method", ["Text", "Speech"])

    if input_method == "Text":
        user_input = st.text_input("You: ", "")
        if user_input:
            response = get_response(user_input)
            if response:
                st.write(f"Chatbot: {response}")

    elif input_method == "Speech":
        if st.button("Start Listening"):
            user_input = transcribe_speech()
            if user_input:
                response = get_response(user_input)
                if response:
                    st.write(f"Chatbot: {response}")

# Ensure the script runs when executed
if __name__ == "__main__":
    main()