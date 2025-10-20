import threading, time, webview
from waitress import serve

from app import app

HOST = "127.0.0.1"
PORT = 5000
URL = f"http://{HOST}:{PORT}"

def run_server():
    serve(app, host=HOST, port=PORT)

if __name__ == "__main__":
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    time.sleep(0.4)

    webview.create_window("My Desktop", f"{URL}?db_name=example_db", width=1200, height=800)
    webview.start()
