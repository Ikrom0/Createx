import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from admin import admin
from models import Admin, db
from routes import register_routes
from template_filters import register_template_filters

app = Flask(__name__)

load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SUPABASE_URL"] = os.getenv("SUPABASE_URL")
app.config["SUPABASE_SERVICE_KEY"] = os.getenv("SUPABASE_SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TELEGRAM_BOT_TOKEN"] = os.getenv("TELEGRAM_BOT_TOKEN")
app.config["TELEGRAM_CHAT_ID"] = os.getenv("TELEGRAM_CHAT_ID")

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(admin)

login_manager.login_view = "admin.login"

register_routes(app)
register_template_filters(app)


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


if __name__ == "__main__":
    app.run()
