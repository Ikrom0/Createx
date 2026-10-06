import os
import tempfile

from flask import (
    abort,
    jsonify,
    make_response,
    render_template,
    request,
)

from models import (
    Article,
    ArticleComment,
    CareerApplication,
    Project,
    Request,
    Subscriber,
    db,
)
from supabase_client import supabase
from telegram import send_telegram_notification
from utils import delete_cv, generate_filename
from validators.forms import (
    validate_career,
    validate_comment,
    validate_request,
    validate_subscriber,
)

SERVICES = {
    "construction": "Construction",
    "development": "Project Development",
    "interior-design": "Interior Design",
    "repairs": "Repairs",
}

PARTNERS = [
    "skema floor",
    "factory glass",
    "numark",
    "edwin international",
    "eiffage construction",
    "royal floor mats",
    "lovato",
    "basset",
    "x-rite",
    "lotte",
    "sennheiser",
    "exxon",
]


def register_routes(app):
    @app.errorhandler(404)
    def page_not_found(error):
        is_admin = request.path.startswith("/admin")

        return render_template("404.html", is_admin=is_admin), 404

    @app.route("/news/<slug>/comment", methods=["POST"])
    def create_comment(slug):
        article = Article.query.filter_by(slug=slug).first_or_404()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        form_data = {"name": name, "email": email, "message": message}

        errors = validate_comment(form_data)

        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        comment = ArticleComment(**form_data, article_id=article.id)

        try:
            db.session.add(comment)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return jsonify(
                {
                    "success": False,
                    "message": "Something went wrong. Please try again later.",
                }
            ), 500

        send_telegram_notification("New comment", comment)
        comments_count = len(article.comments)

        return jsonify(
            {
                "success": True,
                "message": "Comment posted successfully.",
                "comment": {
                    "name": comment.name,
                    "message": comment.message,
                    "date": comment.date.strftime("%B %d, %Y"),
                    "datetime": comment.date.strftime("%Y-%m-%d"),
                },
                "comments_count": (
                    f"{comments_count} comment"
                    if comments_count == 1
                    else f"{comments_count} comments"
                    if comments_count > 1
                    else "No comments"
                ),
            }
        ), 201

    @app.route("/career-application", methods=["POST"])
    def create_application():
        name = request.form.get("name", "").strip()
        city = request.form.get("city", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip() or None
        cv_file = request.files.get("cv_file")

        form_data = {
            "name": name,
            "city": city,
            "phone": phone,
            "email": email,
            "message": message,
        }

        errors = validate_career(form_data, cv_file)

        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        filename = generate_filename(cv_file.filename)
        storage_path = f"cv/{filename}"

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            cv_file.save(temp_path)

        try:
            supabase.storage.from_("uploads").upload(
                storage_path, temp_path, {"content-type": cv_file.content_type}
            )
        except Exception:
            return jsonify(
                {"success": False, "message": "Unable to save uploaded file."}
            ), 500
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        form_data["cv_file"] = f"uploads/{storage_path}"
        new_career = CareerApplication(**form_data)

        try:
            db.session.add(new_career)
            db.session.commit()
        except Exception:
            db.session.rollback()
            delete_cv(form_data["cv_file"])

            return jsonify(
                {
                    "success": False,
                    "message": "Something went wrong. Please try again later.",
                }
            ), 500

        send_telegram_notification(
            "New career application",
            new_career,
            form_data["cv_file"],
        )

        return jsonify({"success": True, "message": "Request sent successfully."}), 201

    @app.route("/subscribe", methods=["POST"])
    def create_subscriber():
        name = request.form.get("name", "").strip() or None
        email = request.form.get("email", "").strip()
        subscribe_type = request.form.get("type")

        form_data = {"name": name, "email": email, "subscribe_type": subscribe_type}

        errors = validate_subscriber(form_data)

        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        new_subscriber = Subscriber(name=name, email=email)

        try:
            db.session.add(new_subscriber)
            db.session.commit()

        except Exception:
            db.session.rollback()
            return jsonify(
                {
                    "success": False,
                    "message": "Something went wrong. Please try again later.",
                }
            ), 500

        send_telegram_notification("New subscriber", new_subscriber)

        return jsonify({"success": True, "message": "Thank you for subscribing!"}), 201

    @app.route("/request", methods=["POST"])
    def create_request():
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip() or None
        message = request.form.get("message", "").strip()
        request_type = request.form.get("type")
        category = request.form.get("category")
        city = request.form.get("city")
        contact = request.form.get("contact")

        form_data = {
            "name": name,
            "phone": phone,
            "email": email,
            "message": message,
            "type": request_type,
            "category": category,
            "city": city,
            "contact": contact,
        }

        errors = validate_request(form_data)

        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        new_request = Request(**form_data)

        try:
            db.session.add(new_request)
            db.session.commit()

        except Exception:
            db.session.rollback()
            return jsonify(
                {
                    "success": False,
                    "message": "Something went wrong. Please try again later.",
                }
            ), 500

        send_telegram_notification("New request", new_request)

        return jsonify({"success": True, "message": "Request sent successfully."}), 201

    @app.route("/")
    def home():
        news = Article.query.limit(3).all()
        projects = Project.query.limit(4).all()

        return render_template(
            "home.html", projects=projects, news=news, partners=PARTNERS[:6]
        )

    @app.route("/services")
    def services():
        return render_template("services.html", services=SERVICES)

    @app.route("/services/<slug>")
    def service(slug):
        service = SERVICES.get(slug)
        projects = Project.query.offset(5).limit(4).all()

        if not service:
            abort(404)

        return render_template(
            "service.html", service=service, projects=projects, partners=PARTNERS[6:]
        )

    @app.route("/work")
    def work():
        category = request.args.get("category", "all")
        page = request.args.get("page", 1, type=int)

        query = Project.query.order_by(Project.id)

        if category != "all":
            query = query.filter_by(category=category)

        projects = query.paginate(page=page, per_page=9, error_out=False)

        if page > projects.pages and projects.pages > 0:
            page = projects.pages
            projects = query.paginate(page=page, per_page=9, error_out=False)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            response = make_response(
                render_template(
                    "partials/_projects-list.html", projects=projects, category=category
                )
            )
            response.headers["Cache-Control"] = "no-store"
            return response

        return render_template(
            "work.html", projects=projects, partners=PARTNERS[4:10], category=category
        )

    @app.route("/work/<slug>")
    def project(slug):
        projects = Project.query.offset(8).limit(4).all()
        project = Project.query.filter_by(slug=slug).first_or_404()

        return render_template("project.html", project=project, projects=projects)

    @app.route("/about")
    def about():
        return render_template("about.html", partners=PARTNERS[::])

    @app.route("/career")
    def career():
        return render_template("career.html")

    @app.route("/contacts")
    def contacts():
        return render_template("contacts.html", discuss_style="discuss--hidden")

    @app.route("/news")
    def news():
        category = request.args.get("category", "all")
        page = request.args.get("page", 1, type=int)

        query = Article.query.order_by(Article.date.desc())

        if category != "all":
            query = query.filter_by(category=category)

        articles = query.paginate(page=page, per_page=6, error_out=False)

        if page > articles.pages and articles.pages > 0:
            page = articles.pages
            articles = query.paginate(page=page, per_page=6, error_out=False)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            response = make_response(
                render_template(
                    "partials/_news-cards.html", articles=articles, category=category
                )
            )
            response.headers["Cache-Control"] = "no-store"
            return response

        return render_template("news.html", articles=articles, category=category)

    @app.route("/news/<slug>")
    def article(slug):
        news = Article.query.limit(3).all()
        article = Article.query.filter_by(slug=slug).first_or_404()

        return render_template("article.html", article=article, news=news)
