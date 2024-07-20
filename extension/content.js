const socket = io.connect("http://localhost:8080");

// YouTube用
if (window.location.host.includes('youtube.com')) {
    setInterval(() => {
        console.log("title取得");
        let titleElement = document.querySelector("#title > h1 > yt-formatted-string");
        let artistElement = document.querySelector("#text > a")
        if (titleElement) {
            console.log(titleElement.innerText);
        }
        socket.emit("message", {"title": titleElement.innerText, "artist": artistElement.innerText});
        }, 1000);
        console.log("YouTube");

        // 操作画面と接続できたとき
    socket.on("connect", function() {
        console.log("WebSocketの接続完了");
        socket.send("Hello");

        // setInterval(function() {
        //     socket.send("Ping");
        // }, 2000);
    });

}

