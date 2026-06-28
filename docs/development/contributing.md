---
icon: lucide/git-commit
---

# Contributing

Obrigado pelo interesse no Minecraft Bedrock Backup Manager!

---

## Antes de começar

- Leia o [DCO](dco.md) — é obrigatório para contribuir
- Leia a [Licença](license.md) — este projeto é AGPL-3.0-or-later
- Veja as [Feature Flags](feature-flags.md) para entender como trabalhar com features inacabadas
- Veja o [Trunk-Based Development](trunk-based-development.md) para entender o fluxo de branches

---

## Configuração inicial (faça uma vez)

**1. Configure seu nome:**

```bash
git config --global user.name "Seu Nome"
```

**2. Use o email privado do GitHub (recomendado):**

Para não expor seu email pessoal no histórico público do git, use o email noreply do GitHub.

Para encontrar o seu:

- Acesse **GitHub → Settings → Emails**
- Marque **"Keep my email address private"**
- Copie o email no formato `123456789+username@users.noreply.github.com`

Configure no git:

```bash
git config --global user.email "123456789+username@users.noreply.github.com"
```

**3. Ao commitar, sempre adicione `-s`:**

```bash
git commit -s -m "feat: sua mensagem"
```

Isso gera automaticamente:

```
Signed-off-by: Seu Nome <123456789+username@users.noreply.github.com>
```

PRs sem `Signed-off-by` em todos os commits serão bloqueadas automaticamente.

---

## Header de licença

Todo arquivo `.py` novo deve ter o header nas primeiras linhas:

```python
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad
```

Rode o script para adicionar automaticamente:

```bash
uv run python scripts/add_license_header.py
```

---

## Uso de IA

Contribuições geradas com auxílio de IA são permitidas, desde que:

- Você revise e entenda o código que está submetendo
- O código não viole direitos autorais de terceiros
- O `Signed-off-by` seja incluído normalmente

A responsabilidade pelo conteúdo submetido é sempre do contribuidor.

---

## Fluxo de contribuição

1. Fork do repositório
2. Cria branch seguindo o padrão do projeto: `git checkout -b feature/sua-feature`
3. Commits com `-s`: `git commit -s -m "feat: descrição"`
4. Push e abre PR em `main`
5. Aguarda review

---

## Conventional Commits

Siga o padrão já usado no projeto:

| Tipo        | Quando usar                              |
| ----------- | ---------------------------------------- |
| `feat:`     | Nova funcionalidade                      |
| `fix:`      | Correção de bug                          |
| `docs:`     | Documentação                             |
| `refactor:` | Refatoração sem mudança de comportamento |
| `test:`     | Testes                                   |
| `chore:`    | Manutenção, dependências                 |

Exemplo:

```bash
git commit -s -m "feat: adicionar suporte a backup incremental"
```

---

## Checklist antes de abrir PR

- [ ] Todos os commits têm `Signed-off-by` (`git commit -s`)
- [ ] Arquivos `.py` novos têm o header SPDX
- [ ] Testes passando (`uv run task test`)
- [ ] Lint passando (`uv run task lint`)
- [ ] Formatação ok (`uv run task format`)
