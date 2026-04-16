# 🎮 Minecraft Bedrock Backup Manager

**Um gerenciador de backups simples para mundos Minecraft Bedrock no Windows 10/11.**

> ⚠️ **NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.**

![Version](https://img.shields.io/badge/version-0.1.0--beta-blue)
![License](https://img.shields.io/badge/license-AGPL--3.0-green)
![Python](https://img.shields.io/badge/python-3.14%2B-blue)

---

## 🚀 O que é?

Um **MVP (Minimum Viable Product) - Hobby Project** que criei para resolver um problema real: backup automático de mundos de Minecraft Bedrock no Windows, sem complicações.

Basicamente: você clica em "Criar Backup" → o app copia a pasta do mundo inteira com timestamp → pronto. Se quer restaurar, seleciona um backup anterior. Simples assim.

**Status:** Funcional, testado (128 testes), pronto para uso beta.

⚠️ **Importante:** Este é um **hobby project pessoal**. Não é suportado profissionalmente nem mantido por empresa. Use por sua conta e risco. Se for útil pra você, ótimo! 😄

---

## ⚡ Quick Start

### Opção 1: Executável (quando disponível)

- Download do `.exe` em [Releases](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/releases)
- Duplo clique e pronto

### Opção 2: Com Python (recomendado para testar)

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

1. **Abre o app** → Lista seus mundos Bedrock automaticamente
2. **Seleciona um mundo** → Mostra backups existentes + metadados
3. **Cria backup** → Cópia completa do mundo com timestamp `YYYY-MM-DD_HH-MM-SS`
4. **Restaura** (opcional) → Seleciona backup anterior com confirmação

**Backups salvos em:** `%UserProfile%\Documents\MinecraftBackups\`

---

## ✨ Funcionalidades

- ✅ Detecção automática de mundos (3 fontes: Normal, UWP Store, Shared)
- ✅ Backup de um clique com timestamp preciso
- ✅ Restauração com confirmação (evita acidentes)
- ✅ Suporte multi-conta Microsoft
- ✅ Interface desktop profissional (CustomTkinter)
- ✅ 128 testes automatizados
- ✅ Validação robusta com Pydantic

---

## 📋 Pré-requisitos

- **Windows 10/11**
- **Python 3.14+** (se compilar local)
- **Minecraft Bedrock Edition** instalado

---

## 🏗️ Estrutura

``` text
src/backup_manager_mvp/
├── main.py                  # Entry point
├── application.py           # Orquestrador
├── models/
│   ├── world_model.py       # Modelo do mundo
│   └── backup_model.py      # Modelo de backup
├── services/
│   ├── world_service.py     # Detecção de mundos
│   └── backup_service.py    # Lógica de backup
└── ui/
    ├── customtkinter/       # Interface CustomTkinter
    │   ├── components/      # Componentes reutilizáveis
    │   ├── screens/         # Telas da aplicação
    │   ├── handlers/        # Event handlers
    │   └── customtkinter_ui.py
    └── base.py              # Abstração de UI
```

---

## 🔧 Desenvolvimento

### Setup

```bash
# Instalar dependências (incluindo dev)
uv sync --all-groups

# Validar setup
uv run pytest tests/ -q
```

### Executar

```bash
# Modo desenvolvimento
uv run task dev

# Modo debug (verbose logging)
uv run task dev-debug

# Testes
uv run pytest tests/ -vv

# Testes com coverage
uv run task test-cov

# Lint
uv run task lint

# Format
uv run task format

# Type check
uv run task type-check
```

### Build

```bash
# Build com PyInstaller
uv run task build-pyinstaller

# Build com limpeza
uv run task build-pyinstaller-clean
```

---

## 🤝 Contribuindo

**Hobby Project Policy:** Este é um projeto pessoal mantido por uma pessoa. **Por enquanto, não estou aceitando Pull Requests.**

### Como Participar?

✅ **Issues** - Bem-vindas! (reporte bugs, sugestões)
✅ **Discussions** - Ideias, feedback e perguntas
❌ **PRs** - Não aceitando por enquanto

### Por Que Não PRs Agora?

- É um hobby project (tempo limitado)
- Mantém o código mais focado e consistente
- Permite que eu trabalhe no ritmo próprio
- Se o projeto crescer, revisarei essa política

### Se o Projeto Crescer

Quando/se o projeto ganhar tração, abro para PRs com:

- Workflow de branches (`develop` + `feature/*`)
- Conventional Commits (`feat:`, `fix:`, etc.)

**Por enquanto: issues e feedback são ouro! 🙏**

---

## 📝 Versionamento

Este projeto segue [Semantic Versioning](https://semver.org/):

``` text
MAJOR.MINOR.PATCH[-PRERELEASE]
0.1.0-beta
```

Versões:

- **0.1.0-beta** — MVP inicial (current)
- **0.1.0-rc.1** — Release candidate
- **0.1.0** — Versão estável
- **0.2.0+** — Features adicionais

Veja [CHANGELOG.md](CHANGELOG.md) para histórico completo.

---

## 📝 Limitações (MVP - Hobby Project)

- ⚠️ Backups são **cópias simples** de arquivo (copy-pasta)
- ⚠️ Sem compressão ou deduplicação
- ⚠️ Sem agendamento automático
- ⚠️ Sem sincronização com cloud
- ⚠️ Manutenção conforme tempo (hobby project)

Essas features podem chegar em versões futuras se houver feedback/interesse e eu tiver tempo.

---

## 🐛 Encontrou um bug?

[Abra uma issue](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/issues) com:

- O que aconteceu (descrição clara)
- Windows version
- Passos para reproduzir
- Log file (se aplicável)

Resolvo conforme tempo permite. Sein hobby project, resposta pode demorar. 😊

---

## 📜 Licença

**AGPL-3.0-or-later** — Código aberto desde o MVP.

**Minecraft™** é marca registrada da Mojang/Microsoft. Este projeto é **não-oficial** e **independente**.

---

## 🛠️ Tech Stack

- **CustomTkinter** - UI desktop moderna
- **Pydantic** - Validação e parsing de dados
- **Pytest** - Framework de testes
- **Ruff** - Lint/formatter
- **PyInstaller** - Build para executável

---

## � Dependências e Créditos

Este projeto é construído sobre bibliotecas open-source fantásticas:

### Produção

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** — MIT License © [Tom Schimansky](https://github.com/TomSchimansky)
  - UI desktop moderna e totalmente customizável baseada em Tkinter
  - Suporte a dark mode, temas customizados e scaling automático

- **[Pydantic](https://github.com/pydantic/pydantic)** — MIT License © Pydantic Contributors
  - Validação de dados com type hints
  - Parsing robusto de modelos

### Desenvolvimento

- **[PyInstaller](https://www.pyinstaller.org/)** — GPL + PyInstaller Exceptions License
  - Build de executáveis standalone para Windows/macOS/Linux

- **[Pytest](https://pytest.org/)** — MIT License
  - Framework completo de testes

- **[Ruff](https://github.com/astral-sh/ruff)** — MIT License © Charlie Marsh
  - Linter e formatter ultra-rápido

- **[uv](https://github.com/astral-sh/uv)** — MIT License © Astral
  - Package manager ultra-rápido para Python

**Obrigado a todos os mantenedores e contribuidores dessas projects! 🙏**

---

## �📬 Contato

- **GitHub**: [@DandanLeinad](https://github.com/DandanLeinad)
- **Issues**: [Report bug](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/issues)
- **Discussions**: [Ideias e feedback](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/discussions)

---

## ⭐ Se foi útil pra você, deixa uma star! ⭐
