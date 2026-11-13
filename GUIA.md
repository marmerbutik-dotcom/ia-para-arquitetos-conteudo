# Rotina diária do Instagram @ia.para.arquitetos

Este repositório gera e hospeda as peças diárias do perfil **@ia.para.arquitetos** (infoproduto "IA para Arquitetos", da Marmer Butik, vendido em https://iaparaarquitetos.com.br). A rotina roda sozinha: escreve a pauta do dia seguinte, gera as peças, sobe aqui e agenda tudo no Metricool, que publica nos horários.

## 1. Volume e horários (reduzido pelo Marcos em 13/11/2026: "diminua a frequência, 1 carrossel por dia, 3 reels, 4 stories")

Todo dia, fuso America/Sao_Paulo, a partir de 14/11/2026 (8 peças por dia):

| Tipo | Qtde | Horários |
|---|---|---|
| Reel | 3 | 11:40 · 14:40 · 20:40 |
| Carrossel | 1 | 19:30 |
| Story | 4 | 08:30 · 13:00 · 17:20 · 21:30 |

Os horários seguem os reels que mais alcançaram na 1ª semana (14:40 e 20:40) e o pico do público no Metricool (11–12 h e 17–20 h). Reels sempre com no mínimo 2 h de intervalo. (Até 13/11 eram 5 reels, 2 carrosséis e 7 stories.) Publicação direta (autoPublish true), sem aprovação prévia.

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

Fecho comercial: no máximo 2 das 8 peças do dia terminam em venda forte (preço e "link na bio"), contando o story `link`. As outras terminam em salvar, comentar ou compartilhar.

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

## 4b. SEO, AEO e GEO dos modelos de referência (pedido do Marcos em 13/11/2026)

Vale para todo modelo da biblioteca (5e) e para os reels "da planta à obra final". Complementa o item 4; não muda os fatos do item 2.

**Por que importa:** desde 2025 o Google indexa posts públicos de contas profissionais do Instagram, e a busca do próprio Instagram lê a legenda, o texto na tela, o alt e a fala. Assistentes de IA (ChatGPT, Gemini, Perplexity) citam trechos que respondem uma pergunta sozinhos e que repetem a mesma entidade com os mesmos fatos.

**1. Mapa de palavras-chave por modelo** (uma principal na 1ª linha, uma secundária no corpo; sem Semrush, use estas):

| Modelo | Principal (1ª linha e capa) | Secundárias (corpo, alt, hashtag) |
|---|---|---|
| Da planta à obra final / evolução | "do projeto à obra com IA", "planta humanizada", "render com IA" | apresentar projeto ao cliente, maquete eletrônica, render de fachada, render de interiores |
| Antes e depois | "antes e depois com IA" | reforma, simulação de reforma, foto do imóvel |
| Prompt na prática | "prompt de render" | prompt para arquitetura, ChatGPT para arquitetos |
| Pergunta-mito / lista | "IA para arquitetos" | inteligência artificial na arquitetura, escritório de arquitetura |
| Ferramentas | "qual IA usar para render" | Veras, PromeAI, Midjourney, ChatGPT Images |

**2. Legenda (molde AEO, até 2.200 caracteres):**
1 · 1ª linha (até 125 caracteres): palavra-chave principal + o que o vídeo mostra.
2 · Pergunta que a pessoa digitaria ("Como apresentar a casa ao cliente antes da obra?").
3 · Resposta direta em até 2 frases, que faça sentido sozinha (é o trecho que a IA cita).
4 · Passos numerados ("1 ·") iguais às etapas do vídeo, com o nome de cada etapa.
5 · Linha de entidade (GEO): "manual IA para Arquitetos", o Workflow pelo número e um fato do item 2.
6 · Um CTA (salvar, comentar, compartilhar ou link na bio).
7 · 3 a 5 hashtags (item 4), sempre #iaparaarquitetos.

**3. Banco de perguntas e respostas (AEO/GEO)** — respostas prontas, só com fatos do item 2; use uma por peça e não repita a mesma em 7 dias:
- Dá para apresentar a casa ao cliente antes da obra? Dá: gere a casa pronta a partir do seu projeto e tire dela a estrutura com a mesma câmera. É a lógica do Workflow 01.
- Quanto tempo leva um render de apresentação com IA? Cerca de 15 min por imagem, contra cerca de 4 h antes (Workflow 01).
- A IA substitui o arquiteto? Não. Ela gera imagem; projeto, responsabilidade técnica e assinatura continuam com o arquiteto.
- Preciso de modelo 3D para usar IA? Não: dá para partir de foto ou croqui. Quem usa Enscape, V-Ray ou Corona pode usar o Veras dentro do programa.
- Qual IA usar para render? Veras, PromeAI, ChatGPT Images, Nano Banana (Gemini) e Midjourney para imagem; ChatGPT, Claude e Gemini para texto.
- Planta humanizada com IA é projeto? Não: é imagem de apresentação feita sobre a sua planta técnica, que continua sendo a referência das medidas.
- Posso usar a foto do cliente na IA? Só com autorização dele.
- Quanto tempo a IA devolve por mês? Cerca de 40 h num escritório com 2 projetos por mês; só no render, 8 × (4 h − 15 min) = 30 h.
- O que vem no manual IA para Arquitetos? 7 workflows, 4 vídeo-aulas, 60 prompts, 7 templates em PDF e Word e planilha de ROI, por R$ 97 ou 12x de R$ 10,03, com 7 dias de garantia.

**4. Texto na tela (SEO do vídeo):**
- Capa e 1º quadro com a palavra-chave principal escrita por extenso (ex.: "Do projeto à obra com IA").
- Nome de cada etapa na tela igual ao da legenda (Planta técnica, Planta humanizada, Estrutura, Obra crua, Render final, Casa pronta).
- Quando o modelo tiver fala ou narração, a fala repete a pergunta e a resposta do item 3 (o Instagram transcreve).

**5. Alt e arquivos:**
- `alt` de até 25 palavras: palavra-chave + cenário + etapas ("Do projeto à obra com IA: planta, estrutura de concreto e casa no lago pronta, mesma câmera").
- Nome dos arquivos de imagem com a palavra-chave e o cenário (ex.: `planta-humanizada-home-office-01.jpg`), sem acento.

**6. Entidade e consistência (GEO):**
- Sempre "manual IA para Arquitetos" (com "manual" e com essa grafia), "Marcos Bovo" só quando citar o autor e "iaparaarquitetos.com.br" sem variação.
- Números exatamente como no item 2 (7 workflows, 60 prompts, R$ 97, cerca de 15 min, 24 h). Nada de arredondar ou inventar.
- Pelo menos 1 vez por semana, um carrossel ou reel de pergunta e resposta pura (formato FAQ), que é o que as IAs mais citam.

**7. Checagem final:** antes de agendar, confira na revisão 5c se a palavra-chave aparece na 1ª linha, na capa, no alt e em uma hashtag, e se a resposta da pergunta cabe em 2 frases.

## 5. Formato da pauta (pautas/AAAA-MM-DD.json)

Veja `pautas/2026-11-08.json` como modelo completo. Use `*itálico*` para o destaque em bronze, sempre no fim do título.

- **Reel tipo `evolucao`** (o estilo principal desde 8/11, ver 5d): a mesma cena passando por etapas, com linha de luz, wireframe e prompt sendo digitado.
  - Campos: `gancho` (2 linhas; a 2ª sai em itálico bronze), `rotulo` (canto superior direito, curto, em maiúsculas), `etapas` (3 ou 4, cada uma com `img`, `nome`, `trans`, `prompt` opcional e `foco` no `mergulho`), `frase` (2 linhas sobre a última etapa), `legenda`, `alt`, `horario`. O cartão final com logo e site entra sozinho.
  - Use 2 por dia (um de interior e um de casa/fachada). Duração sai entre 14 e 18 s. O Marcos gostou do formato (8/11) e pediu mais.
- **Reel tipo `wipe`** (antes e depois que se revela):
  - Campos: `par` (w1 render, w2 peça, w3 imóvel), `gancho`, `passos` (2 a 4 itens, cada um com `titulo` e `prompt`), `final`, `resumo` e `fim` (cartão final).
  - Use no máximo 1 por dia.
- **Reel tipo `cenas`:**
  - De 3 a 6 cenas, cada uma com `eb`, `titulo`, `corpo`, `num`, `prompt` e `itens` conforme o caso, mais `dur` em segundos (2,4 a 5) e `fundo` ("auto" = foto da obra com zoom lento; sem `fundo` = prancha escura).
  - Duração total de 12 a 18 s. A cena 1 é o gancho em até 8 palavras.
  - Varie: nem todo reel termina com preço.
- **Carrossel:**
  - De 5 a 8 slides, com `tema` (rodapé curto).
  - Tipos de slide: `capa` (com `par` ou `img`), texto (com `num`, `eb`, `titulo`, `corpo`, `prompt`), `lista` (`itens` como ["texto", "detalhe"]), `imagem` (`par`), `etapa` e `cta`.
  - `etapa` (ver 5d): foto cheia de uma etapa da sequência com selo numerado. Campos: `img`, `nome`, `n` (opcional, ex.: "02"), `titulo` (opcional, curto) e `prompt` (opcional). O carrossel do dia alterna: dia ímpar é "etapas" (capa com a última imagem, 1 slide `etapa` por etapa, com o prompt de cada uma, 1 slide de texto com o cuidado principal e `cta`); dia par é um carrossel normal (lista, erros, prompts, conta do escritório).
- **Story (tudo automático, sem adesivos — pedido do Marcos em 7/11):** o story precisa funcionar sozinho, sem enquete, caixa de perguntas, emoji deslizante nem adesivo de link. NUNCA escreva no story algo que peça voto, resposta na caixa ou toque em adesivo ("vote", "responda aqui", "toque no link"). Use perguntas só como gancho retórico, já respondidas no próprio story.
  - Tipos: `foto` (imagem de fundo + título + corpo curto), `dica` (prompt), `imagem` (`par`), `numero`, `lista`, `link` e `evolucao`.
  - `evolucao`: story em vídeo (10 a 14 s), com os mesmos campos do reel `evolucao` mas só 2 ou 3 etapas e sem `legenda`. Sai como `story-NN.mp4`, sem cartão final. Use 1 por dia.
  - O tipo `link` mostra o preço e a linha "Link na bio · iaparaarquitetos.com.br" (já vem no modelo). É o último story do dia.
  - Não use o campo `nota`.
- Imagens disponíveis em `assets/img` (além das novas de `assets/img/novas`, ver 5b):
  - v-0, v-1.9, v-3.1, v-4.4, v-5.7, v-7.9 (obra da casa, vertical)
  - h-*, ia-arq-casa (horizontal)
  - w1/w2/w3 (antes e depois)

Gerar: `python3 engine/gera.py pautas/AAAA-MM-DD.json`. Leva cerca de 2 min e grava `saida/AAAA-MM-DD/` com `manifesto.json`. Antes de agendar, abra 1 quadro de cada reel, 1 slide de cada carrossel e todos os stories e confira se nada vazou da moldura.


## 5d. Estilo "evolução" (pedido do Marcos em 8/11/2026)

O Marcos mandou 6 reels de referência (planta que vira planta humanizada, obra crua que vira render, planta que vira estrutura e casa pronta, sempre com a mesma câmera) e pediu esse estilo nos reels, carrosséis e stories. Os 2 vídeos-modelo estão na LP (seção "Em movimento") e em `saida/estilo/`.

**Mix diário (desde 14/11):** 2 reels `evolucao` (1 interior, 1 casa) + 1 reel de outro tipo (pergunta-mito ou lista, que são os que mais alcançam; `wipe` no máximo 1 vez por semana); 1 carrossel (etapas no dia ímpar, normal no dia par); 1 story `evolucao` + 2 stories estáticos + o story `link` às 21:30.

**Sequências do dia (Canva, por referência):** cada dia gere 2 sequências novas no cenário do rodízio (5b), uma de interior e uma de casa:
- **Interior (4 imagens):** 1 planta técnica (desenho 2D preto sobre branco, vista de cima, cotas, sem texto legível) → 2 planta humanizada (`imageReferences` = imagem 1; "mesma planta, mesmas paredes e mesmo enquadramento, agora humanizada: vista de cima, pisos, móveis, plantas, sombras suaves") → 4 render do ambiente principal na altura do olho → 3 obra crua (`imageReferences` = imagem 4; "mesmo ambiente, mesma câmera e mesmas aberturas, em obra: concreto e reboco crus, sem móveis, tubulação aparente"). Gere a 4 antes da 3: a obra sai da imagem pronta, então as linhas casam.
- **Casa (3 imagens):** 1 planta da casa sobre a mesa (papel, régua, lápis, vista de cima) → 3 casa pronta em vista aérea 3/4 ao entardecer → 2 estrutura (`imageReferences` = imagem 3; "mesma casa, mesma câmera aérea, em estrutura de concreto: pilares, lajes, escada, sem fachada nem acabamento, terreno de obra").
- Todas em `PORTRAIT_9_16`, exportadas pelo design-base (5b) para `assets/img/novas/<cenario>-<data>/1-planta.jpg`, `2-...jpg` etc. Registre cada uma no `indice.json` com o campo `sequencia`.
- Confira as etapas lado a lado: mesma câmera, mesmas aberturas. Se uma etapa sair com outra geometria, gere de novo (até 2 vezes); se não acertar, troque a transição por `mergulho` (não depende de alinhamento).

**Transições** (campo `trans` da etapa, sempre a partir da 2ª):
- `scan` linha de luz de cima para baixo com grade (planta técnica → humanizada).
- `mergulho` com `foco: [x, y]` (0 a 1): a câmera entra naquele ponto da etapa anterior e sai na próxima (planta humanizada → interior; use o ponto da sala na planta).
- `linhas` o wireframe da próxima etapa se desenha por cima da anterior e depois revela (obra crua → render).
- `luz` a planta em papel acende como prancha luminosa e vira o wireframe da próxima (planta da casa → estrutura).
- `ergue` linha de luz de baixo para cima (estrutura → casa pronta). `lateral` da esquerda para a direita.
O gerador alinha sozinho cada etapa à anterior (`alinha: true`, padrão).

**Modelos prontos** (copie e troque imagens, textos e prompts):
```json
{"tipo": "evolucao", "horario": "...", "gancho": ["Da planta ao", "apartamento pronto"], "rotulo": "DA PLANTA À OBRA",
 "etapas": [
  {"img": "novas/estilo-apto/1-planta.jpg", "nome": "Planta técnica"},
  {"img": "novas/estilo-apto/2-humanizada.jpg", "nome": "Planta humanizada", "trans": "scan", "prompt": "humanize esta planta: vista de cima, piso de madeira clara, móveis e luz natural"},
  {"img": "novas/estilo-apto/3-obra.jpg", "nome": "Obra crua", "trans": "mergulho", "foco": [0.42, 0.52]},
  {"img": "novas/estilo-apto/4-render.jpg", "nome": "Render final", "trans": "linhas", "prompt": "mesma câmera, mesma arquitetura: sala e cozinha prontas, luz da tarde"}],
 "frase": ["O arquiteto decide.", "A IA executa."], "legenda": "...", "alt": "..."}
```
```json
{"tipo": "evolucao", "horario": "...", "gancho": ["Do projeto à", "casa pronta"], "rotulo": "DO PROJETO À CASA",
 "etapas": [
  {"img": "novas/estilo-casa/1-planta.jpg", "nome": "Planta"},
  {"img": "novas/estilo-casa/2-estrutura.jpg", "nome": "Estrutura", "trans": "luz", "prompt": "a partir desta planta: casa de 2 pavimentos, concreto aparente, piscina e jardim tropical"},
  {"img": "novas/estilo-casa/3-pronta.jpg", "nome": "Casa pronta", "trans": "ergue"}],
 "frase": ["Apresente a casa", "antes da obra."], "legenda": "...", "alt": "..."}
```
As pastas `novas/estilo-apto` e `novas/estilo-casa` são as sequências dos vídeos-modelo: use-as só se o Canva falhar no dia.

**Textos do estilo:** o `prompt` na tela é curto (até cerca de 90 caracteres) e diz o que muda e o que fica ("mesma câmera, mesma arquitetura"). Os nomes das etapas são de obra e projeto (Planta técnica, Planta humanizada, Obra crua, Estrutura, Render final, Casa pronta). A legenda explica a sequência em passos numerados e liga ao Workflow que mais se aproxima (W01 render a partir do modelo; W03 antes e depois mantendo a arquitetura), sem dizer que o manual traz um workflow de planta humanizada. Para a `frase`, alterne entre estas, sem repetir no mesmo dia: "O arquiteto decide. / A IA executa.", "Mesma câmera. / Mesma arquitetura.", "Apresente a casa / antes da obra.", "Do papel à / apresentação.", "A geometria fica. / O resto muda.".


## 5e. Biblioteca de modelos de referência (pedido do Marcos em 13/11/2026)

O Marcos vai trazer reels de referência que tiveram muitas curtidas e visualizações ("precisamos de vários modelos diferentes rodando ao mesmo tempo"). Cada referência vira um modelo nesta tabela, com a análise do que deu certo e o tipo de pauta que o replica. A rotina gira os modelos: os 3 reels do dia usam 3 modelos diferentes, e nenhum modelo aparece em 2 dias seguidos no mesmo horário. O estilo `evolucao` (5d) é o modelo M0.

| Modelo | Referência | O que deu certo (gancho, ritmo, texto, música) | Como replicar (tipo de pauta) | Status |
|---|---|---|---|---|
| M0 · Evolução | vídeos-modelo de 08/11 (`saida/estilo/`) | mesma câmera em etapas, linha de luz, prompt digitado | `evolucao` (5d) | ativo |
| M1 | https://www.instagram.com/p/Dey7uwKP-bv/ (planta → obra final) | aguardando o vídeo para análise | a definir | pendente |
| M2 | https://www.instagram.com/p/DeuFikVxyqk/ | aguardando o vídeo para análise | a definir | pendente |
| M3 | https://www.instagram.com/p/DdssRZkR9Zz/ | aguardando o vídeo para análise | a definir | pendente |
| M4 · Obra ganha vida | https://www.instagram.com/reel/De1_aGksYmg/ (@render3d.fabiogarcia, 12 s) | 1º quadro = obra crua (curiosidade); sem nenhum texto na tela, só o @ no canto; mesma câmera; cada elemento "brota" com borda orgânica (piso, forro, paredes, marcenaria, ilha, banquetas), ~0,5 s cada; no fim as luzes acendem; 8 s de construção + 4 s de fecho escurecido com o @ | `engine/constroi.py` modo `cresce` (base = obra crua, final = render, zonas na ordem piso → teto → janela → marcenaria → mesa → móveis; termina com luz dourada). Spec de exemplo: `saida/modelos/m4-homeoffice.json`. Capa com a palavra-chave (4b), vídeo sem texto | teste (aguarda aprovação) |
| M5 · Fachada em camadas | https://www.instagram.com/reel/DfGzx0pswmR/ (@luck_lucky934, 25 s) | fachada de frente, mesma câmera; muitas etapas curtas (tijolo → reboco → pintura → esquadrias → revestimento e luz → paisagismo e rua); troca por faixas verticais que deslizam de cima e de baixo; depois a câmera se move devagar sobre a casa pronta ao entardecer; sem texto; fecho com o @ | `engine/constroi.py` modo `faixas` (planta → estrutura → casa pronta, a última entrando em bandas; 3 s de câmera lenta no fim). Spec: `saida/modelos/m5-lago.json`. Quanto mais etapas da mesma câmera, melhor (gere 4 a 6 no Canva) | teste (aguarda aprovação) |
| — | perfil @render3d.fabiogarcia (melhores posts) | aguardando dados (concorrentes no Metricool) ou vídeos | a definir | pendente |
| — | perfil @luck_lucky934 (melhores posts, reels, stories e trilhas) | aguardando dados (concorrentes no Metricool) ou vídeos | a definir; trilha: só se existir no catálogo comercial do Instagram (audioConfiguration) | pendente |

Modelo pendente não entra na pauta. Quando um modelo ficar ativo, a rotina compara o alcance dele com os outros nas métricas do Metricool e registra no relatório do dia.

## 5b. Imagens novas todo dia (pedido do Marcos em 7/11/2026)

Todo dia a rotina **gera as 2 sequências do estilo evolução (7 imagens novas)** e as usa como fundo dos reels, capas de carrossel e stories. A regra é **alternar cenários para não ficar repetitivo**.

**Cenários em rodízio** (rotação na ordem abaixo, retomando de onde o último dia parou, conforme `assets/img/novas/indice.json`):
1. casa na praia
2. casa na montanha
3. apartamento (sala ampla, varanda, vista da cidade)
4. casa de bairro (casa térrea ou sobrado em rua residencial brasileira)
5. chalé de montanha
6. rancho na beira do rio
7. casa em frente ao lago
8. casa com piscina
9. área interna (alternar: sala, cozinha, banheiro com cuba de pedra, quarto, home office, varanda gourmet)
10. móveis em diferentes cenários (poltrona, mesa de jantar, aparador, luminária em ambientes variados)

Por dia: pegue os próximos 2 cenários da fila (um para a sequência de interior, outro para a de casa; se o cenário da vez for de casa, a sequência de interior usa a área interna mais próxima na fila). Imagem solta extra só se faltar fundo para algum story. Varie hora do dia (manhã, tarde, entardecer, noite com luz acesa), estação, materiais e estilo (contemporâneo, rústico, minimalista, tropical moderno, colonial reinterpretado). Nunca repita a mesma combinação cenário + estilo + hora em 14 dias.

**Como gerar (Canva, assinatura do Marcos):**
1. `Canva generate-image` com `aspectRatio: PORTRAIT_9_16` e um prompt em português no formato: "Fotografia de arquitetura editorial, vertical: <cenário detalhado: estilo, materiais, paisagem, hora do dia, luz>, câmera na altura do olho, verticais corrigidas, fotorrealista, sem pessoas, sem texto, sem logotipos". Espere uns 20 s e consulte `get-generate-image-job` até SUCCESS. Guarde o media id (ex.: MAHaQGVNws0).
2. Exportar em 1080×1920 pelo design-base **DAHaQBWKpg4** (página PB1LkPGXj3mBxQgL):
   1. `read-design` com `open_transaction: true`.
   2. `edit-design` com `update_fill` em `locator_id: PB1LkPGXj3mBxQgL`, `asset_type: image`, `asset_id: <media id>` e o alt text.
   3. `edit-design` com `finalize: commit`.
   4. `export-design` com `{"type":"jpg","quality":92,"width":1080,"height":1920}`.
   5. Baixe a URL do export com curl para `assets/img/novas/<cenario>-NN.jpg` (sem acento e sem espaço, ex.: `chale-montanha-03.jpg`).
3. Confira cada imagem antes de usar: abra o arquivo. Descarte imagem com texto, logotipo, pessoa deformada ou arquitetura incoerente.
4. Registre a imagem em `assets/img/novas/indice.json` (arquivo, cenário, data, canva_media, descrição) e, ao montar a pauta, anote em `usos` a data e a peça.
5. **Opcional, para reel `wipe`:** gere a versão "antes" da mesma imagem com `generate-image` e `imageReferences: [{type: MEDIA, id: <media id>}]`, com o prompt "Transforme esta imagem num modelo 3D branco sem textura (maquete eletrônica), mesma geometria e mesmo enquadramento". Exporte igual e use na pauta como `"par": {"antes": "novas/x-antes.jpg", "depois": "novas/x.jpg", "la": "Modelo · sem textura", "lb": "Render · IA"}`.

**Uso na pauta:** campo `fundo` da cena do reel, `img` da capa do carrossel e do story (`tipo: foto`, `pergunta` ou `link`): `"novas/arquivo.jpg"`.
- Dê preferência às imagens do dia. Cada imagem nova vale para no máximo 3 peças.
- As fotos antigas da obra (v-*, h-*) entram no máximo 1 vez por dia.
- O tema do texto conversa com o cenário. Ex.: casa de praia → prompt de render de fachada ao entardecer, materiais que aguentam maresia; móveis em cenários → Workflow 02 (peça no ambiente); área interna → luz e materiais; casa de bairro → antes e depois de reforma.
- Toda peça com imagem gerada vai com `ia: true`.

**Se o Canva falhar** (limite de geração ou erro): use as imagens do índice com menos usos e registre a falha no relatório do dia.


## 5c. Revisão das legendas e dos textos (obrigatória, antes de agendar)

O Marcos pediu atenção total aos textos. Antes de agendar, releia CADA legenda e CADA texto de tela como um revisor:
1. **Português:** acentos, crases, concordância, vírgulas, maiúsculas. Sem erro de digitação, sem palavra repetida na mesma frase, sem frase cortada.
2. **Fatos:** só os números do item 2 (7 workflows, 4 vídeo-aulas, 60 prompts, 7 templates, R$ 97, 12x de R$ 10,03, 7 dias de garantia, cerca de 15 min por render, 24 h para proposta). Nada inventado.
3. **Coerência:** a legenda fala da mesma coisa que a peça mostra (mesmo número de passos, mesmos nomes). O texto da tela casa com o cenário da imagem.
4. **Formato:** primeira linha com a palavra-chave e até cerca de 125 caracteres (o que aparece antes do "mais"). Parágrafos curtos, separados por linha em branco. Listas com "1 ·", "2 ·". De 3 a 5 hashtags no fim, sempre com #iaparaarquitetos. Legenda inteira com menos de 2.200 caracteres.
5. **Chamada:** termina em salvar, comentar, compartilhar ou "link na bio", nunca em adesivo de story. Sem pedir enquete ou caixa de perguntas.
6. **Tom:** arquiteto falando com arquiteto. Nada de "revolucionário", "segredo", "hack", caixa alta ou excesso de emoji.
7. Leia em voz alta mentalmente: se uma frase soa estranha, reescreva.

Corrija na pauta e gere de novo antes de agendar. Uma legenda com erro é pior que uma peça a menos.

## 6. Agendar no Metricool

- **Marca:** IA para Arquitetos, **blogId 7942089** (instagramData "ia.para.arquitetos"). Nunca use a Marmer Butik (6358659) nem a Alavanca Web (7942078).
- **Mídia:** URL pública do arquivo no GitHub:
  `https://raw.githubusercontent.com/marmerbutik-dotcom/ia-para-arquitetos-conteudo/main/saida/AAAA-MM-DD/ARQUIVO`.
  Faça o push antes de agendar. O Metricool baixa e hospeda a mídia no momento do agendamento.
- **Chamada:** `createScheduledPost`, com `providers: [{"network":"instagram"}]` e `autoPublish: true`. Cada tipo:
  - **Reel:** `instagramData: {"type":"REEL","showReelOnFeed":true,"isAiGenerated":<ia>}`, `media: [mp4]`, `videoThumbnailUrl: <capa.jpg>`, `text: legenda`, `mediaAltText: [alt]`.
  - **Carrossel:** `instagramData: {"type":"POST","isAiGenerated":<ia>}`, `media` com os slides em ordem, `text: legenda`, `mediaAltText` com o mesmo alt para cada slide.
  - **Story:** `instagramData: {"type":"STORY"}`, `media: [jpg ou mp4]`, sem `text`.
- **Data:** `date` e `publicationDate` no horário do manifesto, com timezone America/Sao_Paulo.
- **Horário já ocupado:** antes de agendar, chame getScheduledPosts do dia. Se um horário do item 1 já tiver um post (o Marcos ou uma sessão anterior pode ter agendado algo à mão), não agende outra peça do mesmo tipo nele: pule a peça correspondente da pauta e registre no relatório.
- **Conferência:** no fim, chame getScheduledPosts do dia e confira que são 8 posts (3 reels, 1 carrossel, 4 stories), contando os que já estavam agendados. Posts em rascunho (draft) não contam.
- **Erro:** se uma chamada der erro, corrija o JSON e tente de novo uma vez. Se falhar de novo, pule a peça e registre em `relatorios/AAAA-MM-DD.md`.

## 6b. 1 reel por dia na @marmerbutik (pedido do Marcos em 8/11/2026)

A Marmer Butik vende o manual, então todo dia vai **1 reel de estilo evolução** para o Instagram @marmerbutik. É só 1 por dia: "não muitos". Desde 13/11 a @marmerbutik também tem limite de 3 reels por dia, e este reel conta como um deles (a rotina semanal da Marmer faz os outros 2).
- **Marca:** Marmer Butik, **blogId 6358659**, rede só `instagram` (sem TikTok, Facebook, YouTube ou outras redes). É a ÚNICA peça que esta rotina agenda nessa marca.
- **Horário:** 14:00 (fuso de São Paulo). A grade de reels da Marmer é 09:30, 12:00, 16:30, 18:00, 20:00 e 21:00, e quem cuida dela é outra rotina, que não deve ser tocada. Antes de agendar, confira com getScheduledPosts (brandId 6358659, só o dia; a resposta é grande, filtre por horário) se 14:00 já tem um REEL de IA para Arquitetos. Se tiver, não agende outro.
- **Vídeo próprio, nunca o mesmo mp4 da @ia.para.arquitetos.** Renderize com `engine/evolui.py`, a partir de uma das sequências do dia (alterne: dia par casa, dia ímpar interior), com outro `gancho`, outra `frase`, prompts de tela diferentes e `"rotulo": "MARMER BUTIK"`. Pode usar 3 etapas em vez de 4. Grave em `saida/marmer/AAAA-MM-DD-<tema>.mp4` e a capa ao lado (`capa=`). Exemplo: `python3 -c "import sys,json; sys.path.insert(0,'engine'); import evolui; evolui.render(json.load(open('spec.json')),'saida/marmer/AAAA-MM-DD-casa.mp4',capa='saida/marmer/AAAA-MM-DD-casa-capa.jpg',som_ofs=9)"`.
- **Legenda (voz da Marmer, para o público dela: arquitetos, designers e clientes de alto padrão):**
  - 1ª linha com a palavra-chave ("render com IA", "IA para arquitetos", "projeto de arquitetura com IA").
  - Pergunta e resposta curta. Passos numerados com o que o vídeo mostra.
  - Uma frase dizendo que o manual IA para Arquitetos é da Marmer Butik, com os fatos do item 2.
  - Chamada: "Conheça o manual em iaparaarquitetos.com.br e siga @ia.para.arquitetos". O link da bio da @marmerbutik é da loja: nunca escreva "link na bio" nesse post.
  - Hashtags: #iaparaarquitetos #marmerbutik #arquitetura + 1 ou 2 do tema.
  - Passe a legenda pelo checklist 5c.
- **Agendar:** `createScheduledPost` com blogId 6358659, `providers: [{"network":"instagram"}]`, `instagramData: {"type":"REEL","showReelOnFeed":true,"isAiGenerated":true}`, `videoThumbnailUrl` com a capa, `mediaAltText` e autoPublish true. Registre o id no relatório do dia, numa linha "Marmer".
- **Limpeza:** `saida/marmer/` segue a mesma regra de limpeza das pastas do dia: apague os arquivos com mais de 3 dias.

## 7. Depois de agendar

- Grave `relatorios/AAAA-MM-DD.md` com: o que foi agendado (horário, tipo, tema, cenário, id do Metricool) e qualquer falha.
- Apague as pastas `saida/` com mais de 3 dias. O Metricool já hospedou a mídia e o repositório fica leve.
- Commit e push.
- Se houver ferramenta de arquivos do computador do Marcos disponível (mcp__remote-devices__device_commit_files), salve também uma cópia da pasta do dia em `C:\Users\Marcos\Pictures\IA para Arquitetos\Instagram\rotina-diaria\AAAA-MM-DD\` (pasta que ele pediu para guardar o conteúdo). Se não houver, siga sem ela.
- Mande ao Marcos um resumo de 3 a 5 linhas: os temas do dia e o primeiro horário.
