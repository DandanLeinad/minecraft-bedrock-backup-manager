# Changelog

> ⚠️ **NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.**

Todas as mudanças notáveis deste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

<!-- Seção mantida para compatibilidade com bump-my-version -->

## [0.4.0-beta] - 2026-05-02

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

Este projeto segue [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH[-PRERELEASE]**
- Exemplos: 0.1.0-beta, 0.1.0-beta.1, 0.1.0-rc.1, 0.1.0

### Release Strategy

- **0.1.0-beta** — MVP inicial ✅
- **0.4.0-beta** — Clean Architecture + Feature Flags (current)
- **0.x.0-rc.1** — Release candidate (após testes)
- **0.x.0** — Versão estável
- **1.0.0** — Produto consolidado (futuro)

---

**Última atualização:** 2026-04-17
