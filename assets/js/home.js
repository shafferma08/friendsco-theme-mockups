/* ==========================================================================
   Friends & Co — home page behaviour
   Hero video mute toggle + "Why friendship" accessible tab panel.
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

  // Tab panel — Why Friendship
  var tabs = Array.from(document.querySelectorAll('.tab-btn'));
  var panels = Array.from(document.querySelectorAll('.tab-panel'));

  function activateTab(idx){
    tabs.forEach(function(t,i){
      var selected = i === idx;
      t.setAttribute('aria-selected', selected);
      t.tabIndex = selected ? 0 : -1;
      panels[i].classList.toggle('is-active', selected);
      if(selected) panels[i].removeAttribute('hidden');
      else panels[i].setAttribute('hidden','');
    });
  }

  tabs.forEach(function(tab, i){
    tab.addEventListener('click', function(){ activateTab(i); });
    tab.addEventListener('keydown', function(e){
      if(e.key === 'ArrowRight'){
        e.preventDefault();
        var next = (i+1) % tabs.length;
        tabs[next].focus(); activateTab(next);
      } else if(e.key === 'ArrowLeft'){
        e.preventDefault();
        var prev = (i-1+tabs.length) % tabs.length;
        tabs[prev].focus(); activateTab(prev);
      } else if(e.key === 'Home'){
        e.preventDefault(); tabs[0].focus(); activateTab(0);
      } else if(e.key === 'End'){
        e.preventDefault(); tabs[tabs.length-1].focus(); activateTab(tabs.length-1);
      }
    });
  });
})();
