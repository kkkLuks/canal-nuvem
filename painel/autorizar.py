"""Autoriza um canal do YouTube uma vez e imprime o refresh token.

Rode no seu computador (precisa de navegador), uma vez por canal:

    YT_CLIENT_ID=... YT_CLIENT_SECRET=... python3 painel/autorizar.py

Na tela do Google, escolha a conta e o canal (contas de marca aparecem na lista).
O refresh token impresso vai para o segredo YT_REFRESH_TOKENS do ambiente da
nuvem. Nunca coloque o token no repositório.
"""

import http.server
import json
import os
import secrets
import sys
import urllib.parse
import urllib.request
import webbrowser

ESCOPOS = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
]
PORTA = int(os.environ.get("PORTA", "8765"))
REDIRECT = f"http://127.0.0.1:{PORTA}/"


def main() -> None:
    cid = os.environ.get("YT_CLIENT_ID")
    csec = os.environ.get("YT_CLIENT_SECRET")
    if not cid or not csec:
        sys.exit("Defina YT_CLIENT_ID e YT_CLIENT_SECRET (app OAuth do tipo 'App para computador').")

    estado = secrets.token_urlsafe(16)
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid,
        "redirect_uri": REDIRECT,
        "response_type": "code",
        "scope": " ".join(ESCOPOS),
        "access_type": "offline",
        "prompt": "consent select_account",
        "state": estado,
    })
    recebido: dict = {}

    class Retorno(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            recebido.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("Pronto, pode fechar esta aba.".encode())

        def log_message(self, *a):
            pass

    print("Abrindo o navegador. Se não abrir, cole este link:\n" + url)
    webbrowser.open(url)
    with http.server.HTTPServer(("127.0.0.1", PORTA), Retorno) as srv:
        while "code" not in recebido and "error" not in recebido:
            srv.handle_request()

    if recebido.get("state") != estado or "code" not in recebido:
        sys.exit(f"Autorização falhou: {recebido.get('error', 'estado inválido')}")

    corpo = urllib.parse.urlencode({
        "code": recebido["code"],
        "client_id": cid,
        "client_secret": csec,
        "redirect_uri": REDIRECT,
        "grant_type": "authorization_code",
    }).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", corpo) as r:
        tok = json.load(r)
    if "refresh_token" not in tok:
        sys.exit("O Google não devolveu refresh token. Remova o acesso do app em myaccount.google.com/permissions e rode de novo.")
    print("\nRefresh token deste canal (guarde como segredo):\n")
    print(tok["refresh_token"])


if __name__ == "__main__":
    main()
