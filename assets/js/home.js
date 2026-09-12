/* ==========================================================================
   Friends & Co — home page behaviour
   Hero video mute toggle. ("Why friendship" no longer needs script — it's a
   plain 3-up grid now instead of a click-to-reveal tab panel.)
   ========================================================================== */
(function(){
  // Mute/unmute button using YouTube IFrame API
  var player;
  var muted = true;
  var iconMute = document.getElementById('iconMute');
  var iconUnmute = document.getElementById('iconUnmute');
  var btn = document.getElementById('audioCtrl');

  window.onYouTubeIframeAPIReady = function(){
    player = new YT.Player('heroYT', {
      events:{
        onReady: function(e){
          e.target.mute();
          e.target.playVideo();
        }
      }
    });
  };

  if(btn){
    btn.addEventListener('click', function(){
      if(!player) return;
      if(muted){
        player.unMute();
        player.setVolume(60);
        muted = false;
        iconMute.style.display = 'none';
        iconUnmute.style.display = '';
        btn.setAttribute('aria-label','Mute background video');
      } else {
        player.mute();
        muted = true;
        iconMute.style.display = '';
        iconUnmute.style.display = 'none';
        btn.setAttribute('aria-label','Unmute background video');
      }
    });
  }
})();
