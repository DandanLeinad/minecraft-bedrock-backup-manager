---
icon: lucide/settings
---

# Configuração

Variáveis de ambiente, feature flags e settings do projeto.

---

## Variáveis de Ambiente

### Feature Flags

Ative/desative features via environment variables:

```bash title="Ativar feature flags"
# Preview de ícone do mundo (padrão: true)
FF_WORLD_ICON_PREVIEW=false uv run task dev

# Preview antes de restaurar (padrão: true)
FF_RESTORE_PREVIEW=false uv run task dev

# Multi-threading para operações paralelas
FF_MULTI_THREADING=true uv run task dev

# Logs avançados para debug
FF_ADVANCED_LOGGING=true uv run task dev

# Múltiplas flags
FF_MULTI_THREADING=true FF_ADVANCED_LOGGING=true uv run task dev
```

| Flag | Padrão | Status | Descrição |
|------|--------|--------|-----------|
| `FF_WORLD_ICON_PREVIEW` | `true` | ✅ Ativo | Preview de ícone do mundo na lista |
| `FF_RESTORE_PREVIEW` | `true` | ✅ Ativo | Preview do conteúdo antes de restaurar |
| `FF_MULTI_THREADING` | `false` | ⚡ Experimental | Operações paralelas de copy/delete |
| `FF_ADVANCED_LOGGING` | `false` | ⚡ Experimental | Logs detalhados para debugging |

### Como Funcionam

```python title="src/backup_manager_mvp/config/feature_flags.py"
import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)

def _parse_bool(value: str) -> bool:
    """Parse string para booleano."""
    return value.lower() in ("true", "1", "yes", "on")

@dataclass(frozen=True)
class FeatureFlags:
    """Feature flags da aplicação (imutável)."""

    # Features ativas por padrão
    ENABLE_WORLD_ICON_PREVIEW: bool = _parse_bool(os.getenv("FF_WORLD_ICON_PREVIEW", "true"))
    ENABLE_RESTORE_PREVIEW: bool = _parse_bool(os.getenv("FF_RESTORE_PREVIEW", "true"))

    # Features experimentais
    ENABLE_MULTI_THREADING: bool = _parse_bool(os.getenv("FF_MULTI_THREADING", "false"))
    ENABLE_ADVANCED_LOGGING: bool = _parse_bool(os.getenv("FF_ADVANCED_LOGGING", "false"))

    def __post_init__(self):
        """Log flags ativadas no init."""
        enabled_flags = [name for name in self.__dataclass_fields__ if getattr(self, name) is True]
        if enabled_flags:
            logger.info(f"Feature flags ativadas: {', '.join(enabled_flags)}")

# Instância global
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
    CI --> MERGE["Merge na main Merge para main<br/>(flag continua false)"]
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

- [Código: feature_flags.py](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/config/feature_flags.py)
- [Guia: Feature Flags](../development/feature-flags.md)
- [Guia: Build](../getting-started/usage.md#build-do-executavel)
- [Guia: Versionamento](../getting-started/usage.md#versionamento-release)
