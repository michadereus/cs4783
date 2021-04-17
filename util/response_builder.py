from flask import make_response

def response_builder(res, res_num):
    response = make_response(res, res_num)
    response.headers.add('Content-Type', 'application/json')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Allow-*', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, api_key, Authorization')
    return response