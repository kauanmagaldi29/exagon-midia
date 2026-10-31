# Ferramentas de conteúdo (@exagondigital)

## Preparar (uma vez)

```bash
cd ferramentas/video && npm install          # baixa a fonte Outfit (@fontsource/outfit)
pip install playwright                        # se ainda não tiver; precisa do Chromium do Playwright
```

## Artes (posts e stories)

- `artes/arts.py`: Pousadas Fácil, posts p1–p7 e stories s1–s7 (semana 2–8/11)
- `artes/arts_ex.py`: Exagon, posts ex1–ex3 e stories es1–es3
- `artes/arts_ex2.py`: Exagon "Seu sistema dá problema?" (ex4 e es4). Reaproveita o CSS e as funções das linhas 1–36 e 82–85 do arts_ex.py.

Rodar: `cd artes && python3 arts_ex.py`. As imagens saem em `artes/out/`.

Medidas: post 1080×1350; story 1080×1920, com 120 px livres em cima e os elementos de baixo a 240 px da borda.

## Vídeo (motor do Reel "Sua pousada não evolui?")

É uma página HTML animada, fotografada quadro a quadro e montada com o ffmpeg.

- `index.html`: as cenas (A–M), as telas verdes de transição e as legendas
- `anim.js`: quando cada cena entra e sai, as animações, a lista de efeitos sonoros e `window.renderAt(t)`
- `data.js`: as legendas sincronizadas com a narração (gerado pelo align.py)
- `align.py`: alinha o texto da narração com o áudio (detecta silêncios, deslocamento de 0,3 s)
- `sfx.py`: gera os efeitos sonoros
- `rv.py`: renderiza (`meta`, `preview`, `scene NOME F0 F1`), em JPEG para o ffmpeg (libx264 crf 17, 30 fps)
- `runA.sh` / `runB.sh`: dois renderizadores em paralelo, divididos pelo `chunks.json`
- `cover.py`: gera a capa (`capa.png`)
- `narr.mp3`: a narração usada (ElevenLabs, voz "Will - Slow, Confident and Distant")

Mixagem final: narração atrasada 300 ms, efeitos ×0,6, `loudnorm I=-14:TP=-1.5`. As partes são juntadas com o concat do ffmpeg (`-c copy`) e o áudio entra com `-c:v copy`.
