from flask import Blueprint

# Create blueprint
main = Blueprint('main', __name__)

# Don't import routes here, but in the create_app function
# This avoids circular import problems