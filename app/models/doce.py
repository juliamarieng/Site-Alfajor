from dataclasses import dataclass


@dataclass(frozen=True)
class Doce:
    id: str
    nome: str
    preco: float
    categoria: str
    cor: str
    topo: str
    descricao: str = ""
    tipo: str = "brigadeiro"  # "brigadeiro" ou "alfajor" (define o desenho)


class DoceRepositorio:
    """Fonte dos dados da vitrine. Para usar um banco depois, só este arquivo muda."""

    _DOCES = (
        Doce("brigadeiro-tradicional", "Brigadeiro tradicional", 6.00, "brigadeiros",
             "#4a2418", "#fff8ec", "O clássico de chocolate, cremoso, com granulado."),
        Doce("ninho", "Brigadeiro de ninho", 6.00, "brigadeiros",
             "#f1e8d2", "#e23d68", "Leite ninho cremoso, o favorito das festas."),
        Doce("beijinho", "Beijinho", 6.00, "tradicionais",
             "#f4efe0", "#d9a441", "Coco e leite condensado, passado no açúcar."),
        Doce("nutella", "Nutella", 7.00, "tradicionais",
             "#6b4a3a", "#fff8ec", "Brigadeiro com o sabor intenso da Nutella."),
        Doce("pacoca", "Paçoca", 7.00, "tradicionais",
             "#d9a95a", "#8a5a2b", "Sabor de paçoca de verdade, com textura macia."),
        Doce("maracuja", "Brigadeiro de maracujá", 6.00, "finos",
             "#fe9a3c", "#fff1a8", "Doce e levemente azedinho, bem refrescante."),
        Doce("alfajor-doce-de-leite", "Alfajor de doce de leite", 6.00, "tradicionais",
             "#e8c48c", "#a8602a", "Massa macia, recheio generoso e cobertura artesanal.",
             tipo="alfajor"),
    )

    def todos(self):
        return list(self._DOCES)

    def buscar(self, doce_id):
        for d in self._DOCES:
            if d.id == doce_id:
                return d
        return None

    def por_ids(self, ids):
        return [d for d in (self.buscar(i) for i in ids) if d]
