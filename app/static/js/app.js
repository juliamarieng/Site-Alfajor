(function () {
  "use strict";

  var selecionados = {}; // id -> { nome, preco, qtd }

  function moeda(v) {
    return v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  }
  function esc(t) {
    var d = document.createElement("div");
    d.textContent = t;
    return d.innerHTML;
  }
  function total() {
    return Object.keys(selecionados).reduce(function (s, id) {
      return s + selecionados[id].preco * selecionados[id].qtd;
    }, 0);
  }

  // ---------- Filtro da vitrine ----------
  document.querySelectorAll(".filtro").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var cat = btn.getAttribute("data-cat");
      document.querySelectorAll(".filtro").forEach(function (b) {
        b.classList.remove("ativo");
        b.setAttribute("aria-pressed", "false");
      });
      btn.classList.add("ativo");
      btn.setAttribute("aria-pressed", "true");
      document.querySelectorAll("#grade .card").forEach(function (c) {
        c.hidden = !(cat === "todos" || c.getAttribute("data-cat") === cat);
      });
    });
  });

  // ---------- Adicionar doce ----------
  document.getElementById("grade").addEventListener("click", function (e) {
    var b = e.target.closest("[data-add]");
    if (!b) return;
    var id = b.getAttribute("data-add");
    if (!selecionados[id]) {
      selecionados[id] = {
        nome: b.getAttribute("data-nome"),
        preco: parseFloat(b.getAttribute("data-preco")),
        qtd: 0
      };
    }
    selecionados[id].qtd++;
    renderEscolhidos();
    b.textContent = "Adicionado";
    setTimeout(function () { b.textContent = "Adicionar"; }, 900);
  });

  // ---------- Lista de escolhidos ----------
  function renderEscolhidos() {
    var ids = Object.keys(selecionados);
    var vazio = document.getElementById("vazio");
    vazio.hidden = ids.length > 0;
    document.getElementById("escolhidos").innerHTML = ids.map(function (id) {
      var d = selecionados[id];
      return '<div class="linha">' +
        '<span class="linha-nome">' + esc(d.nome) + '</span>' +
        '<span class="qtd">' +
          '<button type="button" data-menos="' + id + '" aria-label="Diminuir ' + esc(d.nome) + '">−</button>' +
          '<output aria-live="polite">' + d.qtd + '</output>' +
          '<button type="button" data-mais="' + id + '" aria-label="Aumentar ' + esc(d.nome) + '">+</button>' +
        '</span>' +
        '<span class="linha-preco">' + moeda(d.preco * d.qtd) + '</span>' +
      '</div>';
    }).join("") + (ids.length ? '<div class="total"><span>Total estimado</span><strong>' + moeda(total()) + '</strong></div>' : "");
  }

  document.getElementById("escolhidos").addEventListener("click", function (e) {
    var mais = e.target.getAttribute("data-mais");
    var menos = e.target.getAttribute("data-menos");
    if (mais) selecionados[mais].qtd++;
    if (menos) {
      selecionados[menos].qtd--;
      if (selecionados[menos].qtd <= 0) delete selecionados[menos];
    }
    if (mais || menos) renderEscolhidos();
  });

  // ---------- Enviar pedido (o Controller monta o link do WhatsApp) ----------
  document.getElementById("form").addEventListener("submit", function (e) {
    e.preventDefault();
    var erro = document.getElementById("erro");
    erro.textContent = "";

    var itens = {};
    Object.keys(selecionados).forEach(function (id) { itens[id] = selecionados[id].qtd; });

    var corpo = {
      nome: document.getElementById("nome").value,
      data: document.getElementById("data").value,
      mensagem: document.getElementById("mensagem").value,
      itens: itens
    };

    // Abre a aba antes do fetch para o navegador não bloquear o pop-up
    var aba = window.open("", "_blank");
    if (aba) aba.opener = null;

    fetch("/pedido", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(corpo)
    })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (!res.ok) {
          if (aba) aba.close();
          erro.textContent = res.j.erros.join(" ");
          return;
        }
        if (aba) { aba.location = res.j.url; } else { window.location = res.j.url; }
      })
      .catch(function () {
        if (aba) aba.close();
        erro.textContent = "Não foi possível enviar agora. Tente de novo em instantes.";
      });
  });

  // Não permite escolher data passada
  var hoje = new Date();
  hoje.setMinutes(hoje.getMinutes() - hoje.getTimezoneOffset());
  document.getElementById("data").min = hoje.toISOString().slice(0, 10);
})();
