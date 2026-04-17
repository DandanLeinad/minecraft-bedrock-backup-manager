# 🔧 Configuration Module

Configurações centralizadas da aplicação.

## Módulos

### `feature_flags.py`

Feature flags para features em desenvolvimento.

**Uso:**

```python
from backup_manager_mvp.config import FEATURE_FLAGS

if FEATURE_FLAGS.ENABLE_AUTO_BACKUP:
    # Fazer algo...
    pass
```

**Flags Disponíveis:**

- `ENABLE_AUTO_BACKUP` - Auto-backup em background
- `ENABLE_CLOUD_SYNC` - Sincronização com cloud
- `ENABLE_RESTORE_PREVIEW` - Preview antes de restaurar
- `ENABLE_MULTI_THREADING` - Operações paralelas
- `ENABLE_ADVANCED_LOGGING` - Logs detalhados

**Ativar Flags:**

```bash
FF_AUTO_BACKUP=true uv run python -m backup_manager_mvp.main
```

**Documentação Completa:**

Veja [FEATURE_FLAGS.md](../docs/FEATURE_FLAGS.md) para exemplos e guia de implementação.
