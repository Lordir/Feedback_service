from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app import app
from models import *

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Feedback service admin', template_mode='bootstrap3')
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Reviews, db.session))
admin.add_view(ModelView(Category, db.session))
