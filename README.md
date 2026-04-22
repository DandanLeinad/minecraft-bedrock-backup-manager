# 🎮 Minecraft Bedrock Backup Manager

**Um gerenciador de backups simples para mundos Minecraft Bedrock no Windows 10/11.**

> ⚠️ **NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.**

![Version](https://img.shields.io/badge/version-0.1.0--beta-blue)
![License](https://img.shields.io/badge/license-AGPL--3.0-green)
![Python](https://img.shields.io/badge/python-3.14%2B-blue)
![Tests](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/actions/workflows/tests.yml/badge.svg)

---

## 🚀 O que é?

Um **MVP (Minimum Viable Product) - Hobby Project** que criei para resolver um problema real: backup simples de mundos de Minecraft Bedrock no Windows, sem complicações.

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

# Instalar pre-commit hooks
pre-commit install

# Validar setup
uv run task test
```

### Executar

```bash
# Modo desenvolvimento
uv run task dev

# Modo debug (verbose logging)
uv run task dev-debug
```

### Testes & Qualidade

```bash
# Testes
uv run task test

# Testes com coverage
uv run task test-cov

# Lint (Ruff)
uv run task lint

# Format (Ruff)
uv run task format

# Type check (Pyright)
uv run task type-check

# Todos os hooks pre-commit
pre-commit run --all-files
```

### Build

```bash
# Build com PyInstaller
python build.py

# Build com debug console
python build.py --debug

# Clean + Build
python build.py --clean
```

### Versionamento

```bash
# Ver o que vai mudar (sem executar)
uv run task version-show

# Bump de patch (0.1.0-beta → 0.1.1-beta)
uv run task bump-patch

# Bump de minor (0.1.0-beta → 0.2.0-beta)
uv run task bump-minor

# Bump de major (0.1.0-beta → 1.0.0-beta)
uv run task bump-major

# Remover pre-release (0.1.0-beta → 0.1.0)
uv run task bump-beta

# Ver versão atual
uv run task version
```

---

## 🤝 Contribuindo

### Workflow - Trunk-Based Development

Este projeto segue **Trunk-Based Development** com branches curtas (máx 3-5 dias):

1. **Criar branch** - `feature/nome`, `fix/nome`, `chore/nome`
2. **Commits pequenos** - Cada commit compila/testa
3. **PR em main** - Testes automáticos rodam
4. **Merge rápido** - Após review
5. **Delete branch** - Cleanup

**Workflow Completo:**

```bash
# 1. Atualizar main
git checkout main
git pull origin main

# 2. Criar feature
git checkout -b feature/nome-descritivo

# 3. Desenvolver (commits pequenos)
git add .
git commit -m "feat: descrição"

# 4. Push
git push origin feature/nome-descritivo

# 5. Abrir PR no GitHub
# → Testes rodam automaticamente
# → Code review
# → Merge quando aprovado

# 6. Cleanup
git branch -d feature/nome-descritivo
git push origin --delete feature/nome-descritivo
```

**Commits:** Seguem [Conventional Commits](https://www.conventionalcommits.org/)

```
feat:  nova funcionalidade
fix:   correção de bug
docs:  documentação
style: formatação
test:  testes
chore: dependências, build
```

### Feature Flags

Para features inacabadas, use flags:

```python
from backup_manager_mvp.config import FEATURE_FLAGS

if FEATURE_FLAGS.ENABLE_AUTO_BACKUP:
    # Feature em desenvolvimento
    pass
```

Ativar em desenvolvimento:

```bash
FF_AUTO_BACKUP=true uv run python -m backup_manager_mvp.main
```

Veja [FEATURE_FLAGS.md](docs/FEATURE_FLAGS.md) para guia completo.

### Documentação

- [Trunk-Based Development Guide](docs/TRUNK_BASED_DEVELOPMENT.md)
- [Feature Flags Guide](docs/FEATURE_FLAGS.md)
- [Short Branches Best Practices](docs/SHORT_BRANCHES.md)
- [TESTING.md](docs/TESTING.md)
- [DEVELOPMENT.md](docs/DEVELOPMENT.md)

### Issues e Feedback

✅ **Issues** - Bugs, sugestões, discussões
✅ **Discussions** - Ideias e feedback

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
- ⚠️ Manutenção conforme tempo (hobby project)

### Features Planejadas (Em Desenvolvimento)

Essas features estão em desenvolvimento usando **Feature Flags** (desativadas por padrão):

- 🚧 Auto-backup em background (`FF_AUTO_BACKUP`)
- 🚧 Sincronização com cloud (`FF_CLOUD_SYNC`)
- 🚧 Preview antes de restaurar (`FF_RESTORE_PREVIEW`)
- 🚧 Operações paralelas (`FF_MULTI_THREADING`)
- 🚧 Logs avançados para debug (`FF_ADVANCED_LOGGING`)

Ative no desenvolvimento:

```bash
FF_AUTO_BACKUP=true uv run python -m backup_manager_mvp.main
```

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
