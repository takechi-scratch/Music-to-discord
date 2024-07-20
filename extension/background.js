let nowPlayingInfo = {};

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'nowPlaying') {
    nowPlayingInfo[message.platform] = message.title;
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'getNowPlaying') {
    sendResponse(nowPlayingInfo);
  }
});
