from flask import render_template

from app.models.doce import DoceRepositorio
from app.models.pedido import Pedido


class Application:
    """Único controller: as rotas em route.py só delegam para cá."""

    def __init__(self, config):
        self._config = config
        self._repo = DoceRepositorio()
        self._pages = {"index": self._index}

    # ---------- páginas ----------
    def render(self, page):
        return self._pages.get(page, self._index)()

    def _index(self):
        return render_template(
            "index.html",
            doces=self._repo.todos(),
            destaques=self._repo.por_ids(
                ["brigadeiro-tradicional", "ninho", "beijinho", "alfajor-doce-de-leite"]
            ),
        )

    # ---------- ações ----------
    def criar_pedido(self, dados):
        pedido = Pedido.de_dados(dados, self._repo)
        erros = pedido.validar()
        if erros:
            return {"erros": erros}, 400
        return {"url": pedido.url_whatsapp(self._config["WHATSAPP_NUMERO"])}, 200

    @staticmethod
    def moeda(valor):
        return Pedido.moeda(valor)
