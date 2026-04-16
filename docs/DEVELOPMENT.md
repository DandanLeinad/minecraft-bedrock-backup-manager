# 🔧 Desenvolvimento

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

## Git Workflow

```bash
# 1. Partir de develop
git checkout develop
git pull origin develop

# 2. Criar feature branch
git checkout -b feature/my-feature

# 3. Commitar (siga commitlint)
git add .
git commit -m "feat: add new feature"

# 4. Push
git push -u origin feature/my-feature

# 5. Pull Request (via GitHub)
# → Merge em develop

# 6. Delete branch
git push origin --delete feature/my-feature
```

## Branches

- **`main`** — Protegida (releases com tags)
- **`develop`** — Padrão (onde você trabalha)
- **`feature/*`** — Features novas
- **`fix/*`** — Bug fixes

## Testes

```bash
uv run pytest tests/ -v              # Todos, detalhado
uv run pytest tests/ --cov=src       # Com cobertura
uv run pytest tests/unit/models/     # Apenas models
```

Ver [TESTING.md](./TESTING.md) para mais.
