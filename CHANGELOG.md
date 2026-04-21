# Changelog

> ⚠️ **NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.**

Todas as mudanças notáveis deste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-04-21

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

- ✅ Listagem automática de mundos Bedrock (3 fontes: Normal, UWP Store, Shared)
- ✅ Criação de backups com timestamp (YYYY-MM-DD_HH-MM-SS)
- ✅ Restauração de mundos a partir de backups
- ✅ Suporte multi-conta Microsoft + UWP Store + Shared
- ✅ Interface desktop com CustomTkinter
- ✅ 128 testes automatizados
- ✅ Validação robusta com Pydantic
- ✅ Documentação completa (README, TESTING, CONTRIBUTING)
- ✅ Professional UI/UX com color scheme consistente
- ✅ Semantic versioning e conventional commits

### Changed

- Migração de DearPyGui para CustomTkinter
- Remoção de emojis decorativos de buttons
- Melhorias visuais (cores, rounded corners, hover effects)
- Setup inicial com versão beta para feedback

### Notes

- **Estado:** MVP (Mínimo Produto Viável) - Beta
- **Status:** Funcional e testado
- **Feedback:** Contribuições e sugestões são bem-vindas!

---

## Versioning

Este projeto segue [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH[-PRERELEASE]**
- Exemplos: 0.1.0-beta, 0.1.0-beta.1, 0.1.0-rc.1, 0.1.0

### Release Strategy

- **0.1.0-beta** — MVP inicial (current)
- **0.1.0-rc.1** — Release candidate (após testes)
- **0.1.0** — Versão estável (depois fixes confirmados)
- **0.2.0** — Features adicionais (se houver feedback)
- **1.0.0** — Produto consolidado (futuro)

---

**Última atualização:** 2026-04-17
