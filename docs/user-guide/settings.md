---
icon: lucide/settings
---

# Configurações

Opções de configuração, feature flags e personalização.

---

## ⚙️ Configurações Atuais (MVP)

No MVP, a maioria das configurações é feita via **variáveis de ambiente** (feature flags). Não há arquivo de configuração ou UI de settings ainda.

---

## 🚩 Feature Flags (Variáveis de Ambiente)

Ative/desative features antes de executar:

```bash title="PowerShell"
# Desativar preview de ícone (padrão: true)
$env:FF_WORLD_ICON_PREVIEW = "false"
uv run task dev

# Desativar preview de restauração (padrão: true)
$env:FF_RESTORE_PREVIEW = "false"
uv run task dev

# Ativar multi-threading experimental
$env:FF_MULTI_THREADING = "true"
uv run task dev

# Ativar logs avançados
$env:FF_ADVANCED_LOGGING = "true"
uv run task dev

# Múltiplas flags
$env:FF_MULTI_THREADING = "true"
$env:FF_ADVANCED_LOGGING = "true"
uv run task dev
```

```cmd title="CMD"
set FF_WORLD_ICON_PREVIEW=false
set FF_RESTORE_PREVIEW=false
set FF_MULTI_THREADING=true
MinecraftBedrockBackupManager.exe
```

| Flag | Padrão | Status | Descrição |
|------|--------|--------|-----------|
| `FF_WORLD_ICON_PREVIEW` | `true` | ✅ Ativo | Preview de ícone do mundo na lista |
| `FF_RESTORE_PREVIEW` | `true` | ✅ Ativo | Preview do conteúdo antes de restaurar |
| `FF_MULTI_THREADING` | `false` | ⚡ Experimental | Operações paralelas de copy/delete |
| `FF_ADVANCED_LOGGING` | `false` | ⚡ Experimental | Logs detalhados para debugging |

---

## 📝 Logging

```bash title="Níveis"
# Debug (verbose)
$env:BACKUP_MANAGER_LOG_LEVEL = "DEBUG"
uv run task dev

# Info (padrão)
$env:BACKUP_MANAGER_LOG_LEVEL = "INFO"

# Apenas warnings/errors
$env:BACKUP_MANAGER_LOG_LEVEL = "WARNING"
```

---

## 🎨 Tema da UI

O app detecta automaticamente o tema do Windows:

-   **Claro** → UI clara
-   **Escuro** → UI escura

> Não há toggle manual no MVP. Futuro: configuração persistente.

---

## 🔮 Futuro: Arquivo de Configuração

Planejado para versões futuras (`config.toml` ou `config.json`):

```toml title="config.toml (futuro)"
[backup]
auto_enabled = false
auto_interval_minutes = 60
max_backups_per_world = 50
compression = "zstd"

[paths]
custom_backup_dir = "D:\MeusBackups\Minecraft"
cloud_sync_enabled = false

[ui]
theme = "system"  # light, dark, system
language = "pt-BR"

[advanced]
multi_threading = false
log_level = "INFO"
```

---

## 🔗 Próximos Passos

- [FAQ →](./faq.md)
- [Troubleshooting →](./troubleshooting.md)
- [Guia Dev: Feature Flags →](../development/feature-flags.md)
