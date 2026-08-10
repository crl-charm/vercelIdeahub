import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app

app = create_app()
with app.test_client() as client:
    # ensure cookies included if needed
    resp = client.get('/admin/daily-balance/api/today-stats')
    print('status', resp.status_code)
    try:
        print(resp.get_json())
    except Exception:
        print(resp.get_data(as_text=True))
