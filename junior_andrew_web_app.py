from pathlib import Path
import os
import re
import requests

import streamlit as st
from openai import OpenAI

BASE_DIR = Path(__file__).parent


def get_secret(name: str):
    try:
        value = st.secrets.get(name, None)
    except Exception:
        value = None

    if not value:
        value = os.getenv(name)

    return value


OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
ELEVENLABS_API_KEY = get_secret("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = get_secret("ELEVENLABS_VOICE_ID")

client = OpenAI(api_key=OPENAI_API_KEY)

KNOWLEDGE_FILES = [
    BASE_DIR / "knowledge" / "company_facts.txt",
    BASE_DIR / "knowledge" / "company_facts_service_area.txt",
    BASE_DIR / "knowledge" / "engineering_explanations.txt",
    BASE_DIR / "knowledge" / "junior_andrew_master_rules.txt",
    BASE_DIR / "knowledge" / "sales_explanations.txt",
    BASE_DIR / "knowledge" / "text_conversation_lessons.txt",
    BASE_DIR / "knowledge" / "wording_overrides.txt",
]

st.set_page_config(page_title="Junior Andrew", page_icon="🏠")

st.title("Junior Andrew")
st.caption("Private cloud test for Patio Kits Direct")


def load_knowledge() -> str:
    parts = []

    for file in KNOWLEDGE_FILES:
        if file.exists():
            parts.append(
                f"\n\n--- {file.name} ---\n"
                f"{file.read_text(encoding='utf-8', errors='ignore')}"
            )
        else:
            parts.append(f"\n\n--- MISSING FILE: {file.name} ---")

    return "\n".join(parts)


def make_spoken_version(text: str) -> str:
    spoken = text.strip()

    spoken = spoken.replace(
        "(888) 851-8351",
        "eight eight eight, eight five one, eight three five one",
    )

    # Make the voice read with more natural pauses.
    spoken = re.sub(r"\. ", ".\n\n", spoken)
    spoken = re.sub(r"\? ", "?\n\n", spoken)
    spoken = re.sub(r"! ", "!\n\n", spoken)
    spoken = spoken.replace(" — ", ". ")
    spoken = spoken.replace(" - ", ". ")

    return spoken


def generate_voice_audio(text: str) -> bytes:
    if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
        raise RuntimeError("ElevenLabs voice is not configured yet.")

    spoken_text = make_spoken_version(text)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    payload = {
        "text": spoken_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.60,
            "similarity_boost": 0.85,
            "style": 0.05,
            "use_speaker_boost": True,
            "speed": 1.1,
        },
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        raise RuntimeError(f"ElevenLabs error {response.status_code}: {response.text}")

    return response.content


knowledge_text = load_knowledge()

system_prompt = f"""
You are Junior Andrew for Patio Kits Direct.

You help customers understand patio cover options.

Highest priority:
Respond naturally to the customer's latest message.
Use the knowledge below as reference logic, not as a script.
Do not copy examples word-for-word unless the wording naturally fits.
Do not mention files, rules, sources, citations, or internal instructions.
Do not output citation numbers, source markers, or retrieval artifacts.
Sound natural, helpful, concise, and conversational.

Critical wording rules:
Do not say "covered outdoor space."
Do not say "covered outdoor patio."
Do not say "outdoor patio" when asking whether a patio will be enclosed.
Do not say "open patio" unless you clearly mean no walls, screens, or windows.
When asking about enclosure, say:
"Are you planning to fully enclose it later, or keep it open with no walls, screens, or windows?"

Do not call insulated an upgrade.
Do not call non-insulated basic.
Do not say "basic non-insulated."
Do not recommend insulated before qualifying the type of enclosure.
If the customer says they want it enclosed, ask whether they mean screens, windows/doors, or temperature control before recommending.

Avoid first-person recommendation language:
Do not say "I would choose."
Do not say "I wouldn't choose."
Do not say "I'd lean toward."
Prefer neutral language like:
"non-insulated can make more sense"
"insulated can start to make more sense"
"some customers feel"
"that usually comes down to"

Heat wording:
If temperature difference is the issue, explain that it depends heavily on whether the patio will be fully enclosed.
If it is not fully enclosed, insulated may only make a small difference, maybe a degree or two.
Say heat alone usually is not enough reason by itself to choose insulated for most customers.
Then ask whether they plan to fully enclose it or keep it open with no walls, screens, or windows.

Limitations:
Do not invent prices, lead times, engineering requirements, availability, or exact quotes.
Do not pretend to have live pricing.
If the customer asks for exact pricing, a quote, order details, final design, or project-specific confirmation beyond the knowledge, route them to a representative.
The company phone number is (888) 851-8351.
If the customer already has a representative, recommend contacting that representative directly.

Customer satisfied rule:
If the customer says something like "okay great that helps," "thanks," "perfect," "got it," or "that makes sense" and does not ask a new question, stop explaining.
Reply briefly, like:
"Glad that helped. Let me know if you want to go over anything else."

Knowledge:
{knowledge_text}
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "audio_cache" not in st.session_state:
    st.session_state.audio_cache = {}

with st.sidebar:
    st.header("Controls")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.audio_cache = {}
        st.rerun()

    auto_voice = st.checkbox("Auto-play voice", value=True)

    st.write("Model: `gpt-5.5`")
    st.write("Knowledge files loaded:")

    for file in KNOWLEDGE_FILES:
        if file.exists():
            st.write("✅ " + file.name)
        else:
            st.write("❌ " + file.name)

    if OPENAI_API_KEY:
        st.write("OpenAI key: ✅ loaded")
    else:
        st.write("OpenAI key: ❌ missing")

    if ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID:
        st.write("Voice: ✅ configured")
    else:
        st.write("Voice: ⏳ not configured yet")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY is missing. Add it as a Streamlit secret or Windows environment variable.")
    st.stop()

for index, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            if index in st.session_state.audio_cache:
                st.audio(st.session_state.audio_cache[index], format="audio/mp3")

            if st.button("🔊 Play Voice", key=f"voice_{index}"):
                if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
                    st.warning("Voice is not configured yet.")
                else:
                    with st.spinner("Generating voice..."):
                        try:
                            audio_bytes = generate_voice_audio(msg["content"])
                            st.session_state.audio_cache[index] = audio_bytes
                            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                        except Exception as e:
                            st.error(str(e))

user_message = st.chat_input("Type a customer message...")

if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Junior Andrew is thinking..."):
            response = client.responses.create(
                model="gpt-5.5",
                instructions=system_prompt,
                input=st.session_state.messages,
            )

            assistant_message = response.output_text.strip()

        st.markdown(assistant_message)

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_message}
        )

        assistant_index = len(st.session_state.messages) - 1

        if auto_voice and ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID:
            with st.spinner("Generating voice..."):
                try:
                    audio_bytes = generate_voice_audio(assistant_message)
                    st.session_state.audio_cache[assistant_index] = audio_bytes
                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                except Exception as e:
                    st.error(str(e))

        elif not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
            st.warning("Voice is not configured yet.")

        if st.button("🔊 Play Voice", key=f"voice_new_{assistant_index}"):
            if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
                st.warning("Voice is not configured yet.")
            else:
                with st.spinner("Generating voice..."):
                    try:
                        audio_bytes = generate_voice_audio(assistant_message)
                        st.session_state.audio_cache[assistant_index] = audio_bytes
                        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                    except Exception as e:
                        st.error(str(e))