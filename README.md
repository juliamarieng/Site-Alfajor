# Ju Alfajor Doceria — Flask em arquitetura MVC (sem Docker)

## Rodar
    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    python run.py
Acesse: http://localhost:5000

## Estrutura (BMVC)
- Model:      app/models/      -> Doce, DoceRepositorio, Pedido (regras e validação)
- View:       app/views/       -> templates Jinja + app/static (CSS, JS)
- Controller: app/controllers/ -> rotas: GET / e POST /pedido

