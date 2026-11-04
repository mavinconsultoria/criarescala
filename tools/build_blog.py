import re,os,shutil,html,json
SRC='/home/claude/mavinseguros-blog'; OUT='/home/claude/ce/app'; B='https://criarescala.com.br'
slugs=['fim-da-escala-6x1-o-que-muda-para-as-equipes','escala-5x2-4x3-outros-modelos-de-jornada','como-calcular-equipe-ideal-para-escala-sem-furo','erros-comuns-ao-planejar-a-escala-de-equipe','escala-de-revezamento-como-organizar-turnos','troca-de-turno-e-banco-de-horas','pequenos-negocios-e-a-escala-de-7-dias-por-semana']
css=open(SRC+'/assets/style.css',encoding='utf-8').read()
css=css.replace('/* mavin. seguros — blog | design system baseado no brandbook v1.0 */','/* Criar Escala — blog (base do blog Mavin, paleta Criar Escala) */')
css=re.sub(r'--azul:#2E6BE6;','--azul:#5b3df5;',css); css=css.replace('--azul-escuro:#1E4FB8;','--azul-escuro:#4527d6;').replace('--azul-claro:#EAF1FE;','--azul-claro:#efecff;')
css+='\n.wrap.nav{padding:18px 24px}\n.wm .lime{background:#c8f169;color:#0E2233;border-radius:6px;padding:0 .25em;margin-left:.2em}\n'
open(OUT+'/blog/assets/style.css','w',encoding='utf-8').write(css)
shutil.copy(SRC+'/assets/site.js',OUT+'/blog/assets/site.js')
cover=open(SRC+'/assets/covers/gestao-equipes.svg',encoding='utf-8').read().replace('#2E6BE6','#5b3df5')
open(OUT+'/blog/assets/covers/gestao-equipes.svg','w',encoding='utf-8').write(cover)
WM='<a href="/blog/" class="wm">criar<span class="lime">escala</span><span class="seg">blog</span></a>'
HEADER=f'''<header class="site">
  <div class="wrap nav">
    {WM}
    <nav class="nav-links">
      <a href="/blog/" class="navlink">Blog</a>
      <a href="/?utm_source=blog_criarescala&amp;utm_medium=nav" class="btn btn-primary" data-cta="cotacao" data-cta-label="nav">Criar minha escala grátis</a>
    </nav>
  </div>
</header>'''
FOOTER='''<footer class="site">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <div class="wm">criar<span class="lime">escala</span></div>
        <p>Sistema gratuito para montar a escala do mês da sua equipe, já com a nova regra de jornada.</p>
      </div>
      <div class="foot-col">
        <h5>Navegue</h5>
        <a href="/blog/">Blog</a>
        <a href="/">Criar minha escala</a>
        <a href="https://mavinseguros.com.br/privacidade/">Política de privacidade</a>
      </div>
      <div class="foot-col">
        <h5>Quem faz</h5>
        <a href="https://mavinseguros.com.br">Mavin Seguros</a>
        <a href="mailto:contato@mavinseguros.com.br">contato@mavinseguros.com.br</a>
      </div>
    </div>
    <div class="foot-legal">
      <p class="legal-txt">Criar Escala é uma solução da Mavin. MAVIN CONSULTORIA &amp; CORRETAGEM DE SEGUROS LTDA · CNPJ 68.132.516/0001-23 · R. Adelino Leal Nunes, 279, Novo Mundo, Curitiba/PR. Conteúdo informativo, sem validade jurídica: confirme com um advogado trabalhista ou com o departamento pessoal da sua contabilidade.</p>
    </div>
  </div>
</footer>'''
MES={'10':'out','11':'nov'}
posts=[]
for s in slugs:
    t=open(f'{SRC}/drafts/{s}.html',encoding='utf-8').read()
    d=re.search(r'"datePublished": "([0-9-]+)"',t).group(1)
    nd=min(d,'2026-11-03')
    t=t.replace(f'"datePublished": "{d}"',f'"datePublished": "{nd}"').replace(f'"dateModified": "{d}"',f'"dateModified": "{nd}"').replace(f'content="{d}"',f'content="{nd}"')
    y,m,dd=d.split('-'); ny,nm,ndd=nd.split('-')
    t=t.replace(f'· {dd} {MES[m]} {y} ·',f'· {ndd} {MES[nm]} {ny} ·')
    url=f'{B}/blog/{s}.html'
    t=t.replace(f'https://blog.mavinseguros.com.br/drafts/{s}.html',url)
    t=t.replace('https://blog.mavinseguros.com.br/assets/favicon-512.png',B+'/og.png')
    t=t.replace('— mavin. seguros</title>','| Criar Escala</title>').replace('content="mavin. seguros"','content="Criar Escala"')
    t=t.replace('"author": { "@type": "Organization", "name": "Mavin Seguros" }','"author": { "@type": "Organization", "name": "Criar Escala", "url": "https://criarescala.com.br" }')
    t=t.replace('"publisher": { "@type": "Organization", "name": "Mavin Seguros", "logo": {"@type":"ImageObject","url":"'+B+'/og.png"} }','"publisher": { "@type": "Organization", "name": "Criar Escala", "logo": {"@type":"ImageObject","url":"'+B+'/apple-touch-icon.png"} }')
    t=t.replace('<link rel="icon" type="image/png" href="/assets/favicon-32.png">','<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n<link rel="icon" type="image/png" href="/favicon-32.png">')
    t=t.replace('href="/assets/style.css"','href="/blog/assets/style.css"').replace('src="/assets/site.js"','src="/blog/assets/site.js"').replace('src="/assets/covers/','src="/blog/assets/covers/')
    t=re.sub(r'<header class="site">.*?</header>',HEADER,t,count=1,flags=re.S)
    t=re.sub(r'<footer class="site">.*?</footer>',FOOTER,t,count=1,flags=re.S)
    t=t.replace('<div class="byline">Mavin Seguros · corretora de seguros</div>','<div class="byline">Equipe Criar Escala</div>')
    t=t.replace('href="/posts/','href="/blog/')
    t=t.replace('https://criarescala.com.br?utm_source=blog&amp;','/?utm_source=blog_criarescala&amp;').replace('https://criarescala.com.br/?utm_source=blog&amp;','/?utm_source=blog_criarescala&amp;')
    assert 'blog.mavinseguros' not in t, s
    open(f'{OUT}/blog/{s}.html','w',encoding='utf-8').write(t)
    title=html.unescape(re.search(r'<h1>(.*?)</h1>',t,re.S).group(1)); dek=re.search(r'<p class="dek">(.*?)</p>',t,re.S).group(1)
    meta=re.search(r'class="post-meta">Gestão de equipes · ([^<]*)',t).group(1)
    posts.append((nd,s,title,dek,meta))
