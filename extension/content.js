const socket = io.connect("http://localhost:8080");
const artist_Xpath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[1]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a"
let title
let artist

// YouTube用
if (window.location.host.includes('youtube.com')) {
    setInterval(() => {
        if (window.location.href.includes('youtube.com/watch')) {
            title = document.querySelector("#title > h1 > yt-formatted-string").innerText;
            artist = document.evaluate(artist_Xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerText;
        } else {
            title = ""
            artist = ""
        }
        data = {"title": title, "artist": artist}
        socket.emit("message", data);
        console.log(data)
    }, 1000);
    console.log("YouTube");

    // 操作画面と接続できたとき
    socket.on("connect", function () {
        console.log("WebSocketの接続完了");
        socket.send("Hello");

        // setInterval(function() {
        //     socket.send("Ping");
        // }, 2000);
    });

}

