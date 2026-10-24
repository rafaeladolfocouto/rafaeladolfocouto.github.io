(function(){
  var r=document.documentElement,t='dark';
  try{var v=localStorage.getItem('rc-theme');if(v==='light'||v==='dark')t=v;}catch(e){}
  r.setAttribute('data-theme',t);
  var L=(r.getAttribute('lang')||'pt').slice(0,2);
  var N={pt:['\u263e escuro','\u2600 claro'],en:['\u263e dark','\u2600 light'],es:['\u263e oscuro','\u2600 claro']}[L]||['\u263e escuro','\u2600 claro'];
  document.addEventListener('DOMContentLoaded',function(){
    var b=document.getElementById('themeBtn');
    if(b){
      var sync=function(){var d=r.getAttribute('data-theme')!=='light';b.textContent=d?N[0]:N[1];b.setAttribute('aria-pressed',String(!d));};
      b.addEventListener('click',function(){var n=r.getAttribute('data-theme')==='light'?'dark':'light';r.setAttribute('data-theme',n);try{localStorage.setItem('rc-theme',n);}catch(e){}sync();});
      sync();
    }
    var m=document.getElementById('langMenu');
    if(m){
      document.addEventListener('click',function(e){if(!m.contains(e.target))m.removeAttribute('open');});
      document.addEventListener('keydown',function(e){if(e.key==='Escape')m.removeAttribute('open');});
    }
  });
})();
