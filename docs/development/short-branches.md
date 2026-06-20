# ⏱️ Branches Curtas - Guia Prático

## Princípios Trunk-Based com Branches Curtas

- ✅ **Duração**: Máximo 3-5 dias
- ✅ **Tamanho**: Máximo 400 linhas por PR
- ✅ **Commits**: 3-7 commits pequenos e focados
- ✅ **Integração**: Merge frequente em main
- ✅ **Features**: Use flags para features inacabadas

---

## 🎯 Exemplo 1: Auto-Backup Feature (3 dias)

### Dia 1 - Estrutura Base

```bash
git checkout main && git pull
git checkout -b feature/auto-backup

# Implementar estrutura base
# → service/auto_backup_service.py (vazio/skeleton)
# → models/auto_backup_model.py
# → testes unitários

git add .
git commit -m "feat: add auto-backup service skeleton"
git push origin feature/auto-backup
```

**PR #1:**

- Título: `feat: auto-backup service structure`
- Descrição: "Estrutura base para auto-backup (feature incompleta)"
- Flag: `FF_AUTO_BACKUP=false` por padrão
- Tamanho: ~150 linhas

### Dia 2 - Lógica Base

```bash
# Implementar lógica principal
# → auto_backup_service.py (30% do código)
# → testes

git add .
git commit -m "feat: implement schedule detection"
git push origin feature/auto-backup
```

**PR #2:**

- Título: `feat: auto-backup scheduling logic`
- Tamanho: ~120 linhas
- Status: 60% completo

### Dia 3 - UI + Finalização

```bash
# Adicionar à UI
# → buttons para enable/disable
# → settings UI

git add .
git commit -m "feat: add auto-backup UI controls"

git add .
git commit -m "test: cover edge cases"

# Feature pronta! Merge em main com flag
git push origin feature/auto-backup
```

**PR #3:**

- Título: `feat: auto-backup UI and finalization`
- Tamanho: ~130 linhas
- Status: 100% completo
- Pronto para manter disabled até release

### Dia 4 - Release (ao invés de Dia 4)

```bash
# Quando pronto para release
git checkout main && git pull
# Mudar FF_AUTO_BACKUP padrão de "false" → "true"
git add config/feature_flags.py
git commit -m "feat: enable auto-backup in production"
uv run task bump-minor
git push origin main --tags
```

---

## 🎯 Exemplo 2: Bug Fix (1 dia)

```bash
git checkout main && git pull
git checkout -b fix/encoding-issue

# Investigar bug
git add src/services/backup_service.py
git commit -m "fix: handle non-ASCII backup names"

git add tests/unit/services/test_backup_service.py
git commit -m "test: verify encoding fix with unicode paths"

git push origin fix/encoding-issue
```

**PR:**

- Título: `fix: handle unicode in backup paths`
- Tamanho: ~80 linhas
- Duração: 1-2 horas
- Merge imediato após review

---

## 🎯 Exemplo 3: Chore/Docs (1 dia)

```bash
git checkout main && git pull
git checkout -b chore/update-deps

# Atualizar dependências
uv sync
git add uv.lock pyproject.toml
git commit -m "chore: upgrade pytest from 9.0.3 to 9.1.0"

git add docs/DEVELOPMENT.md
git commit -m "docs: update testing section"

git push origin chore/update-deps
```

**PR:**

- Título: `chore: upgrade dependencies and docs`
- Duração: 2-4 horas
- Merge after CI passes

---

## ⏰ Padrão Temporal Recomendado

| Tipo | Duração | Exemplo |
|------|---------|---------|
| `fix/*` | 2-4 horas | Bug crítico, crash |
| `docs/*` | 2-8 horas | README, guia, exemplos |
| `chore/*` | 4-8 horas | Deps, configs, scripts |
| `feat/*` (pequena) | 1 dia | Simples validação, helper |
| `feat/*` (média) | 2-3 dias | Nova tela, serviço |
| `feat/*` (grande) | Use flags! | Auto-backup, cloud-sync |

---

## ✅ Checklist para Branches Curtas

### Antes de começar

- [ ] Issue/task clara definida
- [ ] Scope bem limitado (1 feature apenas)
- [ ] Duração estimada ≤ 5 dias
- [ ] Sabe como testar localmente

### Durante desenvolvimento

- [ ] Commits pequenos (3-7 commits)
- [ ] Cada commit compila/passa testes
- [ ] Mensagens Conventional Commits
- [ ] Máximo 400 linhas por PR
- [ ] Features usam flags se inacabadas

### Antes de push

- [ ] `uv run task test` passa ✅
- [ ] `uv run task lint` passa ✅
- [ ] `uv run task format` passou ✅
- [ ] Pre-commit hooks instalados ✅

### Na PR

- [ ] Descrição clara
- [ ] Screenshots (se UI)
- [ ] Testing instructions
- [ ] Pronto para merge (nenhuma blocker)

---

## 🚀 Merge e Cleanup

```bash
# ✅ Após PR aprovada:
git checkout main
git pull origin main

# Opção 1: Squash (histórico limpo)
git merge --squash feature/nome
git commit -m "feat: description"

# Opção 2: Rebase (histórico linear)
git rebase origin/main feature/nome
git checkout main
git merge feature/nome

# Push
git push origin main

# Delete branch (local + remote)
git branch -d feature/nome
git push origin --delete feature/nome
```

---

## 📊 Métrica de Saúde

Para manter branches curtas saudáveis:

```
✅ Verde   → Média 2 dias, max 5 dias
🟡 Amarelo → Média 4 dias, max 7 dias
🔴 Vermelho → Branches >7 dias = RISCO!
```

Se branch vai >5 dias:

1. Divida em 2 PRs
2. Use feature flags
3. Meça por "points" em vez de dias

---

## 🎓 Por Que Branches Curtas?

- ✅ Menos conflitos (código muda rápido)
- ✅ Easier code review (poucas linhas)
- ✅ Faster feedback (CI/CD rápido)
- ✅ Menos bugs (mudanças pequenas, testadas)
- ✅ Release ready (sempre pronto para deploy)
- ✅ Team produtivo (menos waiting)
