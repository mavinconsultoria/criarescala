# criarescala.com.br

Site publicado do Criar Escala: o sistema (`index.html`, arquivo único) e o blog em `/blog/`.

**Este repositório é a única fonte do Criar Escala.** Edite o `index.html` aqui. A pasta iCloud `Mavin/Criar Escala` (`app.src.html`, `build.py`, `deploy/`) está desatualizada e não deve ser usada para gerar nem publicar o site.

## Blog
- Posts em `blog/<slug>.html`, mas a URL pública é **sem `.html`** (`https://criarescala.com.br/blog/<slug>`): o Cloudflare Pages redireciona `.html` para a versão sem extensão. Canonical, og:url, JSON-LD, links internos, feed e sitemap usam sempre a URL sem `.html`. Lista em `blog/index.html`, feed em `blog/feed.xml`, URLs no `sitemap.xml` da raiz.
- Título (`<title>`) com no máximo 65 caracteres, para não ser cortado no Google.
- Ritmo: 2 a 3 posts por semana, só sobre escala de trabalho, jornada (EC 141/2026) e gestão de turnos.
- Rascunhos ficam em `drafts/`. A pasta é publicada, mas com cabeçalho `noindex` (ver `_headers`), e só entra no blog quando o arquivo é movido para `blog/`.

## Publicação
Cloudflare Pages, projeto `criarescala`, por upload direto (`wrangler pages deploy`). O push no GitHub **não** publica.
