"""Coletor do painel: views, inscritos e receita de todos os canais.

Lê, para cada canal autorizado, o YouTube Data API (dados do canal e vídeos
recentes) e o YouTube Analytics API (views, inscritos e receita por dia), e
grava JSONs de linhas em painel/out/, no formato que o painel Máquina de
Vídeos lê:

    canais.json   um canal por linha (mesmas colunas da aba Canais)
    diario.json   canal × dia: views, minutos assistidos, inscritos, receita
    videos.json   vídeos recentes de cada canal, com views e se é Short

Variáveis de ambiente (segredos do ambiente da nuvem, nunca no repositório):
    YT_CLIENT_ID, YT_CLIENT_SECRET  app OAuth do Google Cloud
    YT_REFRESH_TOKENS               um token por canal, separados por vírgula
                                    (gerados com painel/autorizar.py)
    DIAS                            janela do diário (padrão 90)

Uso: python3 painel/coletor.py
"""

from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/youtube/v3"
ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
SAIDA = pathlib.Path(__file__).resolve().parent / "out"


def http_json(url: str, token: str | None = None, dados: bytes | None = None) -> dict:
    req = urllib.request.Request(url, data=dados)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def access_token(refresh: str) -> str:
    corpo = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": refresh,
        "grant_type": "refresh_token",
    }).encode()
    return http_json("https://oauth2.googleapis.com/token", dados=corpo)["access_token"]


def get(token: str, caminho: str, **params) -> dict:
    return http_json(f"{API}/{caminho}?{urllib.parse.urlencode(params)}", token)


def relatorio(token: str, inicio: str, fim: str, metricas: list[str], **extra) -> list[dict]:
    q = {"ids": "channel==MINE", "startDate": inicio, "endDate": fim,
         "metrics": ",".join(metricas), **extra}
    r = http_json(f"{ANALYTICS}?{urllib.parse.urlencode(q)}", token)
    nomes = [c["name"] for c in r.get("columnHeaders", [])]
    return [dict(zip(nomes, linha)) for linha in r.get("rows", [])]


def diario(token: str, inicio: str, fim: str) -> tuple[list[dict], bool]:
    """Views e inscritos por dia; receita quando o canal é monetizado."""
    base = ["views", "estimatedMinutesWatched", "subscribersGained", "subscribersLost"]
    try:
        return relatorio(token, inicio, fim, base + ["estimatedRevenue"], dimensions="day", sort="day"), True
    except urllib.error.HTTPError as e:
        if e.code not in (400, 403):
            raise
        # Canal sem monetização (ou sem o escopo monetário): segue sem receita.
        return relatorio(token, inicio, fim, base, dimensions="day", sort="day"), False


def duracao_s(iso: str) -> int:
    """PT1M5S -> 65."""
    n, total = "", 0
    for ch in iso.replace("PT", ""):
        if ch.isdigit():
            n += ch
        else:
            total += int(n or 0) * {"H": 3600, "M": 60, "S": 1}.get(ch, 0)
            n = ""
    return total


def videos_recentes(token: str, uploads: str, limite: int = 50) -> list[dict]:
    ids = [i["contentDetails"]["videoId"] for i in
           get(token, "playlistItems", part="contentDetails", playlistId=uploads, maxResults=limite).get("items", [])]
    if not ids:
        return []
    itens = get(token, "videos", part="snippet,statistics,contentDetails", id=",".join(ids)).get("items", [])
    out = []
    for v in itens:
        d = duracao_s(v["contentDetails"]["duration"])
        out.append({
            "id": v["id"],
            "titulo": v["snippet"]["title"],
            "publicado": v["snippet"]["publishedAt"],
            "duracao_s": d,
            "views": int(v["statistics"].get("viewCount", 0)),
            "short": d <= 180,
        })
    return out


def main() -> None:
    tokens = [t.strip() for t in os.environ.get("YT_REFRESH_TOKENS", "").split(",") if t.strip()]
    if not tokens or "YT_CLIENT_ID" not in os.environ:
        sys.exit("Faltam YT_CLIENT_ID, YT_CLIENT_SECRET ou YT_REFRESH_TOKENS. Veja painel/README.md.")

    hoje = dt.date.today()
    fim = (hoje - dt.timedelta(days=1)).isoformat()
    inicio = (hoje - dt.timedelta(days=int(os.environ.get("DIAS", "90")))).isoformat()

    canais, dias, videos, falhas = [], [], [], []
    for n, refresh in enumerate(tokens, 1):
        try:
            tok = access_token(refresh)
            ch = get(tok, "channels", part="snippet,statistics,contentDetails", mine="true")["items"][0]
            cid = ch["id"]
            st = ch["statistics"]
            canais.append({
                "channelId": cid,
                "title": ch["snippet"]["title"],
                "handle": ch["snippet"].get("customUrl"),
                "subscriberCount": None if st.get("hiddenSubscriberCount") else int(st.get("subscriberCount", 0)),
                "viewCount": int(st.get("viewCount", 0)),
                "videoCount": int(st.get("videoCount", 0)),
            })
            linhas, com_receita = diario(tok, inicio, fim)
            for l in linhas:
                dias.append({
                    "channelId": cid,
                    "canal": ch["snippet"]["title"],
                    "dia": l["day"],
                    "views": int(l["views"]),
                    "minutos": int(l["estimatedMinutesWatched"]),
                    "inscritos": int(l["subscribersGained"]) - int(l["subscribersLost"]),
                    "receita_usd": round(float(l["estimatedRevenue"]), 2) if com_receita else None,
                })
            for v in videos_recentes(tok, ch["contentDetails"]["relatedPlaylists"]["uploads"]):
                videos.append({"channelId": cid, "canal": ch["snippet"]["title"], **v})
            print(f"ok  {ch['snippet']['title']}: {len(linhas)} dias, receita {'sim' if com_receita else 'não'}")
        except Exception as e:  # um canal com problema não derruba os outros
            falhas.append(f"token {n}: {e}")
            print(f"erro token {n}: {e}", file=sys.stderr)

    SAIDA.mkdir(exist_ok=True)
    for nome, linhas in (("canais", canais), ("diario", dias), ("videos", videos)):
        (SAIDA / f"{nome}.json").write_text(json.dumps(linhas, ensure_ascii=False))
    (SAIDA / "estado.json").write_text(json.dumps({
        "gerado": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "janela": [inicio, fim], "canais": len(canais), "falhas": falhas,
    }, ensure_ascii=False, indent=1))
    if falhas and not canais:
        sys.exit(1)


if __name__ == "__main__":
    main()
