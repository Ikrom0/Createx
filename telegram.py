import os
import tempfile

import requests
from flask import current_app

from supabase_client import supabase


def send_telegram_notification(title: str, data, filepath: str | None = None) -> None:
    try:
        telegram_message = f"<b>{title}</b>\n\n"

        if getattr(data, "name", None):
            telegram_message += f"👤 Name: {data.name}\n"

        if getattr(data, "phone", None):
            telegram_message += f"📞 Phone: {data.phone}\n"

        if getattr(data, "email", None):
            telegram_message += f"✉️ Email: {data.email}\n"

        if getattr(data, "location", None):
            telegram_message += f"📍 Location: {data.location}\n"

        if getattr(data, "interest", None):
            telegram_message += f"📂 Interest: {data.interest}\n"

        if getattr(data, "contact_method", None):
            telegram_message += f"☎️ Contact method: {data.contact_method}\n"

        if getattr(data, "message", None):
            telegram_message += f"\n💬 Message:\n{data.message}"

        send_telegram_message(telegram_message)

        if filepath:
            caption = f"<b>{data.name}</b>\n{data.email}"
            storage_path = filepath.removeprefix("uploads/")
            send_telegram_document(storage_path, caption)
    except Exception:
        current_app.logger.exception("Telegram notification failed")


def send_telegram_message(text: str) -> bool:
    token = current_app.config["TELEGRAM_BOT_TOKEN"]
    chat_id = current_app.config["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


def send_telegram_document(storage_path: str, caption: str = "") -> None:
    temp_path = None
    filename = storage_path.removeprefix("cv/")

    try:
        file_data = supabase.storage.from_("uploads").download(storage_path)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_data)
            temp_path = temp_file.name

        url = (
            f"https://api.telegram.org/bot"
            f"{current_app.config['TELEGRAM_BOT_TOKEN']}/sendDocument"
        )

        with open(temp_path, "rb") as document:
            response = requests.post(
                url,
                data={
                    "chat_id": current_app.config["TELEGRAM_CHAT_ID"],
                    "caption": caption,
                    "parse_mode": "HTML",
                },
                files={"document": (filename, document)},
                timeout=30,
            )

        response.raise_for_status()

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
