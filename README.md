# criarescala.com.br

Site publicado do Criar Escala: o sistema (`index.html`, arquivo único gerado por `build.py` a partir de `app.src.html` + `engine.js`, que ficam na pasta iCloud `Mavin/Criar Escala`) e o blog em `/blog/`.

## Blog
- Posts em `blog/<slug>.html`, lista em `blog/index.html`, feed em `blog/feed.xml`, URLs no `sitemap.xml` da raiz.
- Ritmo: 2 a 3 posts por semana, só sobre escala de trabalho, jornada (EC 141/2026) e gestão de turnos.
- Rascunhos ficam em `drafts/`. A pasta é publicada, mas com cabeçalho `noindex` (ver `_headers`), e só entra no blog quando o arquivo é movido para `blog/`.

## Publicação
Cada push na branch `main` publica no Netlify (projeto `criarescala-app`).
