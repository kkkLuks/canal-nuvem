# Painel da Máquina de Vídeos

O painel é uma página privada no claude.ai (tipo Dashboard) com quatro abas: Visão geral (views, inscritos e receita somados de todos os canais), Pipeline (cada vídeo de outlier até publicado), Outliers e Laboratório.

Este diretório tem o que alimenta o painel com dados do YouTube:

- `autorizar.py`: roda uma vez por canal no seu computador e imprime o refresh token OAuth (escopos de leitura do YouTube, do Analytics e da receita).
- `coletor.py`: roda na nuvem, usa os tokens e grava `out/canais.json`, `out/diario.json` (views, inscritos e receita por dia, por canal) e `out/videos.json`. Só usa a biblioteca padrão do Python.

## Ligar a receita

1. No [Google Cloud Console](https://console.cloud.google.com/), num projeto, ative **YouTube Data API v3** e **YouTube Analytics API**.
2. Crie uma credencial OAuth do tipo **App para computador**. Na tela de consentimento, deixe o app em produção (em modo teste o refresh token vence em 7 dias).
3. Para cada canal: `YT_CLIENT_ID=... YT_CLIENT_SECRET=... python3 painel/autorizar.py` e escolha o canal no Google.
4. No ambiente da nuvem, guarde `YT_CLIENT_ID`, `YT_CLIENT_SECRET` e `YT_REFRESH_TOKENS` (tokens separados por vírgula). O ambiente precisa liberar `oauth2.googleapis.com`, `www.googleapis.com` e `youtubeanalytics.googleapis.com`.
5. `python3 painel/coletor.py` gera os arquivos, e a rotina do Claude envia cada um para o painel.

A receita (`estimatedRevenue`, em dólar) só aparece para canais monetizados e chega com uns 2 a 3 dias de atraso. Canais sem monetização entram com receita vazia.

`out/` não vai para o git.
