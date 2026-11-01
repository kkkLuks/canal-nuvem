# Estilo de edição do canal dark (finanças e negócios)

Formato do piloto: **"a marca que dominou e sumiu"** (ex.: Mappin, Varig, Orkut, Kodak, Blockbuster).
Montagem 100% em código no HyperFrames (HTML → MP4) + FFmpeg, sem gravar nada e sem gerar vídeo por IA. Voz do Higgsfield.

## De onde vem cada regra

- **mromidev/claude-animated-shorts** (skill "cartoon-3d-short", Remotion + three.js): fórmula de roteiro, plano de cenas amarrado às palavras da narração, regras de câmera, som sintetizado e QA quadro a quadro. Lá é Remotion; aqui a gente porta as ideias para o HyperFrames, que também roda three.js/canvas dentro do HTML.
- **luks-ai-memory** (regras já aprovadas pelo Luks no canal de games): papel + fundo quadriculado a ~8 FPS para conteúdo investigativo, footage em duas camadas (nítido na frente, mesmo footage ampliado e borrado atrás), pouco texto na tela, texto sempre com som, letra branca com contorno preto e sombra suave (amarelo só no dado principal), hook animado desde o quadro 0, nada de painel parado, luz sem estourar, zoom agressivo que não corta o que importa, trilha que acompanha o humor.

## Roteiro (adaptado da fórmula medida em 20 shorts da referência)

1. **Gancho = paradoxo dito como fato, na 1ª frase, sem introdução.** "Em 1980, metade do Brasil comprava no Mappin. Em 1999, ele não existia mais."
2. **Cenário em 1–2 frases:** ano, lugar, orgulho, números concretos.
3. **Escalada em 3–6 passos:** o auge, cada passo um pouco maior (lojas, faturamento, propaganda que todo mundo lembra).
4. **Pergunta no meio:** "Então como uma empresa desse tamanho some?"
5. **Virada com "Só que...":** o mecanismo real (dívida, inflação, concorrente, decisão errada), explicado com uma analogia do dia a dia.
6. **Queda:** o momento em que quebra.
7. **Final irônico em 1–2 frases:** o que sobrou hoje. O vídeo acaba na última palavra, sem "se inscreva" no fim.
- Ritmo: ~3,5–3,8 palavras/s, frases faladas, nada de travessão nem lista disfarçada (checagem anti-IA do script_check).
- Short: 45–70 s. Longo: 8–15 min com a mesma estrutura repetida por capítulos.
- Todo fato com fonte anotada no topo do roteiro. Nunca copiar roteiro de outro canal.

## Imagem

- **Base: mesa de arquivo/jornal.** Fundo de papel quadriculado creme, recortes com borda de papel, sombra leve, movimento a ~8 FPS (stop motion), retícula e desgaste discretos.
- **Cada frase vira uma ação**, não um texto: logo da marca entra como recorte, gráfico de faturamento que se desenha, mapa do Brasil com lojas pipocando, notas de dinheiro voando, manchete de jornal antiga que gira para a câmera, carimbo "FALÊNCIA".
- **Footage real** (Wikimedia Commons, Internet Archive, Pexels/Pixabay) em moldura de papel, ou em duas camadas quando não preenche 9:16. Fonte de cada arquivo em `credits.json`.
- **Câmera:** segura ~80% do tempo com push-in lento (0,15–0,35%/quadro, mais nas palavras de impacto), movimentos curtos com ease-out (pico no 1º quadro e decai em 8–10 quadros), corte seco só em salto grande de lugar ou tempo, crossfade de 6–8 quadros ao trocar de época, tremor que inverte a cada quadro e some em 7 quadros só em impacto.
- **Luz por fase:** auge = tons quentes e saturados; virada = mais frio; queda = dessaturado e escuro. Nunca branco estourado.
- **Texto:** só dado (R$, ano, %), nome que a imagem não mostra ou citação de fonte. Branco, contorno preto, sombra suave; amarelo no número principal. Legenda de palavra a palavra só se o Luks pedir.
- **Sincronia:** tudo amarrado ao `words.json` (tempo de cada palavra da narração). A reação visual chega 0–3 quadros antes da palavra.

## Som

- Voz Higgsfield, tom estável, -14 LUFS no final.
- Trilha que muda com a fase (auge animado, virada tensa, queda melancólica), abaixada sob a voz.
- SFX por ação: papel, carimbo, caixa registradora, moedas, máquina de escrever no texto digitado, swoosh no texto que entra.

## QA antes de mostrar ao Luks

- Quadros pretos, brancos, congelados (≥12 quadros parados) e pulos.
- Loudness, nada de SFX alto demais.
- Folha de stills a cada 2 s para revisão rápida.
