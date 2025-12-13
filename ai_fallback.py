import subprocess

CHAT_HISTORY = []
MAX_HISTORY = 6   # last 6 turns (user + assistant)

def ai_reply(user_text):
    global CHAT_HISTORY

    CHAT_HISTORY.append(f"User: {user_text}")

    context = "\n".join(CHAT_HISTORY[-MAX_HISTORY:])

    prompt = f"""
You are a helpful assistant.
Reply briefly (1–2 lines).

Conversation so far:
{context}

Assistant:
"""

    result = subprocess.run(
        ["ollama", "run", "qwen2.5:1.5b"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        timeout=8
    )

    reply = result.stdout.decode("utf-8").strip()

    if reply:
        CHAT_HISTORY.append(f"Assistant: {reply}")

    return reply
