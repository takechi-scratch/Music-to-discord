import json
import time
from math import floor
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        title = data["title"]
        artist = data["artist"]
        last_get = time.time()

        emit("message", json.dumps(data))


def rpc_run():
    global title
    global artist
    global last_set

    client_id = "1264115283140804628"
    RPC = Presence(client_id, pipe=0)
    RPC.connect()

    while True:
        RPC.update(details=title, state=artist, large_image="http://takechi.starfree.jp/Line_Music.png")
        last_set = time.time()
        time.sleep(15)


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
                print(f"正常に稼働中 最終設定:{floor(time.time() - last_set)}秒前 最終取得:{floor(time.time() - last_get)}秒前                           ")
            elif time.time() - last_set < 30:
                print("曲名を取得していません。Youtubeを開いて再生してみてください。                                      ")
            else:
                print("設定が行われていません。プログラムを再起動してください。                            ")
            print(f"曲名:{title} , チャンネル:{artist}                                                                      ")

            time.sleep(0.5)

            # input("あああ")

    # タスクが完了するまで待機
    for future in as_completed(futures):
        task = futures[future]
        try:
            print("正常に終了しました。")
        except Exception as e:
            logger.critical(f"エラーが発生しました（エラー: {e}, タスク: {task})")