posts.sort(reverse=True)
rows=''.join(f'''      <a class="row-post" href="/blog/{s}.html">
        <div class="row-img"><img src="/blog/assets/covers/gestao-equipes.svg" alt="" loading="lazy" width="800" height="450"></div>
        <div>
          <span class="row-tag">Gestão de equipes</span>
          <h3>{html.escape(ti)}</h3>
          <p>{dk}</p>
          <span class="meta">{me}</span>
        </div>
        <span class="row-arrow">→</span>
      </a>
''' for nd,s,ti,dk,me in posts)
ld={"@context":"https://schema.org","@type":"Blog","name":"Blog Criar Escala","url":B+"/blog/","publisher":{"@type":"Organization","name":"Criar Escala","url":B+"/"},"blogPost":[{"@type":"BlogPosting","headline":ti,"url":f"{B}/blog/{s}.html","datePublished":nd} for nd,s,ti,dk,me in posts]}
desc='Escala de trabalho, fim da 6x1, jornada de 42h e 40h, revezamento e cobertura de turnos: guias práticos para quem organiza a equipe.'
idx=f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog Criar Escala: escala de trabalho, fim da 6x1 e gestão de turnos</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{B}/blog/">
<meta property="og:type" content="website"><meta property="og:site_name" content="Criar Escala">
<meta property="og:title" content="Blog Criar Escala: escala de trabalho, fim da 6x1 e gestão de turnos">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{B}/blog/"><meta property="og:image" content="{B}/og.png">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="alternate" type="application/rss+xml" title="Blog Criar Escala" href="{B}/blog/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/blog/assets/style.css">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
</head>
<body>
{HEADER}
<section class="section" id="posts">
  <div class="wrap">
    <h1 style="font-size:2rem;letter-spacing:-.03em;margin:8px 0 6px">Escala de trabalho sem furo<span style="color:var(--azul)">.</span></h1>
    <p style="color:var(--cinza);max-width:640px;margin-bottom:28px">{desc}</p>
    <div class="list-posts">
{rows}    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="strip-cta">
      <div><h3>Monte a escala do mês da sua equipe</h3><p>Descubra se a operação vai precisar de mais gente com a nova jornada. Sistema 100% grátis.</p></div>
      <a href="/?utm_source=blog_criarescala&amp;utm_medium=strip&amp;utm_campaign=home-blog" class="btn btn-primary" data-cta="cotacao" data-cta-label="strip-home">Criar minha escala grátis</a>
    </div>
  </div>
</section>
{FOOTER}
<script src="/blog/assets/site.js"></script>
</body>
</html>
'''
open(OUT+'/blog/index.html','w',encoding='utf-8').write(idx)
items=''.join(f'<item><title>{html.escape(ti)}</title><link>{B}/blog/{s}.html</link><guid>{B}/blog/{s}.html</guid><pubDate>{__import__('email.utils').utils.format_datetime(__import__('datetime').datetime.fromisoformat(nd+'T10:00:00-03:00'))}</pubDate><description>{dk}</description></item>' for nd,s,ti,dk,me in posts)
open(OUT+'/blog/feed.xml','w',encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Blog Criar Escala</title><link>{B}/blog/</link><description>{desc}</description>{items}</channel></rss>\n')
urls=[('/','2026-10-21'),('/blog/','2026-11-03')]+[(f'/blog/{s}.html',nd) for nd,s,*_ in posts]
open(OUT+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{B}{u}</loc><lastmod>{d}</lastmod></url>\n' for u,d in urls)+'</urlset>\n')
open(OUT+'/robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {B}/sitemap.xml\n')
print(len(posts),'posts')

# medição (GA4 + Clarity + banner LGPD) em todas as páginas do blog geradas
import glob, subprocess
subprocess.run(['python3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analytics_inject.py'), 'criarescala', *glob.glob(OUT + '/blog/*.html')], check=False)
