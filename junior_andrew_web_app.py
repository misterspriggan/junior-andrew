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
    BASE_DIR / "knowledge" / "build_instruction_guardrails.txt",
    BASE_DIR / "knowledge" / "patio_cover_build_overview.txt",
    BASE_DIR / "knowledge" / "brochure_product_knowledge.txt",
    BASE_DIR / "knowledge" / "haven_lanais_reference.txt",
    BASE_DIR / "knowledge" / "haven_lanai_slope_reference.txt",
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


def clean_visible_text(text: str) -> str:
    cleaned = text.strip()

    # Keep product name customer-facing and capitalized.
    cleaned = re.sub(r"\bhaven\s+lanais\b", "Haven Lanai", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bhaven\s+lanai\b", "Haven Lanai", cleaned, flags=re.IGNORECASE)

    # Avoid standalone "lanai" / "Lanai" because the voice can pronounce it poorly.
    # Make the visible text say the full product name instead.
    cleaned = re.sub(r"\blanais\b", "Haven Lanai", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\blanai\b", "Haven Lanai", cleaned, flags=re.IGNORECASE)

    # Clean accidental duplicated product names.
    cleaned = re.sub(r"\bHaven Haven Lanai\b", "Haven Lanai", cleaned)
    cleaned = re.sub(r"\bHaven Lanai Haven Lanai\b", "Haven Lanai", cleaned)

    return cleaned


def make_spoken_version(text: str) -> str:
    spoken = clean_visible_text(text)

    spoken = spoken.replace(
        "(888) 851-8351",
        "eight eight eight, eight five one, eight three five one",
    )

    # This is the exact spoken pattern that tested best in ElevenLabs:
    # "A Haven la nai is Patio Kits Direct's fully enclosed option."
    # Visible text still shows "Haven Lanai."
    spoken = re.sub(r"\bHaven Lanai\b", "Haven la nai", spoken, flags=re.IGNORECASE)

    # Company pronunciation helper.
    # Visible text still says fascia, but spoken audio uses the company-preferred hard A pronunciation.
    spoken = re.sub(r"\bfascias\b", "fayshas", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\bfascia\b", "faysha", spoken, flags=re.IGNORECASE)

    # Make dimensions sound natural.
    # Example: 10x20, 10 x 20, 10X20 -> 10 by 20
    spoken = re.sub(r"\b(\d+)\s*[xX]\s*(\d+)\b", r"\1 by \2", spoken)

    # Make common units sound natural.
    spoken = re.sub(r"\bsq\.?\s*ft\.?\b", "square feet", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\bsq\.?\s*feet\b", "square feet", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\b(\d+)\s*ft\.?\b", r"\1 feet", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\b1\s*feet\b", "1 foot", spoken, flags=re.IGNORECASE)

    # Make feet/inch marks sound natural.
    # Example: 22'4" -> 22 feet 4 inches
    spoken = re.sub(r"\b(\d+)'\s*(\d+)\"", r"\1 feet \2 inches", spoken)
    spoken = re.sub(r"\b(\d+)'\b", r"\1 feet", spoken)
    spoken = re.sub(r"\b(\d+)\"", r"\1 inches", spoken)

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
            "speed": 1.05,
        },
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        raise RuntimeError(f"ElevenLabs error {response.status_code}: {response.text}")

    return response.content


knowledge_text = load_knowledge()

system_prompt = f"""
You are Junior Andrew for Patio Kits Direct.

You help customers understand patio cover options, Haven Lanais, build concepts, website/product information, and general Patio Kits Direct guidance.

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

Dimension logic:
For attached patio covers, a size like 10x20 usually means 10 feet projection out from the house and 20 feet length along the house.
Do not say projection is missing when the customer already gave a clear attached-cover size like 10x20.
If the cover is freestanding, or if dimensions are close together, ask which direction is projection/front-to-back and which is length/beam direction.
For freestanding covers, the header beam sitting on top of the posts is the length, and the roof pans or rafters run front-to-back as the projection.
If height is not mentioned, average height is often assumed around 9 feet, but final design should be confirmed by a representative or designer.

Heat wording:
If temperature difference is the issue, explain that it depends heavily on whether the patio will be fully enclosed.
If it is not fully enclosed, insulated may only make a small difference, maybe a degree or two.
Say heat alone usually is not enough reason by itself to choose insulated for most customers.
Then ask whether they plan to fully enclose it or keep it open with no walls, screens, or windows.

Build guidance:
Build instructions are general and not specific to every customer's design.
For build questions, explain the general idea only.
Tell customers to use their final design, quote, parts checklist, and correct instruction set.
If the customer already ordered, build support can pull up the specific design and give better project-specific help.
Do not replace build support.
Do not give exact cuts, anchoring, footing, post placement, or engineering instructions as final.

Haven Lanai guidance:
Haven Lanai is Patio Kits Direct's fully enclosed option.
Always write the product name visibly as "Haven Lanai."
Do not write standalone "Lanai" when "Haven Lanai" would fit.
Always capitalize Haven Lanai.
Never write lowercase "lanai" or "lanais" in customer-facing text.
Never visibly write "la nai", "L anai", "L-anai", "la-nai", or any other pronunciation spelling.
Pronunciation helpers are only for hidden spoken audio, not visible text.
Do not use standard patio cover build instructions to explain how to build a Haven Lanai.
Haven Lanai has its own animated instructions in the 3D Designer for the customer's custom Haven Lanai.
If customers ask how to build a Haven Lanai, route them to the 3D Designer animated instructions and build support for project-specific guidance.
You may explain the general animated instruction roadmap if helpful.

FlexiGlaze / window material guidance:
Do not make the Haven Lanai window material sound cheap or flimsy.
Do not lead with "flexible vinyl" in a way that sounds negative.
Better framing:
"The windows have a glass-like look, but they use FlexiGlaze vinyl instead of glass. It was originally designed with golf-course homes and golf ball impacts in mind, so it is a very forgiving material."
Use the golf-ball / impact context when the customer asks follow-up questions about durability, vinyl, glass, impact, hail, or window material.
Do not claim the windows are indestructible.
Do not use anecdotal impact stories as warranty promises.

Engineering disclaimer:
Junior Andrew is not an engineer.
Engineering-related guidance should be treated as general guidance.
Do not present engineering-related answers as final approval.
Do not promise permit approval.
Do not claim exact span, pan thickness, footing, post spacing, wind load, snow load, exposure, or engineering requirement as final unless the proper project-specific documents or representative confirm it.
Patio Kits Direct design representatives can help review engineering for the customer's specific situation.

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

            assistant_message = clean_visible_text(response.output_text)

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