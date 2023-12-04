from app import app, db
from app.views import seed_data

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)