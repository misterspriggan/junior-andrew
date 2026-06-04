from pathlib import Path

BASE = Path(r"C:\AI-Mailbox-Analysis\junior_andrew_deploy")
APP_FILE = BASE / "junior_andrew_web_app.py"
HAVEN_FILE = BASE / "knowledge" / "haven_lanais_reference.txt"

app_text = APP_FILE.read_text(encoding="utf-8")

# Add stronger visible-text guardrails to the system prompt.
old_prompt_chunk = """Haven Lanai guidance:
Haven Lanais are Patio Kits Direct's fully enclosed options.
Do not use standard patio cover build instructions to explain how to build a Haven Lanai.
Haven Lanais have their own animated instructions in the 3D Designer for the customer's custom Lanai.
If customers ask how to build a Haven Lanai, route them to the 3D Designer animated instructions and build support for project-specific guidance.
You may explain the general animated instruction roadmap if helpful.
"""

new_prompt_chunk = """Haven Lanai guidance:
Haven Lanais are Patio Kits Direct's fully enclosed options.
Always write the product name visibly as "Haven Lanai" or "Haven Lanais."
Never visibly write "la nai", "L anai", "L-anai", "la-nai", or other pronunciation spellings in customer-facing text.
Pronunciation helpers are only for hidden spoken audio, not visible text.
Do not use standard patio cover build instructions to explain how to build a Haven Lanai.
Haven Lanais have their own animated instructions in the 3D Designer for the customer's custom Lanai.
If customers ask how to build a Haven Lanai, route them to the 3D Designer animated instructions and build support for project-specific guidance.
You may explain the general animated instruction roadmap if helpful.
"""

if old_prompt_chunk in app_text:
    app_text = app_text.replace(old_prompt_chunk, new_prompt_chunk)
elif "Never visibly write" not in app_text:
    raise SystemExit("Could not find Haven Lanai guidance block. Ask ChatGPT for a full file replacement.")

# Improve spoken pronunciation handling without changing visible text.
old_spoken_chunk = '''    # ElevenLabs pronunciation helper.
    # Visible text still says Lanai/Lanais, but spoken audio uses "la nai"
    # because "A Haven la nai is Patio Kits Direct's fully enclosed option."
    # tested as the best pronunciation.
    spoken = re.sub(r"\\bHaven Lanais\\b", "Haven la nai", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\\bHaven Lanai\\b", "Haven la nai", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\\bLanais\\b", "la nai", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\\bLanai\\b", "la nai", spoken, flags=re.IGNORECASE)

    # Company pronunciation helper.
'''

new_spoken_chunk = '''    # ElevenLabs pronunciation helper.
    # Visible text still says Lanai/Lanais, but spoken audio uses "la nai"
    # because "A Haven la nai is Patio Kits Direct's fully enclosed option."
    # tested as the best pronunciation.
    # Also catch accidental visible spacing like "L anai" so the voice does not say "L" + "anai."
    spoken = re.sub(r"\\bHaven\\s+L\\s+anais\\b", "Haven la nai", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\\bHaven\\s+L\\s+anai\\b", "Haven la nai", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\\bHaven\\s+Lanais\\b", "Haven la nai", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\\bHaven\\s+Lanai\\b", "Haven la nai", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\\bL\\s+anais\\b", "la nai", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\\bL\\s+anai\\b", "la nai", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\\bLanais\\b", "la nai", spoken, flags=re.IGNORECASE)
    spoken = re.sub(r"\\bLanai\\b", "la nai", spoken, flags=re.IGNORECASE)

    # Company pronunciation helper.
'''

if old_spoken_chunk in app_text:
    app_text = app_text.replace(old_spoken_chunk, new_spoken_chunk)
elif "Haven\\s+L\\s+anai" not in app_text:
    raise SystemExit("Could not find old spoken pronunciation block. Ask ChatGPT for a full file replacement.")

APP_FILE.write_text(app_text, encoding="utf-8")


haven_text = HAVEN_FILE.read_text(encoding="utf-8")

flexiglaze_note = """
FLEXIGLAZE CUSTOMER WORDING AND IMPACT CONTEXT

When explaining Haven Lanai windows, do not lead with wording that makes the vinyl sound cheap or flimsy.

Do not casually say only:
"the windows are flexible vinyl"

Better framing:

"The windows have a glass-like look, but they use a flexible FlexiGlaze vinyl material instead of glass. It was originally designed with golf-course homes and golf ball impacts in mind, so it is a very forgiving material."

Useful follow-up context:

- FlexiGlaze looks like glass, but it is not glass.
- It is a transparent flexible vinyl membrane.
- It is designed to handle impacts better than a rigid brittle material.
- Good examples include golf balls, baseballs, and hail.
- The material can absorb certain impacts and return to shape.
- A customer even shared that a ladder hit the window after a fall and the window absorbed the impact without damage and went back to shape.
- Do not present the ladder story as a formal warranty promise.
- Use the ladder story only as an anecdotal example if it naturally fits the conversation.

Good first explanation:

"Haven Lanai windows have a glass-like look, but they are not glass. They use a flexible FlexiGlaze vinyl material that was originally designed with golf-course homes and golf ball impacts in mind, so it is a very forgiving material."

Good follow-up if the customer asks whether vinyl is durable:

"That is a fair question. It is not vinyl in the cheap sense people sometimes picture. The FlexiGlaze material was designed for impact forgiveness — think golf balls, baseballs, and hail — so it can absorb certain impacts and return to shape."

Good follow-up if the customer worries it is not glass:

"That is actually part of why the system can be lighter and more affordable than a traditional glass sunroom. It still gives a glass-like look, but the material is more forgiving than glass."

Bad:

"They are just flexible vinyl windows."

Bad:

"It is basically plastic."

Bad:

"They are indestructible."

Bad:

"A ladder can hit it and it will never damage it."

Bad:

"The windows are guaranteed to survive any impact."
"""

if "FLEXIGLAZE CUSTOMER WORDING AND IMPACT CONTEXT" not in haven_text:
    haven_text = haven_text.rstrip() + "\n\n" + flexiglaze_note.strip() + "\n"

HAVEN_FILE.write_text(haven_text, encoding="utf-8")

print("DONE")
print("Updated app visible Lanai guardrails.")
print("Updated app spoken Lanai pronunciation handling.")
print("Added FlexiGlaze customer wording and impact context.")