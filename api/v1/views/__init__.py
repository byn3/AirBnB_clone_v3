from flask import Blueprint
from models.base_model import BaseModel
app_views = Blueprint('app_views', '__name__', url_prefix='/api/v1')
from api.v1.views.index import *  # noqa: E402
