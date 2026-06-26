---
icon: lucide/rocket
---

# Primeiros Passos — Desenvolvimento

Guia rápido para configurar o ambiente, rodar a aplicação, executar testes e fazer builds.

---

## 🎯 Visão Geral

Este guia cobre o **workflow de desenvolvimento** completo:

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Setup Inicial**

    Clone, instale dependências, configure hooks, valide ambiente.

    [:octicons-arrow-right-24: Setup](usage.md#setup-inicial)

-   :material-play-circle:{ .lg .middle } **Comandos Diários**

    Rodar app, testes, lint, format, type-check, build.

    [:octicons-arrow-right-24: Comandos](usage.md#comandos-diarios-via-taskipy)

-   :material-package:{ .lg .middle } **Build do Executável**

    Release, debug, clean, full rebuild com PyInstaller.

    [:octicons-arrow-right-24: Build](usage.md#build-do-executavel)

-   :material-tag:{ .lg .middle } **Versionamento & Release**

    Commitizen, Conventional Commits, bump version, changelog.

    [:octicons-arrow-right-24: Release](usage.md#versionamento-release)

-   :material-git:{ .lg .middle } **Workflow Git**

    Trunk-Based Development, branches curtas, PRs, CI/CD.

    [:octicons-arrow-right-24: Git Workflow](usage.md#workflow-git-trunk-based-prs)

-   :material-flag:{ .lg .middle } **Feature Flags**

    Desenvolver features incompletas sem quebrar produção.

    [:octicons-arrow-right-24: Feature Flags](usage.md#feature-flags-features-inacabadas)

</div>

---

## ⚡ Quick Start (TL;DR)

```bash title="Setup completo em 30 segundos"
# 1. Clone
git clone https://github.com/DandanLeinad/minecraft-bedrock-backup-manager.git
cd minecraft-bedrock-backup-manager

# 2. Instale uv
irm https://astral.sh/uv/install.ps1 | iex

# 3. Setup
uv sync --all-groups
uv run task pre-commit-install

# 4. Valide
uv run pytest tests/ -q

# 5. Rode!
uv run task dev
```

---

## 📋 Pré-requisitos

| Ferramenta | Versão | Instalação |
|------------|--------|------------|
| **Python** | 3.14+ | [python.org](https://python.org) ou `winget install Python.Python.3.14` |
| **uv** | 0.11+ | `irm https://astral.sh/uv/install.ps1 \| iex` |
| **Git** | 2.40+ | [git-scm.com](https://git-scm.com) |
| **Windows** | 10/11 | Só roda no Windows (Minecraft Bedrock paths) |

---

## 🔗 Próximos Passos

- [Guia completo de uso](./usage.md) — Todos os comandos e workflows
- [Arquitetura Overview](../architecture/overview.md) — Entenda a estrutura do código
- [Trunk-Based Development](../development/trunk-based-development.md) — Workflow Git detalhado
- [Feature Flags](../development/feature-flags.md) — Como usar flags para features WIP
