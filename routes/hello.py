from flask import Blueprint, request
import sys
sys.path.append('../')
from util.response_builder import build_response

hello_bp = Blueprint('hello', __name__)

@hello_bp.route('/hello', methods=['GET'])
def hello():
    if request.method == 'GET':
        return build_response({"message":"hello yourself"},200)
    else:
        return build_response({"message":"error"}, 400)