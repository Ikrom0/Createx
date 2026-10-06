import os
import tempfile
import uuid

from slugify import slugify

from supabase_client import supabase


def generate_unique_slug(model, value, current_id=None) -> str:
    base_slug = slugify(value)
    slug = base_slug
    counter = 2

    query = model.query

    if current_id:
        query = query.filter(model.id != current_id)

    while query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


def generate_filename(filename: str) -> str:
    extension = filename.rsplit(".", 1)[1].lower()
    return f"{uuid.uuid4().hex}.{extension}"


def allowed_filename(filename: str, extension_type: str) -> bool:
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    if extension_type == "image":
        return extension in ("jpg", "jpeg", "png", "webp")

    if extension_type == "document":
        return extension in ("pdf", "doc", "docx")

    return False


def save_images(images: dict, path: str) -> dict:
    image_paths = {}

    for field, file in images.items():
        if not file or not file.filename:
            continue

        filename = generate_filename(file.filename)
        storage_path = f"{path}/{filename}"

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        try:
            supabase.storage.from_("uploads").upload(
                storage_path, temp_path, {"content-type": file.content_type}
            )
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        image_paths[field] = storage_path

    return image_paths


def delete_image(image: str | None, path: str) -> None:
    if not image:
        return

    if not image.startswith(path):
        return

    supabase.storage.from_("uploads").remove([image])


def delete_cv(path: str | None) -> None:
    if not path:
        return

    if not path.startswith("uploads/cv/"):
        return

    storage_path = path.removeprefix("uploads/")

    supabase.storage.from_("uploads").remove([storage_path])
