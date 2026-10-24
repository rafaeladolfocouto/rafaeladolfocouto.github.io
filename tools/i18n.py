#!/usr/bin/env python3
"""Gera as versões em inglês (en/) e espanhol (es/) a partir das páginas em português (raiz).
Uso:  python3 tools/i18n.py extract   -> escreve tools/i18n/units.json
      python3 tools/i18n.py build     -> escreve en/*.html e es/*.html
"""
import re,sys,json,os,glob
from bs4 import BeautifulSoup, NavigableString, Tag
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES=['index','quem-sou','ia-gestao','monetizacao','produtos','blink','shhhift','vilalume','precofeito']
INLINE={'a','b','i','em','strong','sub','sup','span','br','small','code','mark'}
SKIP={'script','style','svg','header','footer'}
ATTRS=['alt','aria-label','title']
def norm(s): return re.sub(r'\s+',' ',s).strip()

def has_text(el): return bool(norm(el.get_text()))
def only_inline(el):
    return all((d.name in INLINE) for d in el.find_all(True))

def units(main):
    out=[]
    def walk(el):
        for ch in list(el.children):
            if not isinstance(ch,Tag) or ch.name in SKIP: continue
            if ch.name=='img' or ch.name=='br': continue
            if has_text(ch) and only_inline(ch) and not ch.find('svg'):
                out.append(ch)
            else:
                walk(ch)
    walk(main)
    return out
def key(el): return norm(el.decode_contents())

def load(p):
    return BeautifulSoup(open(os.path.join(ROOT,p+'.html'),encoding='utf-8').read(),'html.parser')

def attr_targets(soup):
    res=[]
    main=soup.find('main')
    for el in main.find_all(True):
        if el.find_parent('svg') or el.name=='svg':
            pass
        for a in ATTRS:
            if el.has_attr(a) and norm(el[a]): res.append((el,a))
    return res

