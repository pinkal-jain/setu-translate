import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io


st.title("Setu - Translator")

if "translated_text" not in st.session_state:
    st.session_state["translated_text"] = ""

if "target_lang_code" not in st.session_state:
    st.session_state["target_lang_code"] = "en"

languages = GoogleTranslator().get_supported_languages(as_dict=True)
lang_names = list(languages.keys())

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From", ["auto"] + lang_names, index=0)
with col2:
    target_lang = st.selectbox("To", lang_names, index=lang_names.index("english"))

text_input = st.text_area("Enter text to translate", height=150)


if st.button("Translate"):
    if text_input.strip():
        src = "auto" if source_lang == "auto" else languages[source_lang]
        tgt = languages[target_lang]
        try:
            translated = GoogleTranslator(source=src, target=tgt).translate(text_input)
            st.session_state["translated_text"] = translated
            # ✅ CHANGE 2: Add this — save tgt so it survives the rerun
            st.session_state["target_lang_code"] = tgt
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.warning("Please enter some text.")


# ✅ CHANGE 3: Wrap everything below (output, Listen button, code box)
# inside ONE if-block that checks there's actually text to show
if st.session_state["translated_text"]:
    st.subheader("Translated Text")
    st.text_area("Output", st.session_state["translated_text"], height=150)

    if st.button("🔊 Listen"):
        tts = gTTS(
            text=st.session_state["translated_text"],
            lang=st.session_state["target_lang_code"]  
        )
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        st.audio(audio_bytes.getvalue(), format="audio/mp3")

    st.code(st.session_state["translated_text"], language=None)
  