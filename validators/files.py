import os

from PIL import Image, UnidentifiedImageError
from werkzeug.datastructures import FileStorage

from utils import allowed_filename

MAX_FILE_SIZE = 5 * 1024 * 1024

def validate_images(images: dict, dimensions: dict, is_create: bool = False) -> dict:
    errors = {}

    for field, file in images.items():
        if not file or not file.filename:
            if is_create:
                errors[field] = "Image is required."

            continue

        if not allowed_filename(file.filename, "image"):
            errors[field] = "Invalid image format."
            continue

        errors.update(validate_file_size(file, field))

        if field in errors:
            continue

        try:
            with Image.open(file.stream) as image:
                width, height = image.size

                max_width, max_height = dimensions[field]

                if width > max_width or height > max_height:
                    errors[field] = (
                        f"Image dimensions must not exceed "
                        f"{max_width}x{max_height} pixels."
                    )

        except UnidentifiedImageError:
            errors[field] = "Invalid image file."

        finally:
            file.stream.seek(0)
        
    return errors


def validate_file_size(file: FileStorage, field: str) -> dict:
    errors = {}

    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)

    if size == 0:
        errors[field] = "The uploaded file is empty."
    elif size > MAX_FILE_SIZE:
        errors[field] = "The file must not exceed 5 MB."

    return errors


def validate_cv(cv_file: FileStorage | None) -> dict:
    errors = {}

    if not cv_file or cv_file.filename == "":
        errors["cv_file"] = "Please attach your CV."
        return errors

    if not allowed_filename(cv_file.filename, "document"):
        errors["cv_file"] = "Only PDF, DOC and DOCX files are allowed."
        return errors

    errors.update(validate_file_size(cv_file, "cv_file"))

    return errors







