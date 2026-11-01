# Canal na nuvem

Projeto para gerar e transmitir vídeos/lives **24 horas por dia** inteiramente na nuvem, sem usar o processamento, a internet ou a energia do PC pessoal.

## Objetivo

- Rodar uma transmissão contínua (24/7) para YouTube (e, opcionalmente, outras plataformas) a partir de um servidor na nuvem.
- Gerar e montar o conteúdo (vídeos, playlists, áudio, overlays) também na nuvem.
- O PC pessoal só é usado para configurar e acompanhar, nunca para renderizar ou transmitir.

## Ideia de arquitetura (inicial)

1. **Servidor na nuvem** (VPS barata, ex.: Oracle Cloud Free Tier, Hetzner, Contabo) rodando Linux.
2. **FFmpeg** fazendo loop de uma playlist de vídeos e enviando via RTMP para o YouTube Live.
3. **Supervisor/systemd** para reiniciar a live automaticamente se cair.
4. **Pasta de conteúdo** (no próprio servidor ou em armazenamento de objetos) com os vídeos que entram na rotação.
5. (Futuro) Geração automática de vídeos novos com ferramentas de IA e agendamento.

## Próximos passos

- [ ] Escolher o provedor de nuvem
- [ ] Criar script de transmissão 24h com FFmpeg
- [ ] Configurar reinício automático
- [ ] Definir o tema/nicho do canal e o conteúdo da playlist
- [ ] Documentar como colocar a chave de stream com segurança (variável de ambiente, nunca no repositório)
