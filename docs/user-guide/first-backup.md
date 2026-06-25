---
icon: lucide/save
---

# Primeiro Backup

Passo a passo para fazer seu primeiro backup de mundo.

---

## 🎯 Visão Geral

1.  Abra o app
2.  Selecione um mundo
3.  Clique em **Fazer Backup**
4.  Aguarde concluir
5.  Pronto! ✅

---

## 📋 Passo a Passo

### 1. Abra o App

Execute `MinecraftBedrockBackupManager.exe`. A janela principal abrirá com a lista de mundos detectados.

!!! info "Detecção Automática"
    O app procura mundos em 3 locais:
    - Contas Microsoft (`%AppData%\Minecraft Bedrock\Users\{id}\...`)
    - UWP Store (`%LocalAppData%\Packages\Microsoft.MinecraftUWP_...\...`)
    - Shared (`%AppData%\Minecraft Bedrock\Users\Shared\...`)

### 2. Selecione um Mundo

Na barra lateral esquerda, clique no mundo desejado. Você verá:

-   **Nome do mundo** (levelname)
-   **Tamanho** estimado
-   **Conta** (UUID ou "UWP-Store"/"Shared")
-   **Último backup** (se houver)
-   **Quantidade de backups** existentes

### 3. Faça o Backup

Clique no botão **:material-content-save: Fazer Backup** (botão principal, cor primária).

=== "Durante o Backup"
    *   Barra de progresso aparece
    *   Mostra: "Preparando...", "Copiando arquivos...", "Concluído"
    *   Botão fica desabilitado até terminar

=== "Backup Concluído"
    *   Toast de sucesso: "Backup criado com sucesso!"
    *   Contador de backups atualiza na lista
    *   Timestamp do último backup aparece

---

## ⏱️ Tempo Estimado

| Tamanho do Mundo | Tempo Aproximado |
|------------------|------------------|
| < 100 MB | 5-15 segundos |
| 100 MB - 500 MB | 15-60 segundos |
| 500 MB - 1 GB | 1-3 minutos |
| > 1 GB | 3+ minutos |

> Depende da velocidade do seu disco (SSD vs HDD) e quantidade de arquivos.

---

## 📦 O que é Copiado

**Tudo dentro da pasta do mundo:**

```
minecraftWorlds/6LknJ3qXcJo=/
├── levelname.txt           ← Nome do mundo
├── world_icon.jpeg         ← Ícone (se existir)
├── level.dat               ← Dados principais
├── db/                     ← Chunks, entidades, blocos
│   ├── *.ldb
│   └── *.log
├── structures/             ← Estruturas salvas
├── *.mcstructure           ← Arquivos de estrutura
└── ...                     ← Todos os arquivos
```

---

## ✅ Verificar se Deu Certo

Após o backup, você pode:

1.  **No app**: Veja o contador "Backups: 1" e "Último: agora mesmo"
2.  **No Explorer**: Abra `Documentos\MinecraftBackups\backups\{folder_name}\`
3.  **Timestamp**: Pasta nomeada como `2026-06-19_14-30-00`

---

## 🔄 Backup Incremental? (Futuro)

> Atualmente **cada backup é completo** (cópia total).
> Futuro: backup incremental/diferencial para economizar espaço.

---

## 🔗 Próximos Passos

- [Restaurar Mundo →](restore.md)
- [Onde Ficam os Backups →](backup-location.md)
- [Configurações →](settings.md)
