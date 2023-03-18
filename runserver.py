from api import create_app, db
from api.config.config import config_dict

app = create_app(config=config_dict['test'])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
