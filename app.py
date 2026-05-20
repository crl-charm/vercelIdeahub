import os

from app import create_app, db, socketio
from app.db.migrator import SchemaMigrator
from app.db.seeder import DatabaseSeeder

app = create_app()

if not os.environ.get("VERCEL"):
    with app.app_context():
        SchemaMigrator(db, app).run()
        DatabaseSeeder(db, app).run()


if __name__ == "__main__":
    # Disable debug mode in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    socketio.run(app, host="0.0.0.0", port=5000, debug=debug_mode)