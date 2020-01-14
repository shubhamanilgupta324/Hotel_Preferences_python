from flask import Flask
import data_scraping


def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app

def register_blueprints(app):
    app.register_blueprint(data_scraping.blueprint)
    return None

if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=8000)
