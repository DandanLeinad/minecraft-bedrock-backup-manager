---
icon: lucide/settings
---

# Configuração

Variáveis de ambiente, feature flags e settings do projeto.

---

## Variáveis de Ambiente

### Feature Flags

Ative features experimentais via environment variables:

```bash title="Ativar feature flags"
# Auto-backup em background
FF_AUTO_BACKUP=true uv run task dev

# Preview antes de restaurar
FF_RESTORE_PREVIEW=true uv run task dev

# Sincronização com cloud (WIP)
FF_CLOUD_SYNC=true uv run task dev

# Multi-threading para operações paralelas
FF_MULTI_THREADING=true uv run task dev

# Logs avançados para debug
FF_ADVANCED_LOGGING=true uv run task dev

# Múltiplas flags
FF_AUTO_BACKUP=true FF_RESTORE_PREVIEW=true FF_CLOUD_SYNC=true uv run task dev
```

| Flag | Status | Descrição |
|------|--------|-----------|
| `FF_AUTO_BACKUP` | 🧪 Em Desenvolvimento | Backup automático em background |
| `FF_CLOUD_SYNC` | 🧪 Em Desenvolvimento | Sincronização com provedores cloud |
| `FF_RESTORE_PREVIEW` | 🧪 Em Desenvolvimento | Preview do conteúdo antes de restaurar |
| `FF_MULTI_THREADING` | ⚡ Experimental | Operações paralelas de copy/delete |
| `FF_ADVANCED_LOGGING` | ⚡ Experimental | Logs detalhados para debugging |

### Como Funcionam

```python title="src/backup_manager_mvp/config/feature_flags.py"
import os
from dataclasses import dataclass

@dataclass
class FeatureFlags:
    ENABLE_AUTO_BACKUP: bool = _parse_bool(os.getenv("FF_AUTO_BACKUP", "false"))
    ENABLE_CLOUD_SYNC: bool = _parse_bool(os.getenv("FF_CLOUD_SYNC", "false"))
    ENABLE_RESTORE_PREVIEW: bool = _parse_bool(os.getenv("FF_RESTORE_PREVIEW", "false"))
    ENABLE_MULTI_THREADING: bool = _parse_bool(os.getenv("FF_MULTI_THREADING", "false"))
    ENABLE_ADVANCED_LOGGING: bool = _parse_bool(os.getenv("FF_ADVANCED_LOGGING", "false"))

def _parse_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes", "on")

FEATURE_FLAGS = FeatureFlags()
```

### Uso no Código

```python
from backup_manager_mvp.config import FEATURE_FLAGS

# Em qualquer service/UI
if FEATURE_FLAGS.ENABLE_AUTO_BACKUP:
    # Feature ativada
    start_auto_backup_scheduler()

if FEATURE_FLAGS.ENABLE_RESTORE_PREVIEW:
    # Mostrar botão de preview
    show_preview_button()
```

### Workflow com Feature Flags

```mermaid
graph LR
    DEV[Dev Branch] --> FLAG[Feature Flag = false]
    FLAG --> PR[Pull Request]
    PR --> CI[CI: Testes com flag=true]
    CI --> MERGE[Merge na main Merge para main<br/>(flag continua false)]
    MERGE --> RELEASE[Release: flag = true]
```

---

## Logging

```bash title="Níveis de log"
# Debug verbose
BACKUP_MANAGER_LOG_LEVEL=DEBUG uv run task dev

# Info (padrão)
BACKUP_MANAGER_LOG_LEVEL=INFO uv run task dev

# Warning apenas
BACKUP_MANAGER_LOG_LEVEL=WARNING uv run task dev
```

| Nível | Uso |
|-------|-----|
| `DEBUG` | Desenvolvimento, troubleshooting |
| `INFO` | Produção, operações normais |
| `WARNING` | Avisos, degradação |
| `ERROR` | Falhas, exceções |

---

## Caminhos Padrão (Hardcoded no MVP)

| Item | Caminho |
|------|---------|
| **Mundos (AppData)** | `%AppData%\Minecraft Bedrock\Users\{account_id}\games\com.mojang\minecraftWorlds\` |
| **Mundos (UWP Store)** | `%LocalAppData%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds\` |
| **Mundos (Shared)** | `%AppData%\Minecraft Bedrock\Users\Shared\games\com.mojang\minecraftWorlds\` |
| **Backups** | `%UserProfile%\Documents\MinecraftBackups\backups\{folder_name}\{timestamp}\` |

> ⚠️ **Nota**: No MVP os caminhos não são configuráveis. Futuro: arquivo de configuração (TOML/JSON).

---

## Build Configuration

### PyInstaller (build.py)

```bash
# Release (sem console)
uv run task build

# Debug (com console)
uv run task build-debug

# Limpar + rebuild
uv run task build-clean
uv run task build-full
```

### Especificações Principais

```python title="build.py - configuração chave"
# Entry point
"src/backup_manager_mvp/main.py"

# Ícone
"assets/icon.ico"

# Dados incluídos
datas = [
    ("src/backup_manager_mvp/ui/customtkinter/assets", "backup_manager_mvp/ui/customtkinter/assets"),
]

# Hidden imports (auto-detected + manual)
hiddenimports = [
    "customtkinter",
    "PIL",
    "pydantic",
    "pydantic_core",
]
```

---

## Versionamento (Commitizen)

```bash
# Ver versão atual
uv run task cz-version

# Bump patch (0.7.1 → 0.7.2)
uv run task bump-patch

# Bump minor (0.7.1 → 0.8.0)
uv run task bump-minor

# Bump major (0.7.1 → 1.0.0)
uv run task bump-major

# Dry-run
uv run task cz-bump-dry

# Changelog
uv run task cz-changelog
```

### Configuração (pyproject.toml)

```toml title="pyproject.toml - commitizen"
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.7.1b0"
tag_format = "v$version"
version_files = [
    "pyproject.toml:version = \"{version}\"",
    "src/backup_manager_mvp/version.json:\"current\": \"{version}\""
]
changelog_file = "CHANGELOG.md"
changelog_incremental = true
```

---

## Dependências Principais

### Runtime (pyproject.toml)

| Pacote | Versão | Uso |
|--------|--------|-----|
| `customtkinter` | ≥5.2.2 | UI Desktop |
| `pillow` | ≥12.2.0 | Imagens (world_icon) |
| `pydantic` | ≥2.13.4 | Models, validação |

### Development (pyproject.toml)

| Pacote | Versão | Uso |
|--------|--------|-----|
| `pytest` | ≥9.1.0 | Testes |
| `pytest-cov` | ≥7.1.0 | Coverage |
| `ruff` | ≥0.15.16 | Lint + Format |
| `pyright` | ≥1.1.410 | Type checking |
| `commitizen` | ≥4.16.3 | Versionamento |
| `pre-commit` | ≥4.6.0 | Git hooks |
| `pyinstaller` | ≥6.21.0 | Build .exe |
| `taskipy` | ≥1.14.1 | Task runner |
| `zensical` | ≥0.0.45 | Documentação |

---

## Referências

- [Código: feature_flags.py](../../src/backup_manager_mvp/config/feature_flags.py)
- [Guia: Feature Flags](../development/feature-flags.md)
- [Guia: Build](../getting-started/usage.md#build-do-executavel)
- [Guia: Versionamento](../getting-started/usage.md#versionamento-release)
