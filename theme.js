(function(){
  var r=document.documentElement,t='dark';
  try{var v=localStorage.getItem('rc-theme');if(v==='light'||v==='dark')t=v;}catch(e){}
  r.setAttribute('data-theme',t);
  document.addEventListener('DOMContentLoaded',function(){
    var b=document.getElementById('themeBtn');if(!b)return;
    function sync(){var d=r.getAttribute('data-theme')!=='light';b.textContent=d?'☾ escuro':'☀ claro';b.setAttribute('aria-pressed',String(!d));}
    b.addEventListener('click',function(){var n=r.getAttribute('data-theme')==='light'?'dark':'light';r.setAttribute('data-theme',n);try{localStorage.setItem('rc-theme',n);}catch(e){}sync();});
    sync();
  });
})();
