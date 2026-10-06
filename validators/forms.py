from datetime import datetime

from werkzeug.datastructures import FileStorage

from models import Admin, Subscriber

from .common import (
    validate_email_field,
    validate_message,
    validate_name,
    validate_options,
    validate_phone,
    validate_required_fields,
)
from .files import validate_cv, validate_images


def validate_admin(fields: dict) -> dict:
    errors = {}

    validate_required_fields(fields, errors)

    if errors:
        return errors

    admin = Admin.query.filter_by(username=fields["username"]).first()

    if not admin or not admin.check_password(fields["password"]):
        errors["password"] = "Invalid username or password."

    return errors


def validate_project(project_data: dict, images: dict, is_create: bool = False) -> dict:
    errors = {}
    image_dimensions = {
        "card_img": (780, 880),
        "image_sm": (100, 100),
        "image_lg": (1230, 500)
    }

    validate_required_fields(project_data, errors)

    for field in ["size", "price"]:
        if project_data.get(field):
            try:
                project_data[field] = int(project_data[field])

                if project_data[field] <= 0:
                    errors[field] = f"{field.capitalize()} must be greater than 0."

            except ValueError:
                errors[field] = f"{field.capitalize()} must be a valid number."

    subtitle = project_data.get("subtitle")
    if subtitle:
        validate_options("subtitle", subtitle, "subtitles", errors)

    category = project_data.get("category")
    if category:
        validate_options("category", category, "projects", errors)

    goal = project_data.get("goal")
    if goal and len(goal) > 500:
        errors["goal"] = "Goal must be 500 characters or less."

    city = project_data.get("city")
    if city:
        validate_options("city", city, "cities", errors)

    address = project_data.get("address")
    if address and len(address) > 100:
        errors["address"] = "Address must be 100 characters or less."

    date = project_data.get("date")
    if date:
        try:
            project_data["date"] = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            errors["date"] = "Date must be valid."

    errors.update(validate_images(images, image_dimensions, is_create))

    return errors


def validate_article(article_data: dict, images: dict, is_create: bool = False) -> dict:
    errors = {}
    image_dimensions = {
        "image_sm": (600, 306),
        "image_lg": (1230, 500)
    }

    validate_required_fields(article_data, errors)

    title = article_data.get("title")
    if title and len(title) > 100:
        errors["title"] = "Title must be 100 characters or less."

    category = article_data.get("category")
    if category:
        validate_options("category", category, "articles", errors)

    content = article_data.get("content")
    if content and len(content) > 20000:
        errors["content"] = "Content must be 20000 characters or less."

    errors.update(validate_images(images, image_dimensions, is_create))

    return errors


def validate_comment(fields: dict) -> dict:
    errors = {}

    validate_required_fields(fields, errors)

    validate_name(fields["name"], errors)
    validate_email_field(fields["email"], errors)
    validate_message(fields["message"], errors)

    return errors


def validate_career(fields: dict, cv_file: FileStorage | None) -> dict:
    errors = {}

    validate_required_fields(fields, errors, ["name", "city", "phone", "email"])

    validate_name(fields["name"], errors)
    validate_phone(fields["phone"], errors)
    validate_email_field(fields["email"], errors)
    validate_options("city", fields["city"], "cities", errors)
    validate_message(fields["message"], errors)
    errors.update(validate_cv(cv_file))

    return errors


def validate_subscriber(fields: dict) -> dict:
    errors = {}

    name = fields["name"]
    email = fields["email"]
    subscribe_type = fields["subscribe_type"]

    if subscribe_type == "modal":
        if not name:
            errors["name"] = "Name is required."
        else:
            validate_name(name, errors)

    validate_email_field(email, errors)

    if not email:
        errors["email"] = "Email is required."

    if "email" not in errors:
        subscriber = Subscriber.query.filter_by(email=email).first()

        if subscriber:
            errors["email"] = "This email is already subscribed."

    return errors


def validate_request(fields: dict) -> dict:
    errors = {}

    name = fields["name"]
    phone = fields["phone"]
    email = fields["email"]
    message = fields["message"]
    request_type = fields["type"]

    required_fields = ["name", "phone", "message"]

    if request_type == "contact":
        category = fields["category"]
        city = fields["city"]
        contact = fields["contact"]
        required_fields.extend(["category", "city", "contact"])

        if contact == "Email":
            required_fields.append("email")

    validate_required_fields(fields, errors, required_fields)

    if request_type == "contact":
        validate_options("contact", contact, "contacts", errors)
        validate_options("city", city, "cities", errors)
        validate_options("category", category, "projects", errors)


    validate_name(name, errors)
    validate_phone(phone, errors)
    validate_email_field(email, errors)
    validate_message(message, errors)

    return errors













