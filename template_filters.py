from datetime import date

from flask import url_for

from supabase_client import supabase


def register_template_filters(app):
    @app.template_filter("format_comments")
    def format_comment(value: int) -> str:
        if value == 1:
            return f"{value} comment"
        elif value > 1:
            return f"{value} comments"
        return "No comments"

    @app.template_filter("format_date")
    def format_date(value: date) -> str:
        return value.strftime("%B %d, %Y")

    @app.template_filter("image_url")
    def image_url(path: str | None) -> str | None:
        if not path:
            return None

        if path.startswith("uploads/articles/") or path.startswith("uploads/projects/"):
            return supabase.storage.from_("uploads").get_public_url(path)

        return url_for("static", filename=path)
