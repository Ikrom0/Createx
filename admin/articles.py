from flask import jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from models import Article, db
from utils import delete_image, generate_unique_slug, save_images
from validators.forms import validate_article

from . import admin


@admin.route("/articles")
@login_required
def articles():
    articles = Article.query.order_by(Article.date.desc()).all()

    return render_template("admin/articles.html", articles=articles)


@admin.route("/articles/create", methods=["GET", "POST"])
@login_required
def create_article():
    if request.method == "POST":
        article_data = {
            "title": request.form.get("title", "").strip(),
            "category": request.form.get("category", "").strip(),
            "content": request.form.get("content", "").strip(),
        }

        images = {
            "image_sm": request.files.get("image_sm"),
            "image_lg": request.files.get("image_lg"),
        }

        errors = validate_article(article_data, images, is_create=True)

        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        image_paths = save_images(images, "uploads/articles")

        slug = generate_unique_slug(Article, article_data["title"])

        article = Article(
            **article_data,
            slug=slug,
            image_lg=image_paths["image_lg"],
            image_sm=image_paths["image_sm"],
        )

        db.session.add(article)
        db.session.commit()

        return jsonify(
            {"success": True, "redirect_url": url_for("admin.articles")}
        ), 201

    return render_template(
        "admin/article_form.html",
        page_title="Create article",
        page_subtitle="Add a new article and publish it to your website.",
    )


@admin.route("/articles/<slug>/edit", methods=["GET", "POST"])
@login_required
def edit_article(slug):
    article = Article.query.filter_by(slug=slug).first_or_404()

    if request.method == "POST":
        article_data = {
            "title": request.form.get("title", "").strip(),
            "category": request.form.get("category", "").strip(),
            "content": request.form.get("content", "").strip(),
        }

        images = {
            "image_sm": request.files.get("image_sm"),
            "image_lg": request.files.get("image_lg"),
        }

        old_image_sm = article.image_sm
        old_image_lg = article.image_lg

        errors = validate_article(article_data, images)

        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        article.title = article_data["title"]
        article.slug = generate_unique_slug(Article, article_data["title"], article.id)
        article.category = article_data["category"]
        article.content = article_data["content"]

        image_paths = save_images(images, "uploads/articles")

        if "image_sm" in image_paths:
            article.image_sm = image_paths["image_sm"]

        if "image_lg" in image_paths:
            article.image_lg = image_paths["image_lg"]

        db.session.commit()

        if images["image_sm"] and images["image_sm"].filename:
            delete_image(old_image_sm, "uploads/articles/")

        if images["image_lg"] and images["image_lg"].filename:
            delete_image(old_image_lg, "uploads/articles/")

        return jsonify(
            {"success": True, "redirect_url": url_for("admin.articles")}
        ), 201

    return render_template(
        "admin/article_form.html",
        article=article,
        page_title="Edit article",
        page_subtitle="Update the article information and details.",
    )


@admin.route("/articles/<int:id>/delete", methods=["POST"])
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)

    images = (article.image_sm, article.image_lg)

    db.session.delete(article)
    db.session.commit()

    for image in images:
        delete_image(image, "uploads/articles/")

    return redirect(url_for("admin.articles"))
