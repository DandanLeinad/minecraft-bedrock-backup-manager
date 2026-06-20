---
icon: lucide/database-backup
hide:
  - toc
  - navigation
---

# Minecraft Bedrock Backup Manager

> **Gerenciador de backups de mundos Minecraft Bedrock Edition para Windows 10/11.**
> Interface gráfica nativa, backups versionados, restauração com preview.

[![Download Latest Release](https://img.shields.io/github/v/release/DandanLeinad/minecraft-bedrock-backup-manager?include_prereleases&label=Download&color=4f46e5&style=for-the-badge)](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/releases/latest)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg?style=for-the-badge)](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/LICENSE)
[![Python 3.14+](https://img.shields.io/badge/Python-3.14%2B-4f46e5?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078d6?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com/windows)

---

## 🎯 Por que usar?

<div class="grid cards" markdown>

-   :material-gamepad-variant:{ .lg .middle } **Para Jogadores**

    * **Zero configuração** — Detecta mundos automaticamente
    * **Backup em 1 clique** — Versionado com timestamp
    * **Restauração segura** — Preview do conteúdo antes de confirmar
    * **Portátil** — `.exe` único (~5MB), sem instalação

-   :material-code-braces:{ .lg .middle } **Para Desenvolvedores**

    * **Arquitetura Hexagonal** — Ports & Adapters, testável
    * **TDD rigoroso** — 149 testes, 100% models coverage
    * **Feature Flags** — Integração contínua segura
    * **Open Source** — AGPL-3.0, contribuições bem-vindas

</div>

---

## 🚀 Início Rápido

=== "🎮 Usuário Final"

    1. [Baixe o `.exe` mais recente](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/releases/latest) :material-download:
    2. Execute — **sem instalação necessária** :material-play-circle:
    3. Selecione um mundo → **Fazer Backup** :material-content-save:
    4. Pronto! Backups em `Documentos\MinecraftBackups\backups\` :material-folder:

    [![Baixar Agora](https://img.shields.io/badge/Baixar-.exe-4f46e5?style=for-the-badge&logo=github)](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/releases/latest)

=== "🛠️ Desenvolvedor"

    ```bash title="Setup completo"
    # Clone
    git clone https://github.com/DandanLeinad/minecraft-bedrock-backup-manager.git
    cd minecraft-bedrock-backup-manager

    # Instale uv (Windows PowerShell)
    irm https://astral.sh/uv/install.ps1 | iex

    # Setup do projeto
    uv sync --all-groups
    uv run task pre-commit-install

    # Rode a aplicação
    uv run task dev
    ```

    [Guia de Desenvolvimento →](./getting-started/usage.md){ .md-button }

---

## 📚 Documentação

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Primeiros Passos (Dev)**

    Setup, comandos Taskipy, build, versionamento, workflow Git, feature flags.

    [:octicons-arrow-right-24: Ver Guia](./getting-started/usage.md)

-   :material-sitemap:{ .lg .middle } **Arquitetura**

    Ports & Adapters, Domain Models, Services, Dependency Injection, Patterns.

    [:octicons-arrow-right-24: Visão Geral](./architecture/overview.md)
    [:octicons-arrow-right-24: Fluxo de Requisição](./architecture/request-flow.md)
    [:octicons-arrow-right-24: Injeção de Dependência](./architecture/dependency-injection.md)

-   :material-book-open-variant:{ .lg .middle } **Guia do Usuário**

    Instalação, primeiro backup, restauração, localização, configurações, FAQ, troubleshooting.

    [:octicons-arrow-right-24: Começar](./user-guide/index.md)

-   :material-api:{ .lg .middle } **Referência Técnica**

    Models (Pydantic), Ports (ABCs), Services, Configuração, Feature Flags.

    [:octicons-arrow-right-24: API Reference](./reference/index.md)

-   :material-lightbulb-on:{ .lg .middle } **Decisões (ADRs)**

    Registro de decisões arquiteturais: Python agora, Rust/Tauri futuro.

    [:octicons-arrow-right-24: Ver ADRs](./decisions/index.md)

-   :material-git:{ .lg .middle } **Desenvolvimento**

    Trunk-Based Development, branches curtas, feature flags, testing, CI/CD.

    [:octicons-arrow-right-24: Workflow](./development/trunk-based-development.md)

</div>

---

## 🏗️ Arquitetura em Resumo

Visão arquitetural de alto nível — **Ports & Adapters (Hexagonal)** com **Application Controller** como Composition Root.

```mermaid
flowchart TB
    %% Entry Point
    subgraph ENTRY["Entry Point"]
        MAIN["main.py<br/>Composition Root"]
    end

    %% Application Controller
    subgraph CTRL["Application Controller"]
        APP["BackupManagerApp<br/>• DI Container<br/>• Callback Wiring<br/>• Thread Management"]
    end

    %% UI Layer (Adapter)
    subgraph UI["UI Layer (Adapter)"]
        CTK["CustomTkinterUIController"]
        SCR["Screens<br/>• WorldsList<br/>• WorldDetails<br/>• RestorePreview<br/>• RestoreConfirm"]
        HND["Handlers<br/>• Navigation<br/>• Backup<br/>• Restore<br/>• World"]
        MGR["Managers<br/>• Window<br/>• Toast<br/>• Loading<br/>• Progress"]
    end

    %% Application Services
    subgraph SVCS["Application Services"]
        WS["WorldService"]
        BS["BackupService"]
        PS["ProgressService"]
    end

    %% Ports (Interfaces)
    subgraph PORTS["Ports (Interfaces)"]
        WRP["WorldRepositoryPort"]
        BRP["BackupRepositoryPort"]
    end

    %% Domain Models (transversal)
    subgraph DOM["Domain Models"]
        WM["WorldModel"]
        BM["BackupModel"]
        PM["ProgressModel"]
    end

    %% Infrastructure
    subgraph INFRA["Infrastructure"]
        FWR["FileSystemWorldRepository"]
        FBR["FileSystemBackupRepository"]
    end

    %% Dependencies (clean layer boundaries)
    MAIN --> APP
    APP --> UI
    APP --> SVCS
    UI --> APP
    SVCS --> PORTS
    SVCS --> DOM
    PORTS -.->|implements| INFRA
    INFRA -.-> DOM

    %% Styling
    classDef entry fill:#1e293b,stroke:#64748b,color:#fff;
    classDef ctrl fill:#312e81,stroke:#6366f1,color:#fff;
    classDef ui fill:#1e40af,stroke:#3b82f6,color:#fff;
    classDef svc fill:#065f46,stroke:#10b981,color:#fff;
    classDef port fill:#7c2d12,stroke:#f97316,color:#fff;
    classDef dom fill:#92400e,stroke:#f59e0b,color:#fff;
    classDef infra fill:#374151,stroke:#9ca3af,color:#fff;

    class MAIN entry;
    class APP ctrl;
    class CTK,SCR,HND,MGR ui;
    class WS,BS,PS svc;
    class WRP,BRP port;
    class WM,BM,PM dom;
    class FWR,FBR infra;
```

### Legenda das Camadas

| Camada | Responsabilidade | Código |
|--------|------------------|--------|
| **Entry Point** | Configura logging, instancia App | `main.py:83` |
| **App Controller** | DI Container, Callback Wiring, Thread Mgmt | `application.py:36` |
| **UI Layer** | CustomTkinter Adapter, Screens, Handlers, Managers | `ui/customtkinter/` |
| **Services** | Regras de negócio, orquestração | `core/services/` |
| **Ports** | Interfaces (ABC) | `core/ports/` |
| **Domain Models** | Entities/DTOs (transversais) | `core/models/` |
| **Infrastructure** | Implementações FS dos Ports | `infra/repository/` |

> **Nota:** Domain Models são **transversais** — atravessam todas as camadas como entrada/saída de dados. Por isso não estão no meio da cadeia de dependência.

---

## 🛠️ Stack Tecnológico

| Camada | Tecnologia | Versão |
|--------|------------|--------|
| **Linguagem** | Python | 3.14+ |
| **UI** | CustomTkinter | 5.2+ |
| **Validação** | Pydantic | 2.13+ |
| **Testes** | pytest / pytest-cov | 9+ |
| **Lint/Format** | Ruff | 0.15+ |
| **Types** | Pyright | 1.1+ |
| **Build** | PyInstaller | 6.21+ |
| **Versionamento** | Commitizen | 4.16+ |
| **Docs** | Zensical | 0.0.45+ |
| **Package Manager** | uv | 0.11+ |

---

## 🔗 Links Úteis

| Link | Descrição |
|------|-----------|
| [📦 Releases](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/releases) | Downloads `.exe` assinados |
| [🐛 Issues](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/issues) | Bug reports, feature requests |
| [💬 Discussions](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/discussions) | Perguntas, ideias, show & tell |
| [📝 Changelog](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/CHANGELOG.md) | Histórico de versões |
| [🤝 Contributing](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/CONTRIBUTING.md) | Como contribuir |

---

## ⚡ Feature Flags (Experimental)

Ative funcionalidades em desenvolvimento:

```bash title="Ativar feature flags"
# Auto-backup em background
FF_AUTO_BACKUP=true uv run task dev

# Preview antes de restaurar
FF_RESTORE_PREVIEW=true uv run task dev

# Múltiplas flags
FF_AUTO_BACKUP=true FF_CLOUD_SYNC=true FF_RESTORE_PREVIEW=true uv run task dev
```

!!! tip "Dica"
    Feature flags permitem integrar código incompleto na `main` sem quebrar produção.
    Veja [Feature Flags Guide](./development/feature-flags.md) para detalhes.

---

## 📄 Licença

**AGPL-3.0-or-later** — Código aberto, livre para usar, modificar e distribuir.
Consulte [LICENSE](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/LICENSE) para detalhes.

---

*Feito com :heart: por [DandanLeinad](https://github.com/DandanLeinad) · Powered by [Zensical](https://zensical.org) · [Editar esta página](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/edit/main/docs/index.md)*
