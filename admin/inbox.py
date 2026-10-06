import io

from flask import abort, redirect, render_template, send_file, url_for
from flask_login import login_required

from models import (
    ArticleComment,
    CareerApplication,
    Request,
    Subscriber,
    db,
)
from supabase_client import supabase
from utils import delete_cv

from . import admin


@admin.route("/requests")
@login_required
def requests():
    requests = Request.query.order_by(Request.created_at.desc()).all()

    return render_template("admin/requests.html", requests=requests)


@admin.route("/requests/<int:id>")
@login_required
def request_detail(id):
    request_item = Request.query.get_or_404(id)

    return render_template("admin/request.html", request_item=request_item)


@admin.route("/requests/<int:id>/delete", methods=["POST"])
@login_required
def delete_request(id):
    request = Request.query.get_or_404(id)

    db.session.delete(request)
    db.session.commit()

    return redirect(url_for("admin.requests"))


@admin.route("/careers")
@login_required
def careers():
    applications = CareerApplication.query.order_by(
        CareerApplication.created_at.desc()
    ).all()

    return render_template("admin/careers.html", applications=applications)


@admin.route("/careers/<int:id>")
@login_required
def career(id):
    application = CareerApplication.query.get_or_404(id)

    return render_template("admin/career.html", application=application)


@admin.route("/careers/<int:id>/delete", methods=["POST"])
@login_required
def delete_career(id):
    application = CareerApplication.query.get_or_404(id)

    cv_file = application.cv_file

    db.session.delete(application)
    db.session.commit()

    delete_cv(cv_file)

    return redirect(url_for("admin.careers"))


@admin.route("/careers/<int:id>/cv")
@login_required
def download_cv(id):
    application = CareerApplication.query.get_or_404(id)

    if not application.cv_file:
        abort(404)

    storage_path = application.cv_file.removeprefix("uploads/")

    file_data = supabase.storage.from_("uploads").download(storage_path)

    return send_file(
        io.BytesIO(file_data),
        as_attachment=True,
        download_name=storage_path.removeprefix("cv/"),
    )


@admin.route("/subscribers")
@login_required
def subscribers():
    subscribers = Subscriber.query.order_by(Subscriber.created_at.desc()).all()

    return render_template("admin/subscribers.html", subscribers=subscribers)


@admin.route("/subscriber/<int:id>/delete", methods=["POST"])
@login_required
def delete_subscriber(id):
    subscriber = Subscriber.query.get_or_404(id)

    db.session.delete(subscriber)
    db.session.commit()

    return redirect(url_for("admin.subscribers"))


@admin.route("/comments")
@login_required
def comments():
    comments = ArticleComment.query.order_by(ArticleComment.date.desc()).all()

    return render_template("admin/comments.html", comments=comments)


@admin.route("/comments/<int:id>/delete", methods=["POST"])
@login_required
def delete_comment(id):
    comment = ArticleComment.query.get_or_404(id)

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for("admin.comments"))
