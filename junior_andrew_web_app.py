from pathlib import Path
import os

import streamlit as st
from openai import OpenAI

BASE_DIR = Path(__file__).parent

try:
    openai_api_key = st.secrets.get("OPENAI_API_KEY", None)
except Exception:
    openai_api_key = None

if not openai_api_key:
    openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

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

with st.sidebar:
    st.header("Controls")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.write("Model: `gpt-5.5`")
    st.write("Knowledge files loaded:")

    for file in KNOWLEDGE_FILES:
        if file.exists():
            st.write("✅ " + file.name)
        else:
            st.write("❌ " + file.name)

    if openai_api_key:
        st.write("API key: ✅ loaded")
    else:
        st.write("API key: ❌ missing")

if not openai_api_key:
    st.error("OPENAI_API_KEY is missing. Add it as a Streamlit secret or Windows environment variable.")
    st.stop()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

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