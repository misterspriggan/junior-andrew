from pathlib import Path

APP_FILE = Path(r"C:\AI-Mailbox-Analysis\junior_andrew_deploy\junior_andrew_web_app.py")

text = APP_FILE.read_text(encoding="utf-8")

old_audio_block = '''    # This is the exact spoken pattern that tested best in ElevenLabs:
    # "A Haven l'nai is Patio Kits Direct's fully enclosed option."
    # Visible text still shows "Haven Lanai."
    spoken = re.sub(r"\\bHaven Lanai\\b", "Haven l'nai", spoken, flags=re.IGNORECASE)

    # Company pronunciation helper.
'''

new_audio_block = '''    # This is the exact spoken pattern that tested best in ElevenLabs:
    # "A Haven l'nai is Patio Kits Direct's fully enclosed option."
    # Visible text still shows "Haven Lanai."
    spoken = re.sub(r"\\bHaven Lanai\\b", "Haven l'nai", spoken, flags=re.IGNORECASE)

    # ElevenLabs sometimes pronounces the product name worse if it is the very first sound.
    # If the audio starts with Haven l'nai, add a small natural warm-up word in audio only.
    # Visible text is not changed.
    spoken = re.sub(r"^\\s*Haven l'nai\\b", "So, Haven l'nai", spoken, flags=re.IGNORECASE)

    # Company pronunciation helper.
'''

if old_audio_block not in text:
    raise SystemExit("Could not find the current Haven Lanai audio block. Stop and ask ChatGPT for a full app replacement.")

text = text.replace(old_audio_block, new_audio_block)

old_prompt_block = '''Haven Lanai guidance:
Haven Lanai is Patio Kits Direct's fully enclosed option.
Always write the product name visibly as "Haven Lanai."
Do not write standalone "Lanai" when "Haven Lanai" would fit.
Always capitalize Haven Lanai.
Never write lowercase "lanai" or "lanais" in customer-facing text.
Never visibly write "l'nai", "la nai", "L anai", "L-anai", "la-nai", or any other pronunciation spelling.
Pronunciation helpers are only for hidden spoken audio, not visible text.
Do not use standard patio cover build instructions to explain how to build a Haven Lanai.
Haven Lanai has its own animated instructions in the 3D Designer for the customer's custom Haven Lanai.
If customers ask how to build a Haven Lanai, route them to the 3D Designer animated instructions and build support for project-specific guidance.
You may explain the general animated instruction roadmap if helpful.
'''

new_prompt_block = '''Haven Lanai guidance:
Haven Lanai is Patio Kits Direct's fully enclosed option.
Always write the product name visibly as "Haven Lanai."
Do not write standalone "Lanai" when "Haven Lanai" would fit.
Always capitalize Haven Lanai.
Never write lowercase "lanai" or "lanais" in customer-facing text.
Never visibly write "l'nai", "la nai", "L anai", "L-anai", "la-nai", or any other pronunciation spelling.
Pronunciation helpers are only for hidden spoken audio, not visible text.
When possible, do not start the very first sentence with "Haven Lanai." Start naturally, such as "It is..." or "Basically..." and mention Haven Lanai after a few words.
Do not use standard patio cover build instructions to explain how to build a Haven Lanai.
Haven Lanai has its own animated instructions in the 3D Designer for the customer's custom Haven Lanai.
If customers ask how to build a Haven Lanai, route them to the 3D Designer animated instructions and build support for project-specific guidance.
You may explain the general animated instruction roadmap if helpful.
'''

if old_prompt_block not in text:
    raise SystemExit("Could not find the Haven Lanai prompt block. Stop and ask ChatGPT for a full app replacement.")

text = text.replace(old_prompt_block, new_prompt_block)

APP_FILE.write_text(text, encoding="utf-8")

print("DONE")
print("Added audio-only warm-up before Haven l'nai when it starts the voice reply.")
print("Added prompt rule to avoid starting replies with Haven Lanai when possible.")