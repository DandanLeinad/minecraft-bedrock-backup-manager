# Changelog

> ⚠️ **NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.**

Todas as mudanças notáveis deste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


Este projeto segue [Semantic Versioning](https://semver.org/) com formatação **PEP 440**:

- **MAJOR.MINOR.PATCH[-PRERELEASE]**
- Exemplos: `0.1.0b0`, `0.1.0b1`, `0.1.0rc1`, `0.1.0`
- Pré-releases: `a` (alpha), `b` (beta), `rc` (release candidate)

### Release Strategy

- **0.1.0b0** — MVP inicial ✅
- **0.4.0b0** — Clean Architecture + Feature Flags ✅
- **0.5.0b0** — World Icon Preview + Commitizen migration ✅
- **0.6.0b0** — Background thread + Real progress tracking ✅
- **0.7.0b0** — Real file-by-file progress + Background threads (current) ✅
- **0.x.0rc1** — Release candidate (após testes)
- **0.x.0** — Versão estável
- **1.0.0** — Produto consolidado (futuro)

### Versionamento com Commitizen (a partir de 0.5.0b0)

O versionamento agora é **automático via Conventional Commits**:

| Commit Type | Bump | Exemplo |
|-------------|------|---------|
| `fix:` | PATCH | `fix(core): handle missing icon` |
| `feat:` | MINOR | `feat(ui): add world preview` |
| `BREAKING CHANGE:` | MAJOR | `feat(api)!: change backup format` |
| `refactor:`, `docs:`, `chore:`, etc. | Nenhum | — |

**Versão atual:** 0.7.0b0

**Comandos:**
```bash
uv run task cz-bump        # Lança nova versão (analisa commits, atualiza arquivos, cria tag)
uv run task cz-bump-dry    # Preview do bump
uv run task cz-version     # Mostra versão atual
uv run task cz-changelog   # Atualiza CHANGELOG.md
uv run task cz-check       # Valida commits recentes
```

**Fluxo:**
1. Desenvolva com Conventional Commits (`feat:`, `fix:`, etc.)
2. Rode `uv run task cz-bump` quando quiser lançar
3. Commitizen determina o bump, atualiza `pyproject.toml`, `version.json`, `CHANGELOG.md`
4. Cria commit `bump: version X.Y.Z → X.Y.(Z+1)` e tag `vX.Y.Z`

---

**Última atualização:** 2026-06-12

## v0.7.1b0 (2026-06-17)

## v0.7.0b0 (2026-06-12)

## v0.6.0b0 (2026-06-11)

## v0.5.0b0 (2026-06-10)

## v0.4.0-beta (2026-05-02)

### Fix

- correct line endings in bumpversion.toml
- resolve remaining linting errors (SIM115, SIM117, SIM108, RUF005, B023)
- convert python 2 exception syntax to python 3 and update pre-commit ruff version

## v0.1.0-beta (2026-04-17)

### Feat

- add feature flags, improve CI/CD pipeline, and create short-branch guide
- v0.1.0-beta
