from app import app


@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    # avoid circular imports
    from app.database.db import db
    db.init_app(app)
    app.run(debug=True)
