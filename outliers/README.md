# Outliers do canal dark

Busca diária de vídeos de finanças e histórias de negócios que estão performando muito acima da média do próprio canal. É o mesmo motor do `kkkLuks/luks-outlier-nuvem` (views ÷ mediana dos vídeos vizinhos do canal), sem os filtros de games.

- `python3 nicho.py diario`: 6 buscas em rodízio (de `data/buscas.txt`), atualização dos canais e ranking em `out/rank.txt` (longos e shorts separados).
- Precisa da variável `YT_API_KEY` (chave só de leitura da YouTube Data API) no ambiente da nuvem. Nunca coloque a chave no repositório.
- O ambiente da nuvem precisa liberar `www.googleapis.com`.
- Cota: cada busca custa 100 unidades, e cada canal custa ~3. Limite padrão: 9000 por dia (`NICHO_QUOTA`).
- `topics` no banco guarda o que já foi julgado; um vídeo julgado some do ranking.
