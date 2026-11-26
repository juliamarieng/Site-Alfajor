
# Doceria — Flask em arquitetura BMVC (sem Docker)

# Ju Alfajor Doceria — Flask em arquitetura MVC (sem Docker)

## Rodar
    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    
    python route.py
Acesse: http://localhost:5000

## Estrutura (BMVC)
- route.py                       -> rotas (GET /, POST /pedido) que só delegam ao controller
- app/controllers/application.py -> classe Application (único controller)
- app/models/                    -> Doce, DoceRepositorio, Pedido (regras e validação)
- app/views/html/                -> base.html, index.html, _docinho.html (Jinja)
- app/static/                    -> css/style.css, js/app.js
- 
    python run.py
Acesse: http://localhost:5000

## Estrutura (BMVC)
- Model:      app/models/      -> Doce, DoceRepositorio, Pedido (regras e validação)
- View:       app/views/       -> templates Jinja + app/static (CSS, JS)
- Controller: app/controllers/ -> rotas: GET / e POST /pedido

