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

Ative features experimentais antes de executar:

```bash title="PowerShell"
# Auto-backup em background
$env:FF_AUTO_BACKUP = "true"
uv run task dev

# Preview antes de restaurar
$env:FF_RESTORE_PREVIEW = "true"
uv run task dev

# Múltiplas flags
$env:FF_AUTO_BACKUP = "true"
$env:FF_CLOUD_SYNC = "true"
$env:FF_RESTORE_PREVIEW = "true"
uv run task dev
```

```cmd title="CMD"
set FF_AUTO_BACKUP=true
set FF_RESTORE_PREVIEW=true
MinecraftBedrockBackupManager.exe
```

| Flag | Padrão | Descrição |
|------|--------|-----------|
| `FF_AUTO_BACKUP` | `false` | Backup automático periódico |
| `FF_CLOUD_SYNC` | `false` | Sincronização com nuvem (WIP) |
| `FF_RESTORE_PREVIEW` | `false` | Preview de restauração |
| `FF_MULTI_THREADING` | `false` | Operações paralelas |
| `FF_ADVANCED_LOGGING` | `false` | Logs verbosos |

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
