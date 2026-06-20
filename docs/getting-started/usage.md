# Uso — Desenvolvimento

Guia rápido para rodar, testar e construir o projeto localmente.

---

## Setup Inicial

```bash
# 1. Clone
git clone https://github.com/DandanLeinad/minecraft-bedrock-backup-manager.git
cd minecraft-bedrock-backup-manager

# 2. Instale uv (Windows PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# 3. Instale dependências (inclui dev)
uv sync --all-groups

# 4. Instale pre-commit hooks
uv run task pre-commit-install

# 5. Valide ambiente
uv run pytest tests/ -q
```

---

## Comandos Diários (via Taskipy)

```bash
# Rodar aplicação (dev mode)
uv run task dev

# Rodar com logs verbosos
uv run task dev-debug

# Testes
uv run task test              # pytest -vv
uv run task test-cov          # pytest + coverage HTML

# Qualidade de código
uv run task lint              # ruff check
uv run task format            # ruff format
uv run task type-check        # pyright

# Tudo junto (pre-push)
uv run task lint && uv run task format && uv run task type-check && uv run task test
```

---

## Build do Executável

```bash
# Release (sem console, otimizado)
uv run task build

# Debug (com console para ver logs)
uv run task build-debug

# Limpar + rebuild
uv run task build-clean
uv run task build-full        # clean + build

# Output: dist/MinecraftBedrockBackupManager.exe (~4.9MB)
```

---

## Versionamento & Release

```bash
# Ver versão atual
uv run task cz-version

# Bump patch (0.7.1 → 0.7.2)
uv run task bump-patch

# Bump minor (0.7.1 → 0.8.0)
uv run task bump-minor

# Bump major (0.7.1 → 1.0.0)
uv run task bump-major

# Dry-run (preview)
uv run task cz-bump-dry

# Changelog automático
uv run task cz-changelog
```

> Usa **Commitizen** com **Conventional Commits**. Commits devem seguir: `feat(scope): msg`, `fix: msg`, `docs: msg`, etc.

---

## Workflow Git (Trunk-Based + PRs)

```bash
# 1. Partir de main (protegida)
git checkout main
git pull origin main

# 2. Criar branch curta (max 3-5 dias)
git checkout -b feature/nome-curto
# ou fix/, chore/, docs/

# 3. Desenvolver com commits pequenos (Conventional Commits)
git add .
git commit -m "feat: adicionar validação X"

git add .
git commit -m "test: cobrir validação X"

# 4. Push e PR
git push origin feature/nome-curto
# Abrir PR no GitHub → main

# 5. CI roda: pytest + ruff + pyright + commitlint
# 6. Após aprovação: Squash and Merge

# 7. Limpar branch
git checkout main
git pull origin main
git branch -d feature/nome-curto
git push origin --delete feature/nome-curto
```

---

## Feature Flags (Features Inacabadas)

```bash
# Ativar flag para testar feature em desenvolvimento
FF_AUTO_BACKUP=true uv run task dev
FF_RESTORE_PREVIEW=true uv run task dev

# Múltiplas
FF_AUTO_BACKUP=true FF_CLOUD_SYNC=true uv run task dev
```

Flags disponíveis em `src/backup_manager_mvp/config/feature_flags.py`.

---

## Estrutura de Testes

```
tests/
├── unit/                    # Testes unitários (mocks, rápido)
│   ├── models/              # WorldModel, BackupModel, ProgressModel
│   ├── services/            # WorldService, BackupService (mock repo)
│   └── ui/                  # Handlers, components
├── integration/             # Testes com FS real (temp dirs)
│   ├── world/
│   └── backup/
└── conftest.py              # Fixtures compartilhadas
```

```bash
# Rodar testes específicos
uv run pytest tests/unit/models/ -v
uv run pytest tests/unit/services/test_backup_service.py -v
uv run pytest tests/integration/ -v

# Cobertura
uv run task test-cov
# Abre htmlcov/index.html
```

---

## Estrutura do Projeto

```
src/backup_manager_mvp/
├── main.py                          # Entry point
├── application.py                   # App setup (DI container)
├── version.json                     # Versão (atualizada pelo Commitizen)
├── config/
│   ├── __init__.py
│   └── feature_flags.py             # Feature flags (env vars)
├── core/
│   ├── models/                      # Pydantic models (Domain)
│   │   ├── world_model.py
│   │   ├── backup_model.py
│   │   └── progress_model.py
│   ├── ports/                       # Interfaces (ABC)
│   │   ├── world_repository.py
│   │   └── backup_repository.py
│   └── services/                    # Business logic
│       ├── world_service.py
│       ├── backup_service.py
│       └── progress_service.py
├── infra/
│   └── repository/                  # Implementações dos Ports
│       ├── filesystem_world_repository.py
│       └── filesystem_backup_repository.py
└── ui/
    └── customtkinter/               # UI CustomTkinter
        ├── customtkinter_ui.py      # Main window
        ├── screens/                 # Telas (WorldsList, Details, Restore)
        ├── handlers/                # Lógica de UI separada
        ├── components/              # Widgets reutilizáveis
        ├── core/                    # Window, theme, loading
        └── utils/                   # Helpers UI
```

---

## Variáveis de Ambiente Úteis

```bash
# Logs detalhados
BACKUP_MANAGER_LOG_LEVEL=DEBUG uv run task dev

# Feature flags
FF_AUTO_BACKUP=true
FF_CLOUD_SYNC=true
FF_RESTORE_PREVIEW=true
FF_MULTI_THREADING=true
FF_ADVANCED_LOGGING=true
```

---

## Troubleshooting Comum

| Problema | Solução |
|----------|---------|
| `uv: command not found` | Reinicie terminal após instalar uv |
| `pytest: import error` | `uv sync --all-groups` |
| `ruff: not found` | `uv sync --all-groups` |
| `pyright: not found` | `uv sync --all-groups` |
| Build falha no PyInstaller | `uv run task build-clean` e tente novamente |
| Testes falham com FS | Verifique permissões de temp dir |

---

## Próximos Passos

- [Arquitetura Overview](../architecture/overview.md)
- [Ports & Models](../architecture/ports-and-models.md)
- [Trunk-Based Development](../development/trunk-based-development.md)
- [Feature Flags](../development/feature-flags.md)
- [Testing](../development/testing.md)
