# 🎮 Minecraft Bedrock Backup Manager

**Gerenciador simples de backups de mundos Minecraft Bedrock no Windows 10/11.**

> ⚠️ **NÃO É UM PRODUTO OFICIAL DO MINECRAFT. NÃO APROVADO OU ASSOCIADO À MOJANG OU MICROSOFT.**

![Versão](https://img.shields.io/badge/versão-0.7.1b0-blue)
![Licença](https://img.shields.io/badge/licença-AGPL--3.0-green)
![Python](https://img.shields.io/badge/python-3.14%2B-blue)
![Testes](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/actions/workflows/tests.yml/badge.svg)

---

## 🚀 O que é?

Um **projeto pessoal hobby (MVP)** para resolver um problema real: backup simples de mundos Minecraft Bedrock no Windows.

Abra o app → clique em "Fazer Backup" → app copia a pasta do mundo com timestamp → pronto. Quer restaurar? Selecione um backup anterior. É isso.

**Status:** Funcional, testado (149+ testes), pronto para uso beta.

⚠️ **Importante:** Este é um **projeto pessoal hobby**. Não tem suporte profissional nem manutenção garantida por empresa. Use por sua conta e risco.

---

## 📖 Documentação

**Documentação completa em:** https://dandanleinad.github.io/minecraft-bedrock-backup-manager/

| Seção | Descrição |
|-------|-----------|
| [Guia do Usuário](https://dandanleinad.github.io/minecraft-bedrock-backup-manager/user-guide/) | Instalação, primeiro backup, restauração, localização, FAQ |
| [Primeiros Passos (Dev)](https://dandanleinad.github.io/minecraft-bedrock-backup-manager/getting-started/) | Setup, comandos, build, workflow Git |
| [Arquitetura](https://dandanleinad.github.io/minecraft-bedrock-backup-manager/architecture/) | Arquitetura hexagonal, ports & models, fluxo, DI |
| [Referência Técnica](https://dandanleinad.github.io/minecraft-bedrock-backup-manager/reference/) | Models, ports, services, configuração |
| [Desenvolvimento](https://dandanleinad.github.io/minecraft-bedrock-backup-manager/development/) | Contribuindo, DCO, licença, trunk-based, feature flags, testes |

---

## ⚡ Início Rápido

### Opção 1: Executável (quando disponível)
- Baixe o `.exe` em [Releases](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/releases)
- Dê dois cliques e execute

### Opção 2: Do Código Fonte (recomendado para testar)
```bash
git clone https://github.com/DandanLeinad/minecraft-bedrock-backup-manager.git
cd minecraft-bedrock-backup-manager

# Com uv (mais rápido)
uv sync
uv run python -m backup_manager_mvp.main

# Ou com pip + venv
python -m venv .venv
.venv\Scripts\activate
pip install -e .
python -m backup_manager_mvp.main
```

---

## 🎯 Como funciona

1. **Abra o app** → Detecta automaticamente seus mundos Bedrock
2. **Selecione um mundo** → Mostra backups existentes + metadados
3. **Faça backup** → Cópia completa com timestamp `YYYY-MM-DD_HH-MM-SS`
4. **Restaure** (opcional) → Selecione backup anterior com confirmação

**Backups salvos em:** `%UserProfile%\Documents\MinecraftBackups\`

---

## ✨ Funcionalidades

- ✅ Detecção automática de mundos (3 fontes: Normal, UWP Store, Compartilhado)
- ✅ Backup em um clique com timestamp preciso
- ✅ Restauração segura com confirmação (evita acidentes)
- ✅ Suporte a múltiplas contas Microsoft
- ✅ Interface desktop profissional (CustomTkinter)
- ✅ 149+ testes automatizados
- ✅ Validação robusta com Pydantic

---

## 📋 Requisitos

- **Windows 10/11** (64-bit)
- **Python 3.14+** (se compilar do fonte)
- **Minecraft Bedrock Edition** instalado

---

## 🏗️ Arquitetura

Arquitetura Hexagonal (Ports & Adapters) com separação clara:

```
src/backup_manager_mvp/
├── main.py                     # Entry point
├── application.py              # Composition Root + App Controller
├── config/feature_flags.py     # Feature flags
├── core/
│   ├── models/                 # Domain Models (Pydantic)
│   ├── ports/                  # Interfaces (ABC)
│   └── services/               # Lógica de negócio
├── infra/repository/           # Implementações dos Ports (FS)
└── ui/customtkinter/           # Implementação da UI
```

---

## 🔧 Desenvolvimento

### Setup
```bash
uv sync --all-groups
pre-commit install
uv run task test
```

### Executar
```bash
uv run task dev          # modo dev
uv run task dev-debug    # logs verbosos
```

### Qualidade
```bash
uv run task test         # pytest -vv
uv run task test-cov     # testes + coverage
uv run task lint         # ruff check
uv run task format       # ruff format
uv run task type-check   # pyright
```

### Build
```bash
python build.py          # release build
python build.py --debug  # com console
python build.py --clean  # limpa + build
```

### Versionamento (Commitizen)
```bash
uv run task bump-patch
uv run task bump-minor
uv run task bump-major
```

---

## 🤝 Contribuindo

**Workflow:** Trunk-Based Development com branches curtas (máx 3-5 dias)

1. Branch de `main`: `feature/*`, `fix/*`, `chore/*`, `docs/*`
2. Commits pequenos seguindo Conventional Commits
3. PR para `main` → CI roda (testes, lint, type-check)
4. Squash and merge após review
5. Delete branch

**Obrigatório:**
- `Signed-off-by` em TODOS os commits (`git commit -s`)
- Feature flags para features incompletas (`FF_*`)
- Docstrings/logs em inglês, docs em PT-BR
- Sem `print()` — use `logging`

Veja [Guia de Contribuição](https://dandanleinad.github.io/minecraft-bedrock-backup-manager/development/contributing/) para detalhes.

---

## 🚩 Feature Flags

Flags para features em desenvolvimento (desativadas por padrão, salvo indicado):

| Flag | Padrão | Status | Descrição |
|------|--------|--------|-----------|
| `FF_WORLD_ICON_PREVIEW` | `true` | ✅ Ativo | Preview de ícone do mundo na lista |
| `FF_RESTORE_PREVIEW` | `true` | ✅ Ativo | Preview antes de restaurar |
| `FF_MULTI_THREADING` | `false` | ⚡ Experimental | Cópia/deleção paralela |
| `FF_ADVANCED_LOGGING` | `false` | ⚡ Experimental | Logs verbosos de debug |

```bash
# Ativar features experimentais
FF_MULTI_THREADING=true FF_ADVANCED_LOGGING=true uv run task dev
```

---

## 📝 Versionamento

[Semantic Versioning](https://semver.org/) via Commitizen:

- `0.7.1b0` — Beta atual
- Bumps: `uv run task bump-patch|minor|major`

---

## ⚠️ Limitações (MVP - Hobby Project)

- Backups são cópias simples de arquivos (sem compressão/deduplicação)
- Manutenção em tempo pessoal (projeto hobby)

---

## 🐛 Encontrou um bug?

[Abra uma issue](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/issues) com:
- O que aconteceu
- Versão do Windows
- Passos para reproduzir
- Arquivo de log (se aplicável)

---

## 📜 Licença

**AGPL-3.0-or-later** — Open source desde o MVP.

**Minecraft™** é marca registrada da Mojang/Microsoft. Este projeto é **não-oficial** e **independente**.

---

## 🛠️ Tech Stack

- **CustomTkinter** — UI desktop moderna
- **Pydantic** — Validação e parsing de dados
- **Pytest** — Framework de testes
- **Ruff** — Linter/formatter
- **PyInstaller** — Build de executável
- **uv** — Gerenciador de pacotes ultra-rápido
- **Zensical** — Documentação (baseado em MkDocs)

---

## 🙏 Créditos

Construído sobre bibliotecas open-source fantásticas:

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (MIT)
- [Pydantic](https://github.com/pydantic/pydantic) (MIT)
- [PyInstaller](https://www.pyinstaller.org/) (GPL + exceção)
- [Pytest](https://pytest.org/) (MIT)
- [Ruff](https://github.com/astral-sh/ruff) (MIT)
- [uv](https://github.com/astral-sh/uv) (MIT)

---

## 📬 Contato

- **GitHub**: [@DandanLeinad](https://github.com/DandanLeinad)
- **Issues**: [Reportar bug](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/issues)
- **Discussions**: [Ideias e feedback](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/discussions)

---

## ⭐ Se foi útil, deixa uma star! ⭐
