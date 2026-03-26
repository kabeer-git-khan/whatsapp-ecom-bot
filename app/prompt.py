from pathlib import Path

BUSINESS_INFO_PATH = Path(__file__).parent.parent / "data" / "business_info.txt"


def load_system_prompt() -> str:
    with open(BUSINESS_INFO_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_messages(history: list, user_message: str) -> list:
    system_prompt = load_system_prompt()

    messages = [{"role": "system", "content": system_prompt}]
    messages += history
    messages.append({"role": "user", "content": user_message})

    return messages