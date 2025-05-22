import threading
import time
from app import app, notify_listeners


def test_stream_headers():
    with app.test_client() as client:
        resp = client.get('/stream')
        assert resp.status_code == 200
        assert resp.headers['Content-Type'].startswith('text/event-stream')
        assert resp.headers['Cache-Control'] == 'no-cache'
        assert resp.headers['X-Accel-Buffering'] == 'no'
        resp.close()


def test_stream_broadcast():
    def send_msg():
        time.sleep(0.1)
        notify_listeners({'id': 1, 'title': 'Test', 'message': 'hello'})

    with app.test_client() as client:
        thread = threading.Thread(target=send_msg)
        thread.start()
        resp = client.get('/stream', buffered=True)
        data = next(resp.response).decode('utf-8')
        thread.join()
        assert 'data:' in data
        resp.close()


