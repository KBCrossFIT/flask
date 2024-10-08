from flask import Blueprint, jsonify

portfolio_routes = Blueprint('portfolio_routes', __name__)
text = "asdf"

# 기본 라우트
@portfolio_routes.route('/calculate', methods=['GET'])
def calculate():
    
    return text
