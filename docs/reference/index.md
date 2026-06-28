---
icon: lucide/book-open
---

# Referência Técnica

Documentação de referência da API interna: Models, Ports, Services e Configuração.

---

## 🎯 Visão Geral

Esta seção documenta os contratos públicos e estruturas de dados usadas internamente. Útil para desenvolvedores que querem contribuir ou estender o projeto.

<div class="grid cards" markdown>

-   :material-class:{ .lg .middle } **Models (Pydantic)**

    WorldModel, BackupModel, ProgressModel — validação, serialização, type hints.

    [:octicons-arrow-right-24: Ver Models](./models.md)

-   :material-api:{ .lg .middle } **Ports (Interfaces ABC)**

    WorldRepositoryPort, BackupRepositoryPort — contratos de persistência.

    [:octicons-arrow-right-24: Ver Ports](./ports.md)

-   :material-cog:{ .lg .middle } **Services**

    WorldService, BackupService, ProgressService — lógica de negócio.

    [:octicons-arrow-right-24: Ver Services](./services.md)

-   :material-cog-outline:{ .lg .middle } **Configuração**

    Feature flags, variáveis de ambiente, settings.

    [:octicons-arrow-right-24: Ver Config](./config.md)

</div>

---

## 🔗 Navegação Rápida

| Documento | Descrição |
|-----------|-----------|
| [Models](./models.md) | Pydantic models com validações |
| [Ports](./ports.md) | Interfaces ABC (contratos) |
| [Services](./services.md) | Lógica de negócio |
| [Config](./config.md) | Feature flags, env vars |

---

## 📖 Leituras Relacionadas

- [Arquitetura Overview](../architecture/overview.md) — Como as peças se conectam
- [Ports & Models](../architecture/ports-and-models.md) — Detalhes de contratos e DI
- [Development Setup](../getting-started/usage.md) — Como rodar testes
