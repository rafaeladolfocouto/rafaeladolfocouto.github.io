# Portfólio de produtos

Site estático multipágina (HTML, `style.css` e `theme.js`, sem build) para publicar no GitHub Pages.

## Publicar em rafaeladolfocouto.github.io

1. Crie um repositório público chamado `rafaeladolfocouto.github.io`.
2. Envie todos os arquivos e `.nojekyll` para a branch `main`.
3. Em Settings > Pages, escolha "Deploy from a branch", branch `main`, pasta `/ (root)`.
4. Em um ou dois minutos o site fica em https://rafaeladolfocouto.github.io

Para usar um repositório com outro nome (por exemplo `portfolio`), o endereço vira https://rafaeladolfocouto.github.io/portfolio

## Estrutura

- `index.html`: home com os caminhos de leitura
- `quem-sou.html`, `ia-gestao.html`, `monetizacao.html`: conteúdo profissional
- `produtos.html` e uma página por produto (`blink.html`, `shhhift.html`, `vilalume.html`, `precofeito.html`)
- `style.css`: identidade Teorema Âmbar, com modo escuro e claro (variáveis em `:root`)
- `theme.js`: botão de tema, que lembra a escolha do visitante

Cada produto tem suas cores no bloco "temas por produto" do CSS. Os logos e as telas são carregados direto dos sites de cada produto.
