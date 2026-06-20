# 🚀 Feature Flags Implementation Guide

## Exemplo Prático

### Na UI - Mostrar botão apenas se flag ativada

**Antes (sem flag):**

```python
# ❌ Problema: Feature incompleta quebra produção
def _setup_buttons(self) -> None:
    self.backup_btn = create_button("Backup")
    self.restore_btn = create_button("Restore")
    self.preview_btn = create_button("Preview")  # ❌ QUEBRA SE INCOMPLETO!
    self.sync_btn = create_button("Cloud Sync")   # ❌ QUEBRA SE INCOMPLETO!
```

**Depois (com flag):**

```python
from backup_manager_mvp.config import FEATURE_FLAGS

def _setup_buttons(self) -> None:
    self.backup_btn = create_button("Backup")
    self.restore_btn = create_button("Restore")

    # ✅ Só mostra em desenvolvimento
    if FEATURE_FLAGS.ENABLE_RESTORE_PREVIEW:
        self.preview_btn = create_button("Preview")

    # ✅ Só mostra em desenvolvimento
    if FEATURE_FLAGS.ENABLE_CLOUD_SYNC:
        self.sync_btn = create_button("Cloud Sync")
```

---

## Workflow com Feature Flags

### 1️⃣ Criar Feature Branch

```bash
git checkout -b feature/auto-backup
```

### 2️⃣ Implementar Feature com Flag

```python
from backup_manager_mvp.config import FEATURE_FLAGS

class BackupService:
    def backup_world(self, world_id: str) -> bool:
        """Faz backup do mundo."""
        # Código base que SEMPRE funciona
        self._create_backup(world_id)

        # ✅ Feature nova - protegida por flag
        if FEATURE_FLAGS.ENABLE_AUTO_BACKUP:
            self._schedule_auto_backup(world_id)

        return True
```

### 3️⃣ Commitar e Push

```bash
git add .
git commit -m "feat: add auto-backup with feature flag"
git push origin feature/auto-backup
```

### 4️⃣ Abrir PR

- Testes rodam ✅
- Feature ativada via flag para CI
- Feature desativada por padrão

### 5️⃣ Merge em main

```bash
# Feature merged mas DESATIVADA por padrão
# Só ativa em desenvolvimento com:
FF_AUTO_BACKUP=true uv run python -m backup_manager_mvp.main
```

### 6️⃣ Release com Feature Ativada

Quando feature está pronta:

```bash
# 1. Mudar padrão em feature_flags.py
ENABLE_AUTO_BACKUP: bool = _parse_bool(os.getenv("FF_AUTO_BACKUP", "true"))

# 2. Commit + bump version
git add .
git commit -m "feat: enable auto-backup in production"
uv run task bump-minor

# 3. Push + GitHub Actions cria release
git push origin main --tags
```

---

## Testing com Flags

```python
import pytest
import os

def test_auto_backup_disabled():
    """Testa que feature é segura quando desativada."""
    os.environ["FF_AUTO_BACKUP"] = "false"
    from backup_manager_mvp.config import FEATURE_FLAGS

    assert FEATURE_FLAGS.ENABLE_AUTO_BACKUP is False
    # ... test backup sem auto-schedule

def test_auto_backup_enabled():
    """Testa feature quando ativada."""
    os.environ["FF_AUTO_BACKUP"] = "true"
    from backup_manager_mvp.config import FEATURE_FLAGS

    assert FEATURE_FLAGS.ENABLE_AUTO_BACKUP is True
    # ... test auto-schedule funciona
```

---

## Checklist para Feature Flag

- [ ] Feature criada em branch curta (`feature/nome`)
- [ ] Flag adicionada em `config/feature_flags.py`
- [ ] Código protegido: `if FEATURE_FLAGS.ENABLE_*:`
- [ ] Padrão é `"false"` (desativado)
- [ ] Testes passam com flag ativada E desativada
- [ ] Documentação updated em código
- [ ] PR descrita com: "Ativa via `FF_*=true`"
- [ ] Quando pronto para release: mudar padrão + bump version

---

## Flags Disponíveis

| Flag | Status | Propósito |
|------|--------|----------|
| `FF_AUTO_BACKUP` | Em Desenvolvimento | Auto-backup em background |
| `FF_CLOUD_SYNC` | Em Desenvolvimento | Sincronização com cloud |
| `FF_RESTORE_PREVIEW` | Em Desenvolvimento | Preview antes de restaurar |
| `FF_MULTI_THREADING` | Experimental | Operações paralelas |
| `FF_ADVANCED_LOGGING` | Experimental | Logs detalhados para debug |

---

## Executar com Flags

```bash
# Uma flag
FF_AUTO_BACKUP=true uv run python -m backup_manager_mvp.main

# Múltiplas flags
FF_AUTO_BACKUP=true FF_RESTORE_PREVIEW=true uv run python -m backup_manager_mvp.main

# No CI
FF_AUTO_BACKUP=true FF_CLOUD_SYNC=true uv run task test
```
