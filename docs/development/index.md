---
icon: lucide/git-branch
---

# Desenvolvimento

Guias de workflow, padrões e práticas de desenvolvimento do projeto.

---

## 🎯 Visão Geral

Este projeto segue **Trunk-Based Development** com branches curtas, feature flags, e CI/CD automatizado.

<div class="grid cards" markdown>

-   :material-git:{ .lg .middle } **Trunk-Based Development**

    Branches curtas (3-5 dias), PRs obrigatórias, merge squash, versionamento automático.

    [:octicons-arrow-right-24: Ver Guia](./trunk-based-development.md)

-   :material-flag:{ .lg .middle } **Feature Flags**

    Integre código incompleto sem quebrar produção. Ative via env var para testar.

    [:octicons-arrow-right-24: Ver Guia](./feature-flags.md)

-   :material-timer:{ .lg .middle } **Branches Curtas**

    Exemplos práticos: feature em 3 dias, bugfix em 1 dia, chore em 4 horas.

    [:octicons-arrow-right-24: Ver Guia](./short-branches.md)

-   :material-test-tube:{ .lg .middle } **Testing**

    Estrutura (unit/integration), anatomia de teste (AAA), TDD workflow, coverage.

    [:octicons-arrow-right-24: Ver Guia](./testing.md)

</div>

---

## ⚡ Quick Reference

### Comandos Essenciais

```bash title="Daily workflow"
# Rodar app (dev)
uv run task dev

# Testes
uv run task test          # pytest -vv
uv run task test-cov      # + coverage HTML

# Qualidade
uv run task lint          # ruff check
uv run task format        # ruff format
uv run task type-check    # pyright

# Tudo junto (pre-push)
uv run task lint && uv run task format && uv run task type-check && uv run task test
```

### Git Flow

```bash title="Nova feature"
git checkout main && git pull
git checkout -b feature/nome-curto

# Desenvolva com commits pequenos
git add . && git commit -m "feat: adicionar X"
git add . && git commit -m "test: cobrir X"

# Push + PR
git push origin feature/nome-curto
# Abrir PR no GitHub → main
```

### Feature Flags

```bash title="Testar feature WIP"
FF_AUTO_BACKUP=true uv run task dev
FF_RESTORE_PREVIEW=true uv run task dev
```

---

## 📋 Checklist de PR

- [ ] Branch name segue padrão (`feature/*`, `fix/*`, `chore/*`, `docs/*`)
- [ ] Commits seguem [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] Testes passam localmente (`uv run task test`)
- [ ] Code formatado (`uv run task format`)
- [ ] Lint limpo (`uv run task lint`)
- [ ] Type check passa (`uv run task type-check`)
- [ ] Feature flags usadas para features incompletas
- [ ] Sem `print()` — usar `logging`
- [ ] Máximo 400 linhas por PR
- [ ] Descrição clara do que foi mudado

---

## 🔗 Links Relacionados

- [Primeiros Passos](../getting-started/usage/) — Setup completo
- [Arquitetura](../architecture/overview.md) — Entenda o código antes de contribuir
- [ADR 0001](../decisions/0001-python-now-rust-tauri-future.md) — Contexto técnico
- [CONTRIBUTING.md](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/CONTRIBUTING.md) — Guia oficial de contribuição
