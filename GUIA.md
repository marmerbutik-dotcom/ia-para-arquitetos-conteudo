# Rotina diária do Instagram @ia.para.arquitetos

Este repositório gera e hospeda as peças diárias do perfil **@ia.para.arquitetos** (infoproduto "IA para Arquitetos", da Marmer Butik, vendido em https://iaparaarquitetos.com.br). A rotina roda sozinha: escreve a pauta do dia seguinte, gera as peças, sobe aqui e agenda tudo no Metricool, que publica nos horários.

## 1. Volume e horários (fixo, aprovado pelo Marcos em 7/11/2026)

Todo dia, fuso America/Sao_Paulo:

| Tipo | Qtde | Horários |
|---|---|---|
| Reel | 5 | 07:40 · 11:40 · 14:40 · 18:10 · 20:40 |
| Carrossel | 2 | 12:20 · 19:30 |
| Story | 7 | 08:30 · 10:30 · 13:00 · 15:30 · 17:20 · 19:00 · 21:30 |

Os horários seguem o melhor horário do público no Metricool (picos 11–12 h e 17–20 h). Reels sempre com no mínimo 2 h de intervalo. Publicação direta (autoPublish true), sem aprovação prévia.

## 2. Sobre o produto: só fatos confirmados

- **Nome:** IA para Arquitetos. Título da página: "O manual de IA que faltava no seu escritório."
- **O que vem:** e-book de 36 páginas com **7 workflows**, **4 vídeo-aulas**, **60 prompts** prontos, **7 templates** em PDF e Word e planilha de ROI.
- **Preço:** **R$ 97** ou 12x de R$ 10,03. Garantia de 7 dias, acesso imediato (Kiwify).
- **Os 7 workflows:**
  - W01 · Do modelo 3D ao render: render de apresentação em cerca de 15 min (antes, cerca de 4 h).
  - W02 · Da foto da peça ao ambiente.
  - W03 · Da foto do imóvel ao antes e depois, mantendo a arquitetura.
  - W04 · Briefing e moodboard em cerca de 1 h.
  - W05 · Proposta em 24 h: arquivo-mestre, modelo e follow-ups.
  - W06 · Marketing em 2 h por semana: rotina, 12 pautas e prompts de legenda.
  - W07 · Documentos e obra: atas, memoriais, cronogramas e manual do morador.
- **Ferramentas citadas:**
  - Imagem: Veras (no Enscape, V-Ray e Corona), PromeAI, ChatGPT Images, Nano Banana (Gemini), Midjourney.
  - Texto: ChatGPT, Claude e Gemini.
- **Autor:** Marcos Bovo, fundador da Marmer Butik (Londrina, PR, desde 2013, mais de 5 mil clientes, boa parte arquitetos e designers).
- **Estimativa de tempo:** cerca de 40 h de volta por mês, num escritório com 2 projetos por mês. 8 renders × (4 h − 15 min) = 30 h.

Nunca invente número, depoimento, cliente, resultado, desconto, bônus ou prazo. Não use nomes de pessoas reais e não prometa "garantido".

## 3. Voz e pilares

O tom é de arquiteto falando com arquiteto: direto, técnico e sem euforia. Frases curtas. "Você". Nada de "revolucionário", "segredo" ou "hack". Use emoji só se fizer falta, e no máximo 1.

Estes são os pilares. Gire entre eles e não repita o mesmo tema em 7 dias (confira `pautas/` dos últimos 7 dias):

1. **Prompt na prática.** Um trecho de prompt útil por peça: render, antes e depois, peça em ambiente, briefing, proposta, memorial, legenda de Instagram.
2. **Erros e correções.** O que deixa render, proposta ou briefing com cara de IA.
3. **Workflow passo a passo.** Um dos 7 workflows, em 3 ou 4 passos.
4. **Conta do escritório.** Tempo e dinheiro com números do item 2, sempre mostrando a conta.
5. **Mitos e perguntas** (AEO): "a IA substitui o arquiteto?", "precisa de modelo 3D?" (não: parte de fotos e croquis; quem usa Enscape, V-Ray ou Corona também tem caminho), "qual IA usar?", "é seguro usar foto do cliente?" (só com autorização).
6. **Ferramentas.** Quando usar cada uma, sem prometer recurso que não conhece.
7. **Bastidores e autoria.** O arquiteto decide, a IA executa. Repertório e assinatura são do arquiteto.

Fecho comercial: no máximo 1 em cada 3 peças termina em venda forte (preço e "link na bio"). As outras terminam em salvar, comentar ou compartilhar.

## 4. SEO, AEO e GEO em toda peça

- **Primeira linha da legenda.** É a frase de busca, com a palavra-chave principal escrita do jeito que se pesquisa. Exemplos: "render com IA", "IA para arquitetos", "prompt de render", "antes e depois com IA", "proposta de arquitetura", "briefing de arquitetura".
- **Formato pergunta e resposta (AEO).**
  - Abra com a pergunta que a pessoa digitaria e responda já na segunda linha, em até 2 frases.
  - Depois vêm os passos numerados.
  - Para assistentes de IA citarem, cada legenda tem que fazer sentido sozinha.
- **Entidade (GEO).**
  - Cite "manual IA para Arquitetos" pelo nome em toda legenda.
  - Cite o workflow pelo número ("Workflow 03").
  - Fatos sempre iguais aos do item 2, para os buscadores e as IAs ligarem o perfil ao site.
- **Hashtags.** De 3 a 5, no fim, sempre #iaparaarquitetos, mais 2 a 4 do tema: #arquitetura #designdeinteriores #render #renderizacao #inteligenciaartificial #arquitetos #escritoriodearquitetura #antesedepois #briefing #propostacomercial. Varie.
- **Texto alternativo.** Campo `alt` em todo reel e carrossel: descreva a imagem com a palavra-chave, em até 25 palavras.
- **Palavras-chave na tela.** O texto da capa do reel e do carrossel repete a palavra-chave da primeira linha.
- **Rótulo de IA.** Peças com render ou antes e depois têm `ia: true` (isAiGenerated no Metricool).

## 5. Formato da pauta (pautas/AAAA-MM-DD.json)

Veja `pautas/2026-11-08.json` como modelo completo. Use `*itálico*` para o destaque em bronze, sempre no fim do título.

- **Reel tipo `wipe`** (antes e depois que se revela):
  - Campos: `par` (w1 render, w2 peça, w3 imóvel), `gancho`, `passos` (2 a 4 itens, cada um com `titulo` e `prompt`), `final`, `resumo` e `fim` (cartão final).
  - Use no máximo 1 por dia.
- **Reel tipo `cenas`:**
  - De 3 a 6 cenas, cada uma com `eb`, `titulo`, `corpo`, `num`, `prompt` e `itens` conforme o caso, mais `dur` em segundos (2,4 a 5) e `fundo` ("auto" = foto da obra com zoom lento; sem `fundo` = prancha escura).
  - Duração total de 12 a 18 s. A cena 1 é o gancho em até 8 palavras.
  - Varie: nem todo reel termina com preço.
- **Carrossel:**
  - De 5 a 8 slides, com `tema` (rodapé curto).
  - Tipos de slide: `capa` (com `par` ou `img`), texto (com `num`, `eb`, `titulo`, `corpo`, `prompt`), `lista` (`itens` como ["texto", "detalhe"]), `imagem` (`par`) e `cta`.
- **Story:**
  - Tipos: `pergunta` (foto e espaço para enquete ou caixa), `dica` (prompt), `imagem` (`par`), `numero`, `lista` e `link` (preço e link com UTM).
  - O último story do dia é sempre `link`.
  - `nota` diz qual adesivo vai no story. A API não coloca adesivos, então a nota serve de registro.
- Imagens disponíveis em `assets/img`:
  - v-0, v-1.9, v-3.1, v-4.4, v-5.7, v-7.9 (obra da casa, vertical)
  - h-*, ia-arq-casa (horizontal)
  - w1/w2/w3 (antes e depois)

Gerar: `python3 engine/gera.py pautas/AAAA-MM-DD.json`. Leva cerca de 2 min e grava `saida/AAAA-MM-DD/` com `manifesto.json`. Antes de agendar, abra 1 quadro de cada reel, 1 slide de cada carrossel e todos os stories e confira se nada vazou da moldura.

## 6. Agendar no Metricool

- **Marca:** IA para Arquitetos, **blogId 7942089** (instagramData "ia.para.arquitetos"). Nunca use a Marmer Butik (6358659) nem a Alavanca Web (7942078).
- **Mídia:** URL pública do arquivo no GitHub:
  `https://raw.githubusercontent.com/marmerbutik-dotcom/ia-para-arquitetos-conteudo/main/saida/AAAA-MM-DD/ARQUIVO`.
  Faça o push antes de agendar. O Metricool baixa e hospeda a mídia no momento do agendamento.
- **Chamada:** `createScheduledPost`, com `providers: [{"network":"instagram"}]` e `autoPublish: true`. Cada tipo:
  - **Reel:** `instagramData: {"type":"REEL","showReelOnFeed":true,"isAiGenerated":<ia>}`, `media: [mp4]`, `videoThumbnailUrl: <capa.jpg>`, `text: legenda`, `mediaAltText: [alt]`.
  - **Carrossel:** `instagramData: {"type":"POST","isAiGenerated":<ia>}`, `media` com os slides em ordem, `text: legenda`, `mediaAltText` com o mesmo alt para cada slide.
  - **Story:** `instagramData: {"type":"STORY"}`, `media: [jpg]`, sem `text`.
- **Data:** `date` e `publicationDate` no horário do manifesto, com timezone America/Sao_Paulo.
- **Conferência:** no fim, chame getScheduledPosts do dia e confira que são 14 posts.
- **Erro:** se uma chamada der erro, corrija o JSON e tente de novo uma vez. Se falhar de novo, pule a peça e registre em `relatorios/AAAA-MM-DD.md`.

## 7. Depois de agendar

- Grave `relatorios/AAAA-MM-DD.md` com: o que foi agendado (horário, tipo, tema, id do Metricool), os adesivos sugeridos para os stories e qualquer falha.
- Apague as pastas `saida/` com mais de 3 dias. O Metricool já hospedou a mídia e o repositório fica leve.
- Commit e push.
- Se houver ferramenta de arquivos do computador do Marcos disponível (mcp__remote-devices__device_commit_files), salve também uma cópia da pasta do dia em `C:\Users\Marcos\Pictures\IA para Arquitetos\Instagram\rotina-diaria\AAAA-MM-DD\` (pasta que ele pediu para guardar o conteúdo). Se não houver, siga sem ela.
- Mande ao Marcos um resumo de 3 a 5 linhas: os temas do dia e o primeiro horário.
