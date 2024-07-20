import json
import time
from concurrent.futures import ThreadPoolExecutor

from pypresence import Presence
from flask import Flask
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
title = "未再生"
artist = "未再生"


@app.route("/", methods=["GET"])
def home():
    return "server is running!"


# データの送受信
@socketio.on("message")
def handle_message(data):
    global title
    global artist

    print(data)

    if data not in ["Ping", "Hello"]:
        title = data["title"]
        artist = data["artist"]

        emit("message", json.dumps(data))


def rpc_run():
    global title
    global artist

    client_id = "1264115283140804628"
    RPC = Presence(client_id, pipe=0)
    RPC.connect()

    while True:
        print(RPC.update(details=title, state=artist, large_image="http://takechi.starfree.jp/Line_Music.png"))  # Set the presence
        time.sleep(15)


def flask_run():
    socketio.run(app, port=8080)


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:  # 同時実行できるスレッド数の上限を設定
        futures = {executor.submit(task): task for task in [
            rpc_run,
            flask_run
        ]}
