# Changelog

> ⚠️ **NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.**

Todas as mudanças notáveis deste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


Este projeto segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html) com formatação **PEP 440**:

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

**Versão atual:** 0.7.1b0

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
5. Cria commit `bump: version X.Y.Z → X.Y.(Z+1)` e tag `vX.Y.Z`

---

**Última atualização:** 2026-06-17

## v0.7.1b0 (2026-06-17)

### Test

- Reorganize test suite to domain-first structure with English messages
- Move tests from `tests/unit/` and `tests/integration/` to domain-first structure:
  - `tests/world/unit/`, `tests/world/integration/`
  - `tests/backup/unit/`, `tests/backup/integration/`
  - `tests/progress/unit/`, `tests/ui/unit/`, `tests/utils/unit/`
- Rename all test files PT→EN:
  - `test_descoberta_mundos.py` → `test_world_discovery.py`
  - `test_metadados_mundo.py` → `test_world_metadata.py`
  - `test_criar_backup.py` → `test_create_backup.py`
  - `test_listar_backups.py` → `test_list_backups.py`
  - `test_restaurar_backup.py` → `test_restore_backup.py`
  - `test_progresso_backup.py` → `test_backup_progress.py`
- Rename all tests to BDD pattern: `test_should_<expected>_when_<condition>`
- Add auto-markers via `pytest_collection_modifyitems`:
  - Domain: `world`, `backup`, `progress`, `ui`, `utils`
  - Type: `unit`, `integration`, `slow`
- Add factories: `WorldFactory`, `BackupFactory` in `tests/factories/`
- Translate all docstrings/error messages to English describing business rules
- Group tests in classes by behavior (`TestFolderNameValidation`, `TestCreateBackup`, etc.)
- Update source code to raise English error messages
- Remove old `tests/unit/` and `tests/integration/` directories

### Refactor

- Restructure test suite to domain-first layout
- Translate all test names, docstrings, and error messages to English
- Add pytest auto-markers for domain and test type filtering
- Add test factories for clean test data creation
- Convert all error messages in source code to English

### Refactor

- Convert all test file names from Portuguese to English
- Rename all test functions to BDD pattern (`test_should_<expected>_when_<condition>`)
- Add pytest auto-markers for domain and test type
- Create test factories for WorldModel and BackupModel
- Translate all test docstrings and error messages to English
- Update source code error messages to English

## v0.7.0b0 (2026-06-12)

### Feature

- Implement real file-by-file progress tracking for backup and restore operations
- Replace fake `total=1` placeholder with actual file-by-file progress
- Add `copy_tree_with_progress()` to `BackupRepositoryPort`
- Implement recursive copy with per-file callback in `FileSystemBackupRepository`
- Update `BackupService.create_backup()` and `restore_backup()` to use progress tracking

### Refactor

- Add `_create_progress_callback()` helper to convert `(current, total)` → `ProgressModel`
- Pre-scan total file count before copy for accurate progress denominator
- Works for both backup and restore operations
- Progress granularity: per file (not per directory)

### Test

- Add 13 progress tracking tests (create + restore with progress)
- Add progress callback tests for create/restore operations
- Test progress starts at 0%, ends at 100%, includes stage text

### Chore

- Update version to 0.7.0b0

## v0.6.0b0 (2026-06-11)

### Feature

- Add background thread support for long-running operations
- Implement real progress tracking (replaces fake progress)
- Add `ProgressService` and `ProgressModel` for thread-safe progress tracking

### Refactor

- Move backup/restore operations to background threads
- Implement `ProgressService` with callback-based progress reporting
- Add `ProgressModel` with percentage calculation and completion status

## v0.5.0b0 (2026-06-10)

### Feature

- Add world icon preview feature (`FF_WORLD_ICON`)
- Implement world icon loading and caching
- Add `IconLoader` with async loading and memory cache

### Feature

- Add feature flags system (`FF_WORLD_ICON`, `FF_AUTO_BACKUP`, etc.)
- Implement `FeatureFlags` config with env var overrides

### Fix

- Fix world icon loading race conditions
- Fix cache invalidation on world rename

## v0.4.0b0 (2026-05-02)

### Refactor

- Migrate to Clean Architecture (Domain, Application, Infrastructure, UI layers)
- Introduce Repository Pattern (`WorldRepositoryPort`, `BackupRepositoryPort`)
- Implement `FileSystemWorldRepository` and `FileSystemBackupRepository`

### Feature

- Add feature flags system (`FF_WORLD_ICON`, `FF_AUTO_BACKUP`, etc.)
- Implement `FeatureFlags` config with env var overrides

### Fix

- Fix world icon loading race conditions
- Fix cache invalidation on world rename

### Fix

- Correct line endings in bumpversion.toml
- Resolve remaining linting errors (SIM115, SIM117, SIM108, RUF005, B023)
- Convert python 2 exception syntax to python 3 and update pre-commit ruff version

## v0.1.0-beta (2026-04-17)

### Feat

- Add feature flags, improve CI/CD pipeline, and create short-branch guide
- Initial MVP: world discovery, backup creation, listing, and restore
- Basic UI with CustomTkinter (world list, backup list, progress bar)
- World discovery from 3 sources (Normal, UWP Store, Shared)
- Backup creation with timestamp, restore with confirmation
- Pydantic models for WorldModel, BackupModel, ProgressModel

### Feat

- Add feature flags, improve CI/CD pipeline, and create short-branch guide
- Initial MVP: world discovery, backup creation, listing, and restore
- Basic UI with CustomTkinter (world list, backup list, progress bar)
- World discovery from 3 sources (Normal, UWP Store, Shared)
- Backup creation with timestamp, restore with confirmation
- Pydantic models for WorldModel, BackupModel, ProgressModel
