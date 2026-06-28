---
icon: lucide/cpu
---

# Setup de Desenvolvimento

## Setup Rápido

```bash
# Clone
git clone https://github.com/DandanLeinad/minecraft-bedrock-backup-manager.git
cd minecraft-bedrock-backup-manager

# Instale uv (Windows):
irm https://astral.sh/uv/install.ps1 | iex

# Setup
uv sync --all-groups

# Valide
uv run pytest tests/ -q
```

## Workflow Diário

```bash
# Rodar app
uv run task dev

# Rodar testes
uv run task test

# Formatar + lint + type check
uv run task format
uv run task lint
uv run task type-check

# Compilar executável
uv run task build           # Release
uv run task build-full      # Limpa + rebuild
```

## Git Workflow (Trunk-Based)

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

## Branches

- **`main`** — Protegida (releases com tags, trunk)
- **`feature/*`** — Features novas (vida curta: 3-5 dias)
- **`fix/*`** — Bug fixes
- **`chore/*`** — Manutenção
- **`docs/*`** — Documentação

## Testes

```bash
uv run pytest tests/ -v              # Todos, detalhado
uv run pytest tests/ --cov=src       # Com cobertura
uv run pytest tests/unit/models/     # Apenas models
```

Ver [Testes](../development/testing.md) para mais.
