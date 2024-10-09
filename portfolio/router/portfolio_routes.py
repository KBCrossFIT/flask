from flask import Blueprint, request, jsonify
from portfolio.service.portfolio import calculate_portfolio

portfolio_routes = Blueprint('portfolio_routes', __name__)


@portfolio_routes.route('/api/portfolio/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400

    calculated_data = calculate_portfolio(data)

    return_data = jsonify(calculated_data)

    return return_data
