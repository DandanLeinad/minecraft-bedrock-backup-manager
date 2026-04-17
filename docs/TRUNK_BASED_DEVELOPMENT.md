# Trunk-Based Development (Hybrid GitHub Flow)

> Metodologia de desenvolvimento ágil focada em integração contínua com branches curtas e testes automatizados.

## 📋 Visão Geral

Este projeto segue uma abordagem **Hybrid entre GitHub Flow e Trunk-Based Development**:

- ✅ Branches de curta duração (máx 3-5 dias)
- ✅ Testes automatizados obrigatórios
- ✅ Feature Flags para features inacabadas
- ✅ Versionamento automático
- ✅ PRs obrigatórias (mesmo para desenvolvimento solo)

---

## 🌳 Estrutura de Branches

```
main (trunk) ← SEMPRE PRONTO PARA PRODUÇÃO
  ↑
  ├─ feature/nova-funcionalidade (curta vida)
  ├─ fix/corrigir-bug (curta vida)
  └─ chore/atualizar-deps (curta vida)
```

### Regras

- **`main`**: Código pronto para release, sempre funcional
- **`feature/*`**: Novas funcionalidades (máx 3-5 dias)
- **`fix/*`**: Bugfixes críticos (máx 1-2 dias)
- **`chore/*`**: Atualizações, configuração (máx 1 dia)

---

## 🔄 Fluxo de Desenvolvimento

### 1️⃣ Criar Feature Branch

```bash
# Atualizar main
git checkout main
git pull origin main

# Criar feature branch
git checkout -b feature/nome-descritivo
```

**Nomes de branch:**

```
feature/adicionar-auto-backup
fix/corrigir-encoding-backup
chore/atualizar-dependencias
```

### 2️⃣ Desenvolver com Commits Pequenos

```bash
# Commits frequentes (3-5 linhas de mudança por commit)
git add .
git commit -m "feat: adicionar validação de caminho"

git add .
git commit -m "feat: integrar novo validador"

git add .
git commit -m "test: adicionar testes para validador"
```

**Formato de commit (Conventional Commits):**

```
<tipo>(<escopo>): <descrição>

feat:      nova funcionalidade
fix:       corrigir bug
docs:      documentação
style:     formatação de código
refactor:  refatoração sem mudança funcional
perf:      otimização de performance
test:      adicionar/modificar testes
chore:     atualizar dependências, build, etc
ci:        mudanças em CI/CD
```

### 3️⃣ Fazer Push e Abrir PR

```bash
# Push da feature branch
git push origin feature/nome-descritivo

# No GitHub:
# - Clique em "New Pull Request"
# - Selecione: feature/nome-descritivo → main
# - Descreva o que foi feito
```

### 4️⃣ Testes Automatizados (CI/CD)

GitHub Actions executará automaticamente:

- ✅ Testes (pytest)
- ✅ Linting (ruff)
- ✅ Validação de commit messages
- ✅ Coverage report

**Se falhar:** Faça fixes na mesma branch

```bash
git add .
git commit -m "fix: resolver falha no teste"
git push origin feature/nome-descritivo
```

### 5️⃣ Code Review e Merge

```bash
# Após PR ser aprovada:
# 1. Clique em "Squash and merge" (mantém histórico limpo)
# OU manualmente:

git checkout main
git pull origin main
git merge feature/nome-descritivo
git push origin main
```

### 6️⃣ Deletar Branch

```bash
# Localmente
git branch -d feature/nome-descritivo

# Remotamente
git push origin --delete feature/nome-descritivo
```

---

## 📦 Versionamento Automático

Use `bump-my-version` para versionar:

```bash
# Instalado como dependência dev
uv run bump-my-version --help

# Tipos de bump
uv run bump-my-version bump major    # 0.1.0 → 1.0.0
uv run bump-my-version bump minor    # 0.1.0 → 0.2.0
uv run bump-my-version bump patch    # 0.1.0 → 0.1.1
uv run bump-my-version bump pre_l    # 0.1.0 → 0.1.0-beta

# Atualiza automaticamente:
# - pyproject.toml
# - src/backup_manager_mvp/version.json
# - CHANGELOG.md
# - Cria git tag e commit
```

**Workflow de Release:**

```bash
# 1. Fazer merge de features em main
# 2. Quando pronto para release:
uv run bump-my-version bump minor

# 3. Isso faz:
#    ✅ Atualiza versão em 3 arquivos
#    ✅ Atualiza CHANGELOG.md
#    ✅ Cria commit automático
#    ✅ Cria git tag (v0.2.0)

# 4. Git push automático vai triggerar GitHub Actions
#    ✅ Testa código
#    ✅ Cria release no GitHub
#    ✅ Faz build do .exe
```

