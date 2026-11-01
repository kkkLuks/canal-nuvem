# Pipeline do canal dark

Plano de como os vídeos são pesquisados, produzidos e publicados, todos na nuvem.

## Visão

- **Agora (fase 1, semi-manual):** o Claude roda na nuvem, procura outliers, escreve roteiros e monta os vídeos; o Luks aprova cada vídeo antes de publicar.
- **Meta (fase 3, autônomo):** o Claude trabalha sozinho 24/7, postando todos os dias, vídeos longos e shorts, em vários canais.
- **Restrição:** custo baixo por vídeo. O único serviço pago por geração é a voz.

## Stack

| Etapa | Ferramenta | Custo |
|---|---|---|
| Achar outliers (vídeos que performam muito acima da média do canal) | vidIQ (conector) + YouTube Data API | assinatura vidIQ / grátis (cota da API) |
| Roteiro | Claude | incluso |
| Narração | Higgsfield (só voz: `seed_audio` ou `text2speech_v2`) | créditos Higgsfield |
| Footage | Bancos gratuitos com licença clara (Pexels, Pixabay, Wikimedia Commons, Internet Archive / domínio público) | grátis |
| Montagem, legendas, motion graphics | [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → MP4, open source) + FFmpeg | grátis (CPU do servidor) |
| Upload | YouTube Data API v3 com OAuth (um token por canal) | grátis (cota da API) |
| Live 24h (opcional) | FFmpeg → RTMP do YouTube Live | grátis (CPU do servidor) |

## Fluxo de um vídeo

```
outlier ─► tema + ângulo ─► roteiro ─► narração (Higgsfield)
                                   └─► lista de cenas ─► footage (bancos grátis)
narração + footage + legendas ─► composição HyperFrames ─► render MP4
MP4 + título + descrição + thumbnail ─► revisão do Luks (fase 1) ─► upload OAuth
```

1. **Pesquisa de outliers:** buscar vídeos do nicho com views muito acima da média do próprio canal (vidIQ `outliers` / YouTube search). Guardar tema, título, gancho e duração.
2. **Roteiro:** texto original inspirado no tema (nunca cópia), com gancho nos primeiros 15s. Longo: 8–15 min. Short: 30–60s.
3. **Narração:** gerar o áudio no Higgsfield; sempre checar o custo (`get_cost`) antes.
4. **Cenas e footage:** quebrar o roteiro em cenas com palavras-chave; baixar clipes/imagens com licença que permite uso comercial e registrar a fonte de cada um (`credits.json`).
5. **Montagem:** composição HyperFrames com footage, Ken Burns em imagens, legendas sincronizadas, trilha sem direitos autorais. Render 16:9 (longo) e 9:16 (short).
6. **Publicação:** upload via OAuth, com metadados e thumbnail; vídeos com voz de IA marcados como conteúdo sintético quando exigido pelo YouTube.

## Fases

- **Fase 1 (agora):** um canal, em português, nicho finanças e histórias de negócios. Vídeos produzidos sob demanda, com aprovação manual. Medir custo e tempo por vídeo.
- **Fase 2:** rotina agendada (busca de outliers diária + fila de roteiros), ainda com aprovação.
- **Fase 3:** publicação automática diária, vários canais, shorts derivados dos vídeos longos.

## Custo e limites

- Voz é o custo variável: medir créditos por minuto de narração no primeiro piloto e definir orçamento diário.
- A cota padrão da YouTube Data API é 10.000 unidades/dia por projeto; cada upload custa ~1.600, então ~6 uploads/dia por projeto Google Cloud.
- O conector do Higgsfield funciona dentro das sessões do Claude. Para rodar fora delas, verificar se há API com chave própria.

## Segredos

Tokens OAuth, chaves de API e chave de stream ficam em variáveis de ambiente ou no gerenciador de segredos do servidor. Nunca no repositório.
