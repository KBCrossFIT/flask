from flask import Flask
from portfolio.router.portfolio_routes import portfolio_routes

app = Flask(__name__)

app.register_blueprint(portfolio_routes)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)