---

## 🎯 Feature Flags (Para Features Inacabadas)

Use para integrar código inacabado sem quebrar produção:

```python
# src/backup_manager_mvp/config/feature_flags.py
from dataclasses import dataclass
import os

@dataclass
class FeatureFlags:
    ENABLE_AUTO_BACKUP = os.getenv("FF_AUTO_BACKUP", "false").lower() == "true"
    ENABLE_CLOUD_SYNC = os.getenv("FF_CLOUD_SYNC", "false").lower() == "true"
    ENABLE_RESTORE_PREVIEW = os.getenv("FF_RESTORE_PREVIEW", "false").lower() == "true"

# Uso na UI
from config.feature_flags import FeatureFlags

if FeatureFlags.ENABLE_RESTORE_PREVIEW:
    # Mostrar botão de preview
    create_preview_button()
```

**Ativar flag para testes:**

```bash
# Via variável de ambiente
FF_AUTO_BACKUP=true uv run python -m backup_manager_mvp.main
```

---

## 🧪 Testes Obrigatórios

Antes de fazer push:

```bash
# Rodar testes localmente
uv run pytest -v

# Com coverage
uv run pytest -v --cov=src --cov-report=html

# Linting
uv run ruff check src/

# Formatação
uv run ruff format src/
```

**Tasks disponíveis:**

```bash
uv run task test          # Rodar testes
uv run task test-cov      # Testes + coverage
uv run task lint          # Verificar linting
uv run task format        # Formatar código
uv run task type-check    # Type checking
```

---

## 📋 Pre-commit Hooks

Os hooks rodam automaticamente antes de cada commit:

```bash
# Instalar hooks (uma vez)
pre-commit install

# Rodar manualmente em todos os arquivos
pre-commit run --all-files

# Bypass (se necessário)
git commit --no-verify
```

**Valida:**

- ✅ Conventional commits
- ✅ Code formatting (Ruff)
- ✅ Whitespace issues
- ✅ Large files
- ✅ YAML/TOML syntax
- ✅ Merge conflicts

---

## 📝 Checklist para PR

Antes de fazer submit:

- [ ] Branch name segue padrão (`feature/*`, `fix/*`)
- [ ] Commits seguem Conventional Commits
- [ ] Testes passam localmente (`uv run task test`)
- [ ] Code formatado (`uv run task format`)
- [ ] CHANGELOG.md atualizado (se necessário)
- [ ] Feature flags usadas para features inacabadas
- [ ] Sem `print()` ou `console.log()` (usar logging)
- [ ] Máximo 400 linhas por PR
- [ ] Descrição clara do que foi mudado

---

## 🚀 Workflow Completo (Exemplo)

```bash
# 1. Atualizar main
git checkout main
git pull origin main

# 2. Criar feature
git checkout -b feature/adicionar-preview

# 3. Desenvolver
# ... editar arquivos ...
git add .
git commit -m "feat: estrutura do preview"

git add .
git commit -m "feat: renderizar preview"

git add .
git commit -m "test: adicionar testes do preview"

# 4. Push
git push origin feature/adicionar-preview

# 5. Abrir PR no GitHub e esperar testes

# 6. Se tudo passar, mergear
git checkout main
git pull origin main
git merge feature/adicionar-preview
git push origin main

# 7. Delete branch
git branch -d feature/adicionar-preview
git push origin --delete feature/adicionar-preview

# 8. Se é release, versionem
uv run bump-my-version bump minor
# Isso faz push automático + tag
```

---

## ⚠️ Práticas a EVITAR

❌ **Commits diretos em `main`**

```bash
# ❌ NUNCA
git checkout main
git commit -m "fix: ..."
git push origin main

# ✅ SIM
git checkout -b fix/nome
git commit -m "fix: ..."
git push origin fix/nome
# ... abrir PR ...
```

❌ **Branches mortas por semanas**

```bash
# ❌ NUNCA deixar branches por >1 semana
# ✅ SIM deletar após merge
```

❌ **Ignorar falhas em testes**

```bash
# ❌ NUNCA fazer --no-verify
# ✅ SIM corrigir os testes
```

❌ **PRs gigantes**

```bash
# ❌ NUNCA PR com 1000+ linhas
# ✅ SIM dividir em múltiplas PRs
```

---

## 📚 Referências

- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)

---

**Última atualização:** 2026-04-17
