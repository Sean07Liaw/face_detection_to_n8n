from flask import Flask, request, jsonify
from werkzeug.serving import make_server
import queue
import threading

app = Flask(__name__)

# 建一個 queue 用來傳資料到 main thread
data_queue = queue.Queue()

# 定義 webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # 接收 JSON 資料
    # print("收到的資料:", data)
    print("Webhook received data")

    # 把資料放到 queue 裡
    data_queue.put(data)

    srv.received_data = data

    return jsonify({"status": "success"}), 200

class ServerThread(threading.Thread):
    def __init__(self, host, port, app):
        threading.Thread.__init__(self)
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()
        self.received_data = None

    def run(self):
        print("Starting server to receive webhook data...")
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

    def get_received_data(self, timeout=None):
        self.received_data = data_queue.get(timeout=timeout)

        # 清空 queue，避免下次呼叫時拿到舊資料
        while not data_queue.empty():
            try:
                data_queue.get_nowait()
            except queue.Empty:
                break

        return self.received_data

def run_server():
    global srv
    srv = ServerThread("0.0.0.0", 5000, app)
    srv.start()

def shutdown_server():
    global srv
    srv.shutdown()

def get_received_data(timeout=None):
    global srv
    return srv.get_received_data(timeout=timeout)

if __name__ == '__main__':
    srv = ServerThread("0.0.0.0", 5000, app)
    srv.start()
    # 這裡是 main thread，可以做別的事情
    import time
    time.sleep(10)

    print(srv.received_data)
    srv.shutdown()
    srv.join()
    print("Server 已關閉")
