from flask import jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from models import Project, db
from utils import delete_image, generate_unique_slug, save_images
from validators.forms import validate_project

from . import admin


@admin.route("/projects")
@login_required
def projects():
    projects = Project.query.order_by(Project.date.desc()).all()

    return render_template("admin/projects.html", projects=projects)


@admin.route("/projects/create", methods=["GET", "POST"])
@login_required
def create_project():
    if request.method == "POST":
        project_data = {
            "title": request.form.get("title", "").strip(),
            "subtitle": request.form.get("subtitle", "").strip(),
            "category": request.form.get("category", "").strip(),
            "goal": request.form.get("goal", "").strip(),
            "city": request.form.get("city", "").strip(),
            "address": request.form.get("address", "").strip(),
            "client": request.form.get("client", "").strip(),
            "architect": request.form.get("architect", "").strip(),
            "size": request.form.get("size", "").strip(),
            "price": request.form.get("price", "").strip(),
            "date": request.form.get("date", "").strip(),
        }

        images = {
            "card_img": request.files.get("card_img"),
            "image_sm": request.files.get("image_sm"),
            "image_lg": request.files.get("image_lg"),
        }

        errors = validate_project(project_data, images, is_create=True)

        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        image_paths = save_images(images, "uploads/projects")

        slug = generate_unique_slug(Project, project_data["title"])

        project = Project(
            **project_data,
            slug=slug,
            card_img=image_paths["card_img"],
            image_lg=image_paths["image_lg"],
            image_sm=image_paths["image_sm"],
        )

        db.session.add(project)
        db.session.commit()

        return jsonify(
            {"success": True, "redirect_url": url_for("admin.projects")}
        ), 201

    return render_template(
        "admin/project_form.html",
        page_title="Create project",
        page_subtitle="Add a new project to your portfolio.",
    )


@admin.route("/projects/<slug>/edit", methods=["GET", "POST"])
@login_required
def edit_project(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()

    if request.method == "POST":
        project_data = {
            "title": request.form.get("title", "").strip(),
            "subtitle": request.form.get("subtitle", "").strip(),
            "category": request.form.get("category", "").strip(),
            "goal": request.form.get("goal", "").strip(),
            "city": request.form.get("city", "").strip(),
            "address": request.form.get("address", "").strip(),
            "client": request.form.get("client", "").strip(),
            "architect": request.form.get("architect", "").strip(),
            "size": request.form.get("size", "").strip(),
            "price": request.form.get("price", "").strip(),
            "date": request.form.get("date", "").strip(),
        }

        images = {
            "card_img": request.files.get("card_img"),
            "image_sm": request.files.get("image_sm"),
            "image_lg": request.files.get("image_lg"),
        }

        errors = validate_project(project_data, images)

        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        old_card_img = project.card_img
        old_image_lg = project.image_lg
        old_image_sm = project.image_sm

        project.title = project_data["title"]
        project.slug = generate_unique_slug(Project, project_data["title"], project.id)
        project.subtitle = project_data["subtitle"]
        project.category = project_data["category"]
        project.goal = project_data["goal"]
        project.city = project_data["city"]
        project.address = project_data["address"]
        project.client = project_data["client"]
        project.architect = project_data["architect"]
        project.size = project_data["size"]
        project.price = project_data["price"]
        project.date = project_data["date"]

        image_paths = save_images(images, "uploads/projects")

        if "card_img" in image_paths:
            project.card_img = image_paths["card_img"]

        if "image_sm" in image_paths:
            project.image_sm = image_paths["image_sm"]

        if "image_lg" in image_paths:
            project.image_lg = image_paths["image_lg"]

        db.session.commit()

        if images["card_img"] and images["card_img"].filename:
            delete_image(old_card_img, "uploads/projects/")

        if images["image_sm"] and images["image_sm"].filename:
            delete_image(old_image_sm, "uploads/projects/")

        if images["image_lg"] and images["image_lg"].filename:
            delete_image(old_image_lg, "uploads/projects/")

        return jsonify(
            {"success": True, "redirect_url": url_for("admin.projects")}
        ), 201

    return render_template(
        "admin/project_form.html",
        project=project,
        page_title="Edit project",
        page_subtitle="Update the project information and details.",
    )


@admin.route("/projects/<int:id>/delete", methods=["POST"])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)

    images = (project.card_img, project.image_sm, project.image_lg)

    db.session.delete(project)
    db.session.commit()

    for image in images:
        delete_image(image, "uploads/projects/")

    return redirect(url_for("admin.projects"))
