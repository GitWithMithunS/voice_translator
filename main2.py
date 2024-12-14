import streamlit as st
import googletrans
import speech_recognition
import gtts
import os

def translate_speech(src_lang, dest_lang):
    """
    Perform speech recognition, translation, and text-to-speech.
    
    :param src_lang: Source language code
    :param dest_lang: Destination language code
    :return: Tuple of (original text, translated text)
    """
    # Initialize recognizer
    recognizer = speech_recognition.Recognizer()
    
    # Capture audio
    with speech_recognition.Microphone() as source:
        st.write(f"Speak in {src_lang} language...")
        try:
            # Listen to audio
            audio = recognizer.listen(source, timeout=5)
            
            # Recognize speech
            speech_text = recognizer.recognize_google(audio, language=src_lang)
            st.write(f"You said in {src_lang}: {speech_text}")
            
            # Translate text
            translator = googletrans.Translator()
            translation = translator.translate(
                text=speech_text, 
                src=src_lang, 
                dest=dest_lang
            )
            
            # Text to speech
            tts = gtts.gTTS(translation.text, lang=dest_lang)
            tts.save("translation.mp3")
            
            return speech_text, translation.text
        
        except speech_recognition.UnknownValueError:
            st.error("Could not understand the audio")
            return None, None
        except speech_recognition.RequestError:
            st.error("Could not request results from Google Speech Recognition")
            return None, None
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None, None

def main():
    st.title("🌐 Multilingual Voice Translator")
    
    # Language selection
    st.sidebar.header("Translation Settings")
    source_lang = st.sidebar.selectbox(
        "Source Language", 
        list(googletrans.LANGUAGES.values()), 
        index=list(googletrans.LANGUAGES.values()).index('kannada')
    )
    dest_lang = st.sidebar.selectbox(
        "Destination Language", 
        list(googletrans.LANGUAGES.values()), 
        index=list(googletrans.LANGUAGES.values()).index('hindi')
    )
    
    # Get language codes
    source_code = [code for code, lang in googletrans.LANGUAGES.items() if lang == source_lang][0]
    dest_code = [code for code, lang in googletrans.LANGUAGES.items() if lang == dest_lang][0]
    
    # Translate button
    if st.button("🎙️ Start Translation"):
        # Perform translation
        original_text, translated_text = translate_speech(source_code, dest_code)
        
        # Display results
        if original_text and translated_text:
            st.subheader("Translation Results")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"Original ({source_lang}):")
                st.info(original_text)
            
            with col2:
                st.write(f"Translated ({dest_lang}):")
                st.info(translated_text)
            
            # Play audio button
            if st.button("🔊 Play Translation"):
                os.system("start translation.mp3")

if __name__ == "__main__":
    main()