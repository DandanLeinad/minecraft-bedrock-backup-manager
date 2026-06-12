# Changelog

> ⚠️ **NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.**

Todas as mudanças notáveis deste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.0b0] - 2026-06-12

### Added
- Real file-by-file progress tracking for backup/restore operations
- Background thread execution for backup/restore operations (UI stays responsive)
- Progress callback with per-file granularity

### Changed
- Background thread execution for backup/restore operations
- Thread-safe UI updates via main_window.after() callbacks
- Progress callback converts (current,total) → ProgressModel

### Fixed
- UI freeze during backup/restore operations
- Progress bar now shows real per-file progress

## [0.6.0b0] - 2026-06-11

### Added
- World Icon Preview: world_icon.jpeg preview in worlds list and details
- Real file-by-file progress tracking for backup/restore operations
- Background thread execution for backup/restore operations (UI stays responsive)

### Changed
- Background thread execution for backup/restore operations
- Thread-safe UI updates via main_window.after() callbacks

### Fixed
- Pyright type errors (32 errors fixed)

## [0.5.0b0] - 2026-06-10

### Added
- Preview de ícone do mundo (world_icon.jpeg) na lista de mundos e detalhes
  - Novo utilitário `WorldIconLoader` para carregar/renderizar imagem 800x450 (proporção 16:9)
  - Feature flag: `ENABLE_WORLD_ICON_PREVIEW` (ativa por padrão)
  - Tamanhos: 48px altura (~85px largura) na lista, 128px altura (~228px largura) no header
  - Cache em memória para performance

### Changed
- **Migração de versionamento**: `bump-my-version` → `Commitizen`
  - Remove dependência transitiva vulnerável `idna 3.11` (CVE-2024-3651)
  - Versionamento automático baseado em Conventional Commits (`feat:`, `fix:`, `BREAKING CHANGE:`)
  - Changelog gerado automaticamente a partir dos commits
  - Tasks: `cz-bump`, `cz-changelog`, `cz-version`, `cz-check`
  - Tag format: `v$version` (ex: `v0.5.0b0`)
- **Normalização de versão**: `0.5.0-beta` → `0.5.0b0` (PEP 440)
  - Formato compatível com ferramentas modernas (Commitizen, PyPI, uv)
  - Tags Git: `v0.5.0b0`, `v0.6.0b0`, etc.

## [0.4.0-beta] - 2026-05-02

<!-- Seção mantida para compatibilidade com bump-my-version -->

### Added
- Refatoração para Clean Architecture com separação entre core, infra e ui
- Reorganização dos testes unitários por comportamento:
  - tests/unit/backup/
  - tests/unit/world/
  - tests/unit/progress/
- Centralização de fixtures compartilhadas em tests/unit/conftest.py

### Changed
- UI de restauração ajustada para usar o fluxo de preview quando a feature flag está ativa
- FF_RESTORE_PREVIEW ativada por padrão no ambiente de desenvolvimento
- Atualização de dependências e tooling:
  - PyInstaller 6.20.0
  - pre-commit
  - pyright
  - ruff

## [0.3.0-beta] - 2026-04-22

### Added
- Preview de conteúdo do backup antes de restaurar (MC-3)
  - Novo método `BackupService.get_backup_preview_info()`
  - Tela customizada mostrando arquivos e pastas do backup
  - Tamanho total e metadados do backup
  - Feature flag: `FF_RESTORE_PREVIEW` (ativável com `FF_RESTORE_PREVIEW=true`)
  - 10 testes abrangentes (205 total)

### Fixed
- UnicodeEncodeError ao fazer log de mensagens com emojis no Windows
  - Regex pattern para remover todos os emojis antes de logging
  - Mantém emojis na UI (dialogs, toasts)
  - Remove emojis apenas nos logs (compatível com cp1252)

## [0.2.0-beta] - 2026-04-21

### Added
- Nova estrutura de Trunk-Based Development
- Versionamento automático com `bump-my-version`
- Feature flags para features em desenvolvimento
- Barra de progresso visual para operações de backup/restore (MC-2)
  - Componente customizado com CustomTkinter
  - Callback pattern para rastreamento de progresso
  - Integração com BackupService e UI controller
  - Suporte a múltiplos stages de operação

### Changed
- Migração de Git Flow para Trunk-Based Development
- Melhorias no fluxo de CI/CD

## [0.1.0-beta] - 2026-04-14

### Added
- Listagem automática de mundos Bedrock (3 fontes: Normal, UWP Store, Shared)
- Criação de backups com timestamp (YYYY-MM-DD_HH-MM-SS)
- Restauração de mundos a partir de backups
- Suporte multi-conta Microsoft + UWP Store + Shared
- Interface desktop com CustomTkinter
- 128 testes automatizados
- Validação robusta com Pydantic
- Documentação completa (README, TESTING, CONTRIBUTING)
- Professional UI/UX com color scheme consistente
- Semantic versioning e conventional commits

### Changed
- Migração de DearPyGui para CustomTkinter
- Remoção de emojis decorativos de buttons
- Melhorias visuais (cores, rounded corners, hover effects)
- Setup inicial com versão beta para feedback

---

## Versioning

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
