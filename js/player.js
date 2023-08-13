function onYouTubeIframeAPIReady() {

  const playerContainers = document.querySelectorAll('.youtube-audio');

  playerContainers.forEach(container => {

    var icon = document.createElement("img");
    icon.setAttribute("class", "youtube-icon");
    icon.style.cssText = "cursor: pointer; cursor: hand";
    icon.src = "images/loading.png";
    container.appendChild(icon);

    var imageSize = "30px"; // Adjust the sizes as needed
    icon.style.width = imageSize;
    icon.style.height = imageSize;


    var playerContainer = document.createElement("div");
    playerContainer.setAttribute("class", "youtube-player");
    container.appendChild(playerContainer);

    var updateIcon = function(isPlaying) {
        var iconSrc = isPlaying ? "pause.png" : "play.png"; // Use the actual filenames
        icon.setAttribute("src", "images/" + iconSrc); // Specify the relative path
    };

    var player;
    icon.onclick = function() {
        if (player.getPlayerState() === YT.PlayerState.PLAYING || player.getPlayerState() === YT.PlayerState.BUFFERING) {
            player.pauseVideo();
            updateIcon(false);
        } else {
            player.playVideo();
            updateIcon(true);
        }
    };

    player = new YT.Player(playerContainer, {
        height: "0",
        width: "0",
        videoId: container.getAttribute('data-video'),
        playerVars: {
            autoplay: container.getAttribute('data-autoplay'),
            loop: container.getAttribute('data-loop')
        },
        events: {
            onReady: function(event) {
                player.setPlaybackQuality("small");
                updateIcon(player.getPlayerState() !== YT.PlayerState.CUED);
            },
            onStateChange: function(event) {
                if (event.data === YT.PlayerState.ENDED) {
                    updateIcon(false);
                }
            }
        }
    });
  });
}
