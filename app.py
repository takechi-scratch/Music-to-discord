import json
import time
from math import floor
from concurrent.futures import ThreadPoolExecutor

from pypresence import Presence
from flask import Flask
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
title = "未再生"
artist = "未再生"
last_set = 0
last_get = 0


@app.route("/", methods=["GET"])
def home():
    return "server is running!"


# データの送受信
@socketio.on("message")
def handle_message(data):
    global title
    global artist
    global last_get

    if data not in ["Ping", "Hello"]:
        title = data["title"] if data["title"] != "" else "未再生"
        artist = data["artist"] if data["artist"] != "" else "未再生"
        last_get = time.time()

        emit("message", json.dumps(data))


def rpc_run():
    global title
    global artist
    global last_set

    try:
        client_id = "1264115283140804628"
        RPC = Presence(client_id, pipe=0)
        RPC.connect()

        while True:
            if title == "未再生":
                RPC.update(details="再生していません", large_image="http://takechi.starfree.jp/Line_Music.png")
            else:
                RPC.update(details=title, state=artist, large_image="http://takechi.starfree.jp/Line_Music.png")
            last_set = time.time()
            time.sleep(15)
    except Exception as e:
        print(e)


def flask_run():
    socketio.run(app, port=8080)


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(task): task for task in [
            rpc_run,
            flask_run
        ]}
        print("起動ができました！少々お待ちください…")
        print("-" * 30 + "\n\n", end="")
        print()

        while True:
            print("\033[2A", end="")
            if time.time() - last_get < 10:
                print("正常に稼働中",
                      f"最終設定:{floor(time.time() - last_set)}秒前",
                      f"最終取得:{floor(time.time() - last_get)}秒前" + " "*30)
            elif time.time() - last_set < 30:
                print("曲名を取得していません。Youtubeを開いて再生してみてください。" + " "*30)
            else:
                print("設定が行われていません。プログラムを再起動してください。" + " " * 30)
            print(f"曲名:{title} , チャンネル:{artist}" + " " * 30)

            time.sleep(0.5)

            # input("あああ")
