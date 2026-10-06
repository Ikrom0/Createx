from flask import render_template
from flask_login import login_required

from models import ArticleComment, CareerApplication, Request, Subscriber

from . import admin


@admin.route("/")
@login_required
def dashboard():
    stats = {
        "requests": Request.query.count(),
        "career_applications": CareerApplication.query.count(),
        "subscribers": Subscriber.query.count(),
        "comments": ArticleComment.query.count(),
    }

    latest_requests = Request.query.order_by(Request.created_at.desc()).limit(5).all()

    latest_comments = (
        ArticleComment.query.order_by(ArticleComment.date.desc()).limit(5).all()
    )

    latest_applications = (
        CareerApplication.query.order_by(CareerApplication.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        latest_requests=latest_requests,
        latest_comments=latest_comments,
        latest_applications=latest_applications,
    )










