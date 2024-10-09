from flask import Flask
from flask_cors import CORS
from portfolio.router.portfolio_routes import portfolio_routes
from persona.router.persona_routes import persona_routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(portfolio_routes)
app.register_blueprint(persona_routes)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)


