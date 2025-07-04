import logging

logger = logging.getLogger("sender")


def logging_user_data(response):
    json_response_for_logging = response.copy()
    json_response_for_logging["account_hash"] = "***"
    logger.info(json_response_for_logging)


def save_token(token: str, env_path: str = ".env"):
    key = "CHAT_TOKEN"
    new_line = f"{key}={token}\n"
    lines = []

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    with open(env_path, "w", encoding="utf-8") as f:
        for line in lines:
            if not line.startswith(f"{key}="):
                f.write(line)
        f.write(new_line)


def clean_text(text: str) -> str:
    return text.replace("\n", "").replace("\r", "")
