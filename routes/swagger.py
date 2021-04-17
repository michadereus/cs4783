from flask import Blueprint, make_response, request, make_response, render_template
import sys
sys.path.append('../')
from util.response_builder import response_builder

swagger_bp = Blueprint('swagger', __name__)

@swagger_bp.route('/swagger.json')
def swagger():
    try:
        # res = response_builder(render_template('swagger.json'), 200)
        return response_builder(render_template('swagger.json'), 200)
    except:
        # res = make_response("response failure", 400)
        return response_builder("Failure to render swagger.json", 400)
