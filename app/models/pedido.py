from dataclasses import dataclass, field
from datetime import date
from urllib.parse import quote


@dataclass
class ItemPedido:
    doce: object
    quantidade: int

    @property
    def subtotal(self):
        return self.doce.preco * self.quantidade


@dataclass
class Pedido:
    nome: str
    itens: list = field(default_factory=list)
    data: str = ""
    mensagem: str = ""

    # ---------- construção a partir do que o navegador enviou ----------
    @classmethod
    def de_dados(cls, dados, repositorio):
        dados = dados if isinstance(dados, dict) else {}
        itens = []
        brutos = dados.get("itens")
        if isinstance(brutos, dict):
            for doce_id, qtd in brutos.items():
                doce = repositorio.buscar(doce_id)
                try:
                    qtd = int(qtd)
                except (TypeError, ValueError):
                    continue
                if doce and 1 <= qtd <= 99:
                    itens.append(ItemPedido(doce, qtd))
        return cls(
            nome=str(dados.get("nome", "")).strip()[:80],
            itens=itens,
            data=str(dados.get("data", "")).strip(),
            mensagem=str(dados.get("mensagem", "")).strip()[:500],
        )

    # ---------- regras de negócio ----------
    def validar(self):
        erros = []
        if not self.nome:
            erros.append("Informe seu nome para enviar o pedido.")
        if not self.itens and not self.mensagem:
            erros.append("Escolha um doce ou escreva uma mensagem antes de enviar.")
        if self.data:
            try:
                if date.fromisoformat(self.data) < date.today():
                    erros.append("A data precisa ser hoje ou depois.")
            except ValueError:
                erros.append("Data inválida.")
        return erros

    @property
    def total(self):
        return sum(i.subtotal for i in self.itens)

    @staticmethod
    def moeda(v):
        return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def texto(self):
        linhas = [f"Olá! Meu nome é {self.nome}."]
        if self.itens:
            linhas += ["", "Gostaria de encomendar:"]
            linhas += [f"• {i.quantidade}x {i.doce.nome}" for i in self.itens]
            linhas.append(f"Total estimado: {self.moeda(self.total)}")
        if self.data:
            a, m, d = self.data.split("-")
            linhas += ["", f"Data: {d}/{m}/{a}"]
        if self.mensagem:
            linhas += ["", self.mensagem]
        return "\n".join(linhas)

    def url_whatsapp(self, numero):
        return f"https://wa.me/{numero}?text={quote(self.texto())}"
