# Montagem de vídeo na nuvem (piloto: Varig)

Pipeline que transforma roteiro + narração em vídeo longo e Shorts, sem usar o PC.
Estilo: docs/ESTILO.md (papel quadriculado, recortes a 8 FPS, câmera com push-in, luz por fase).

## Passos

1. **Narração** (Higgsfield, ElevenLabs voz "Andre"): um MP3 por capítulo em `voz/capN.mp3`. Custo medido: ~0,0032 crédito por caractere (~30 créditos para 9.600 caracteres).
2. **Tempo de cada palavra**: `python3 tools/align.py narr.json words.json` (faster-whisper "small", alinha o texto do roteiro com as palavras ouvidas).
3. **Imagens livres**: `python3 tools/flickr.py plano_imgs.json` baixa fotos do Flickr só com licença que permite uso comercial e adaptação (CC BY, CC BY-SA, CC0, domínio público) e grava `assets/credits.json`. A Wikimedia devolve 429 para o IP da nuvem.
4. **Mapas**: `node tools/maps.mjs` (Natural Earth via world-atlas + d3-geo).
5. **Cenas**: `cenas.py` descreve cada cena pela palavra da narração que a dispara; `props.py` desenha os recortes em SVG; `engine.js` anima tudo em função do tempo (determinístico) dentro do HyperFrames.
6. **Build**: `python3 build.py` gera um projeto HyperFrames por capítulo em `build/capN/` e `build/timeline.json` (palavras, efeitos, fases).
7. **Som**: `python3 audio.py build/timeline.json build/mix.wav` sintetiza efeitos e trilha por fase (auge, virada, queda), abaixa a trilha sob a voz e mixa.
8. **Render**: `tools/render_all.sh 0 1 2 3 4 5 6 7 8` (HyperFrames, 30 fps, ~5 quadros/s numa máquina de 4 CPUs).
9. **Final**: `tools/final.sh` junta os capítulos, coloca o áudio e normaliza em -14 LUFS.
10. **Shorts**: `python3 shorts.py final/varig-longo.mp4` corta os trechos, reenquadra em 1080x1920 e coloca o título.

QA: `tools/snaps.sh 0 1 ...` gera folhas de stills por capítulo em `qa/`.

Dependências: Node 22 + `hyperframes@0.8.226`, `world-atlas@2.0.2`, `d3-geo@3.1.1`, `topojson-client@3.1.0`, `@fontsource/{anton,special-elite,oswald,permanent-marker}`; Python com `faster-whisper`, `numpy`, `scipy`, `pillow`, `fonttools`; FFmpeg.