def extract():
    seen={};order=[]
    def add(k):
        if k not in seen: seen[k]='u%04d'%(len(seen)+1); order.append(k)
    per={}
    for p in PAGES:
        soup=load(p); main=soup.find('main'); keys=[]
        t=soup.title.string; add(norm(t)); keys.append(norm(t))
        for m in soup.find_all('meta'):
            if m.get('name')=='description' or m.get('property') in('og:title','og:description'):
                add(norm(m['content']))
        for el in units(main):
            add(key(el))
        for el,a in attr_targets(soup): add(norm(el[a]))
    json.dump({seen[k]:k for k in order},open(os.path.join(ROOT,'tools/i18n/units.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
    print(len(order),'unidades')

LANG={'en':{'html':'en','theme':('☾ dark','☀ light'),'lang':'English','nav':['Home','About me','AI/ML & management','Data monetization','Products'],'aria_nav':'Main','aria_theme':'Switch between dark and light mode','aria_lang':'Language',
  'foot':'© 2026 Rafael Couto. Blink, shhhift, Vilalume and Preço Feito are independent projects. shhhift is not affiliated with Spotify, Google, YouTube or Apple.','linkedin':'LinkedIn','skip':'Skip to content'},
 'es':{'html':'es','theme':('☾ oscuro','☀ claro'),'lang':'Español','nav':['Inicio','Quién soy','IA/ML y gestión','Monetización de datos','Productos'],'aria_nav':'Principal','aria_theme':'Alternar entre modo oscuro y claro','aria_lang':'Idioma',
  'foot':'© 2026 Rafael Couto. Blink, shhhift, Vilalume y Preço Feito son proyectos independientes. shhhift no está afiliado a Spotify, Google, YouTube ni Apple.','linkedin':'LinkedIn','skip':'Ir al contenido'}}
PT={'html':'pt-BR','lang':'Português'}
NAVHREF=['index.html','quem-sou.html','ia-gestao.html','monetizacao.html','produtos.html']
NAVKEY={'index':0,'quem-sou':1,'ia-gestao':2,'monetizacao':3,'produtos':4,'blink':4,'shhhift':4,'vilalume':4,'precofeito':4}
LOGO=re.search(r'<a class="brand"[^>]*>(<svg.*?</svg>)',open(os.path.join(ROOT,'index.html'),encoding='utf-8').read(),re.S).group(1)

def header(lang,page):
    L=LANG[lang]
    nav=''.join('<a href="%s"%s>%s</a>'%(h,' aria-current="page"' if i==NAVKEY[page] else '',t) for i,(h,t) in enumerate(zip(NAVHREF,L['nav'])))
    langs=''.join('<a href="%s" lang="%s"%s>%s</a>'%(('../' if l!='pt' else '')+((l+'/') if l not in('pt',) else '')+page+'.html' if False else relpath(lang,l,page),l if l!='pt' else 'pt',' aria-current="true"' if l==lang else '',{'pt':'Português','en':'English','es':'Español'}[l]) for l in ('pt','en','es'))
    cur=lang.upper()
    return f'''<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html">{LOGO}rafael couto</a>
    <nav aria-label="{L['aria_nav']}">{nav}</nav>
    <div class="ctl">
      <button class="theme" id="themeBtn" type="button" aria-label="{L['aria_theme']}">{L['theme'][0]}</button>
      <details class="lang" id="langMenu"><summary aria-label="{L['aria_lang']}">🌐 {cur}</summary><div class="langlist">{langs}</div></details>
    </div>
  </div>
</header>'''
def relpath(cur,target,page):
    # caminho de uma página em `cur` para a mesma página em `target`
    base='' if cur=='pt' else '../'
    return base+('' if target=='pt' else target+'/')+page+'.html'
def footer(lang):
    L=LANG[lang]
    return f'''<footer>
  <div class="wrap">
    <a href="https://www.linkedin.com/in/rafaeladolfocouto" target="_blank" rel="noopener">LinkedIn</a>
    <a href="mailto:rafaeladolfocouto@gmail.com">rafaeladolfocouto@gmail.com</a>
    <p style="margin-top:16px">{L['foot']}</p>
  </div>
</footer>'''

def build():
    tr={l:json.load(open(os.path.join(ROOT,'tools/i18n/%s.json'%l),encoding='utf-8')) for l in ('en','es')}
    units_=json.load(open(os.path.join(ROOT,'tools/i18n/units.json'),encoding='utf-8'))
    inv={v:k for k,v in units_.items()}
    miss=set()
    for lang in ('en','es'):
        d=tr[lang]; os.makedirs(os.path.join(ROOT,lang),exist_ok=True)
        def T(k):
            uid=inv.get(k)
            if uid is None or uid not in d: miss.add((lang,k[:70])); return None
            return d[uid]
        for p in PAGES:
            soup=load(p); main=soup.find('main')
            for el in units(main):
                t=T(key(el))
                if t is None: continue
                el.clear(); frag=BeautifulSoup(t,'html.parser')
                for c in list(frag.contents): el.append(c)
            for el,a in attr_targets(soup):
                t=T(norm(el[a]))
                if t is not None: el[a]=t
            t=T(norm(soup.title.string))
            if t: soup.title.string=t
            for m in soup.find_all('meta'):
                if m.get('name')=='description' or m.get('property') in('og:title','og:description'):
                    t=T(norm(m['content']))
                    if t: m['content']=t
            html=str(soup)
            html=re.sub(r'<header class="top">.*?</header>',lambda m:header(lang,p),html,flags=re.S)
            html=re.sub(r'<footer>.*?</footer>',lambda m:footer(lang),html,flags=re.S)
            html=re.sub(r'(<html[^>]*?)lang="pt-BR"',lambda m:m.group(1)+'lang="%s"'%LANG[lang]['html'],html,count=1)
            html=html.replace('href="style.css','href="../style.css').replace('src="theme.js','src="../theme.js').replace('src="img/','src="../img/')
            alts=''.join('<link rel="alternate" hreflang="%s" href="https://rafaeladolfocouto.github.io/%s%s.html">'%(l,'' if l=='pt' else l+'/',p) for l in('pt','en','es'))
            html=html.replace('</head>',alts+'\n</head>',1)
            open(os.path.join(ROOT,lang,p+'.html'),'w',encoding='utf-8').write(html)
    # páginas em português: troca header/footer pelos com seletor de idioma
    for p in PAGES:
        f=os.path.join(ROOT,p+'.html'); s=open(f,encoding='utf-8').read()
        s=re.sub(r'<header class="top">.*?</header>',lambda m:header('pt',p),s,flags=re.S)
        if 'hreflang' not in s:
            alts=''.join('<link rel="alternate" hreflang="%s" href="https://rafaeladolfocouto.github.io/%s%s.html">'%(l,'' if l=='pt' else l+'/',p) for l in('pt','en','es'))
            s=s.replace('</head>',alts+'\n</head>',1)
        open(f,'w',encoding='utf-8').write(s)
    if miss:
        print('SEM TRADUÇÃO:',len(miss))
        for m in sorted(miss)[:20]: print(m)
    else: print('ok, tudo traduzido')

# header PT usa LANG['pt'] nav
LANG['pt']={'html':'pt-BR','theme':('☾ escuro','☀ claro'),'nav':['Início','Quem sou','IA/ML e gestão','Monetização','Produtos'],'aria_nav':'Principal','aria_theme':'Alternar entre modo escuro e claro','aria_lang':'Idioma'}
if __name__=='__main__':
    {'extract':extract,'build':build}[sys.argv[1]]()
