import re

from email_validator import EmailNotValidError, validate_email

OPTIONS = {
    "cities": ("New York", "New Jersey", "San Francisco"),
    "contacts": ("Phone", "Email", "Telegram"),
    "articles": ("Company News", "Innovation", "Industry News", "Expert Tips", "Marketing"),
    "projects": ("Interior Design", "Project Development", "Construction", "Repairs"),
    "subtitles": ("Apartments Flats", "Business Centers", "Private Houses", "Stores Malls")
}

def validate_required_fields(fields: dict, errors: dict, required_fields: list[str] | None = None) -> None:
    if required_fields is None:
        required_fields = fields
    
    
    for field in required_fields:
        if not fields[field]:
            errors[field] = f"{field.capitalize()} is required."


def validate_name(name: str, errors: dict) -> None:
    if "name" not in errors:
        if len(name) < 3 or len(name) > 50:
            errors["name"] = "Name must be between 3 and 50 characters."


def validate_phone(phone: str, errors: dict) -> None:
    digits = re.sub(r"\D", "", phone)
    if "phone" not in errors:
        if len(digits) < 7 or len(digits) > 20:
            errors["phone"] = "Phone must contain between 7 and 20 digits."


def validate_email_field(email: str, errors: dict) -> None:
    if not email:
        return

    if "email" not in errors:
        try:
            validate_email(email)
        except EmailNotValidError:
            errors["email"] = "Please enter a valid email address."


def validate_message(message: str, errors: dict) -> None:
    if not message:
        return

    if "message" not in errors:
        if len(message) < 10 or len(message) > 2000:
            errors["message"] = "Message must be between 10 and 2000 characters."


def validate_options(field: str, value: str, option: str, errors: dict) -> None:
    if field not in errors:
        if value not in OPTIONS[option]:
            errors[field] = "Please select a valid option."
