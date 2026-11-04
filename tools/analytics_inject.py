#!/usr/bin/env python3
"""Insert analytics (consent mode + delayed loader + LGPD banner) into HTML files.
usage: inject.py <brand> <file>...   brand: mavin | criarescala | savant"""
import sys, re

T = '/home/claude/tpl/'
MARK = 'data-analytics="mavin-v1"'

def generic(ga, clarity, key, bg, fg, accent, privacy, font):
    head = f"""<!-- Medição (GA4 + Clarity) com Consent Mode v2 {MARK} -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{'ad_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','analytics_storage':'denied','wait_for_update':500}});
  (function(){{ try {{ if (localStorage.getItem('{key}') === 'accepted') gtag('consent','update',{{'ad_storage':'granted','ad_user_data':'granted','ad_personalization':'granted','analytics_storage':'granted'}}); }} catch(e){{}} }})();
</script>
<script>
/* GA4 e Clarity carregados na primeira interação ou 5 s após o carregamento, para não atrasar a página. */
(function(w,d){{
  var done=false;
  function load(){{
    if(done) return; done=true;
    var g=d.createElement('script'); g.async=true; g.src='https://www.googletagmanager.com/gtag/js?id={ga}'; d.head.appendChild(g);
    gtag('js', new Date()); gtag('config', '{ga}');
    (function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(w,d,"clarity","script","{clarity}");
    var ok=false; try{{ ok = localStorage.getItem('{key}')==='accepted'; }}catch(e){{}}
    w.clarity('consentv2',{{ad_Storage: ok?'granted':'denied', analytics_Storage: ok?'granted':'denied'}});
    ['pointerdown','keydown','scroll','touchstart'].forEach(function(e){{ w.removeEventListener(e,load,{{passive:true}}); }});
  }}
  ['pointerdown','keydown','scroll','touchstart'].forEach(function(e){{ w.addEventListener(e,load,{{passive:true,once:true}}); }});
  w.addEventListener('load',function(){{ setTimeout(load,5000); }});
  /* cliques em WhatsApp, telefone e e-mail viram eventos de conversão */
  d.addEventListener('click',function(ev){{
    var a=ev.target.closest && ev.target.closest('a[href]'); if(!a) return;
    var h=a.getAttribute('href')||'', n=null;
    if(/wa\\.me|whatsapp/i.test(h)) n='click_whatsapp'; else if(/^tel:/i.test(h)) n='click_telefone'; else if(/^mailto:/i.test(h)) n='click_email';
    if(n) gtag('event', n, {{link_url:h, page_path:location.pathname}});
  }}, true);
}})(window,document);
</script>
<!-- Fim da medição -->"""
    banner = f"""<!-- Banner de consentimento de cookies (LGPD) -->
<style>
  #an-cookie-bar{{position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;max-width:640px;margin:0 auto;background:{bg};color:{fg};border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.25);padding:10px 12px 10px 16px;display:flex;align-items:center;gap:12px;font-family:{font};font-size:12px;line-height:1.4;transition:transform .3s ease,opacity .3s ease}}
  #an-cookie-bar.an-hidden{{transform:translateY(20px);opacity:0;pointer-events:none}}
  #an-cookie-bar a{{color:inherit;text-decoration:underline;opacity:.9}}
  #an-cookie-bar .an-t{{flex:1;opacity:.88}}
  #an-cookie-bar .an-a{{display:flex;gap:6px;flex-shrink:0}}
  #an-cookie-bar button{{font-family:inherit;font-weight:700;font-size:12px;padding:7px 12px;border-radius:8px;border:none;cursor:pointer;white-space:nowrap}}
  #an-cookie-no{{background:rgba(127,127,127,.18);color:inherit;font-weight:600}}
  #an-cookie-ok{{background:{accent};color:#fff}}
  @media(max-width:480px){{#an-cookie-bar{{flex-direction:column;align-items:stretch;text-align:left}}#an-cookie-bar .an-a{{justify-content:flex-end}}}}
</style>
<div id="an-cookie-bar" class="an-hidden" role="dialog" aria-label="Consentimento de cookies">
  <div class="an-t">Usamos cookies para medir e melhorar o uso do site.{(' <a href="'+privacy+'">Política de privacidade</a>') if privacy else ''}</div>
  <div class="an-a"><button id="an-cookie-no" type="button">Recusar</button><button id="an-cookie-ok" type="button">Aceitar</button></div>
</div>
<script>
(function(){{
  var bar=document.getElementById('an-cookie-bar'), k='{key}', s=null;
  try{{ s=localStorage.getItem(k); }}catch(e){{}}
  if(!s) bar.classList.remove('an-hidden');
  function done(v){{ try{{ localStorage.setItem(k,v); }}catch(e){{}} bar.classList.add('an-hidden'); }}
  document.getElementById('an-cookie-ok').addEventListener('click',function(){{
    gtag('consent','update',{{'ad_storage':'granted','ad_user_data':'granted','ad_personalization':'granted','analytics_storage':'granted'}});
    if(window.clarity) clarity('consentv2',{{ad_Storage:'granted',analytics_Storage:'granted'}});
    done('accepted');
  }});
  document.getElementById('an-cookie-no').addEventListener('click',function(){{ done('rejected'); }});
}})();
</script>"""
    return head, '', banner

BRANDS = {
    'criarescala': lambda: generic('G-2L3P5YF5HM', 'z8ddnrsilw', 'criarescala_cookie_consent', '#111827', '#F9FAFB', '#5B3DF5', None, 'inherit'),
    'mavinconsultoria': lambda: generic('G-82E012LG8D', 'z8ddvo13wc', 'mavinconsultoria_cookie_consent', '#0E2233', '#FAF9F6', '#2E6BE6', 'https://mavinseguros.com.br/privacidade/', 'inherit'),
    'savant': lambda: generic('G-82E012LG8D', 'z8ddvo13wc', 'savant_cookie_consent', '#0E2233', '#FAF9F6', '#2E6BE6', '/privacidade', 'inherit'),
}

def mavin():
    head = open(T + 'mavin_head.html').read().replace('<!-- Google Consent Mode v2', f'<!-- {MARK} --><!-- Google Consent Mode v2', 1)
    return head, open(T + 'mavin_noscript.html').read(), open(T + 'mavin_banner.html').read()

brand = sys.argv[1]
head, noscript, banner = mavin() if brand == 'mavin' else BRANDS[brand]()
for path in sys.argv[2:]:
    s = open(path, encoding='utf-8').read()
    if MARK in s or 'GTM-PCPXGX2B' in s or 'G-2L3P5YF5HM' in s or 'G-82E012LG8D' in s:
        print('skip (already)', path); continue
    if brand == 'mavin':
        # remove direct GA4 gtag snippet and HubSpot loader (both come from the GTM block)
        s = re.sub(r'<!-- Google tag \(gtag\.js\) -->\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-QKM151SNGV"></script>\s*<script>.*?</script>', '', s, flags=re.S)
        s = re.sub(r'<script[^>]*id="hs-script-loader"[^>]*></script>', '', s)
    m = re.search(r'<head[^>]*>', s, re.I)
    if not m:
        print('NO HEAD', path); continue
    s = s[:m.end()] + '\n' + head + '\n' + s[m.end():]
    if noscript:
        mb = re.search(r'<body[^>]*>', s, re.I)
        if mb: s = s[:mb.end()] + '\n' + noscript + '\n' + s[mb.end():]
    i = s.lower().rfind('</body>')
    s = (s[:i] + banner + '\n' + s[i:]) if i >= 0 else s + banner
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', path)
