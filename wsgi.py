import os

try:
    import eventlet
    eventlet.monkey_patch()
except Exception:
    pass

from app import create_app, db
from app.db.migrator import SchemaMigrator
from app.db.seeder import DatabaseSeeder

app = create_app()

if not os.environ.get("VERCEL"):
    try:
        with app.app_context():
            SchemaMigrator(db, app).run()
            DatabaseSeeder(db, app).run()
    except Exception as err:
        print(f"Startup migration warning: {err}")

if __name__ == "__main__":
    app.run()
