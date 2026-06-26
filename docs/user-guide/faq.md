---
icon: lucide/help-circle
---

# FAQ — Perguntas Frequentes

Respostas para as dúvidas mais comuns.

---

## 🎮 Uso Geral

### O app funciona com Minecraft Java Edition?

**Não.** Apenas **Minecraft Bedrock Edition** (Windows 10/11, Microsoft Store). Java Edition tem estrutura de mundos diferente.

### Funciona com Realms / Servidores dedicados?

**Backups locais apenas.** O app faz backup dos mundos salvos **no seu computador**. Realms e servidores dedicados não são acessíveis localmente.

### Precisa ter o Minecraft aberto para fazer backup?

**Não.** O app lê os arquivos direto do disco. O Minecraft deve estar **fechado** para garantir consistência (evita arquivos travados).

### O app modifica meus mundos originais?

**Não ao fazer backup.** Apenas **copia** os arquivos.
**Sim ao restaurar.** Restauração **sobrescreve** o mundo atual — por isso faça backup antes!

---

## 💾 Backups

### Quantos backups posso ter?

**Ilimitados** (limitado pelo espaço em disco). Cada backup é uma cópia completa.

### Posso apagar backups antigos manualmente?

**Sim.** Vá em `Documentos\MinecraftBackups\backups\{world_id}\` e delete as pastas de timestamp que não quer mais. O app não apaga nada automaticamente.

### Backups são comprimidos (zip)?

**Não no MVP.** São cópias diretas dos arquivos. Futuro: compressão opcional (zstd/lz4).

### Posso mover a pasta de backups para outro disco?

**Sim.** Copie a pasta `MinecraftBackups` inteira. Para restaurar, o app procura no local padrão — você precisaria copiar de volta ou restaurar manualmente.

---

## 🔄 Restauração

### Restaurar apaga o backup?

**Não.** O backup original permanece intacto. Pode restaurar quantas vezes quiser.

### E se eu restaurar o backup errado?

Faça um **backup do estado atual** *antes* de restaurar (se tiver progresso novo). Depois restaure o backup correto.

### O mundo some da lista após restaurar?

**Não.** O mundo continua na lista. Apenas o conteúdo da pasta foi substituído.

---

## 🖥️ Compatibilidade

### Windows 7 / 8.1?

**Não suportado.** Requer Windows 10 (build 1903+) ou Windows 11.

### Linux / macOS / Steam Deck?

**Não no MVP.** Python + CustomTkinter é Windows-only (caminhos `%AppData%`, `%LocalAppData%`).
**Futuro:** Rust + Tauri será cross-platform.

### ARM64 (Snapdragon, etc.)?

**Não testado.** Build atual é x64. Pode rodar via emulação x64 no Windows on ARM.

---

## 🛡️ Segurança / Antivírus

### Meu antivírus bloqueia / alerta

**Falso positivo comum.** O `.exe` não é assinado digitalmente (certificado custa $200-400/ano).
-   Código 100% open source: [GitHub](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager)
-   Build reprodutível via PyInstaller
-   Adicione exceção no seu AV

### O app envia dados para internet?

**Não.** Zero telemetria, zero conexões de rede (exceto se ativar `FF_CLOUD_SYNC` futuramente). Funciona 100% offline.

---

## 🐛 Problemas Conhecidos

| Problema | Status | Workaround |
|----------|--------|------------|
| Mundos com caracteres especiais no nome | Conhecido | Funciona, mas preview pode mostrar errado |
| Backup muito lento em HDD | Conhecido | Use SSD ou aguarde |
| App não detecta mundo recém-criado | Ocasional | Reinicie o app |
| Restauração falha "permission denied" | Antivírus | Desative AV temporariamente |

---

## 🤝 Contribuir / Reportar Bug

| Ação | Link |
|------|------|
| **Reportar bug** | [GitHub Issues](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/issues) |
| **Sugerir feature** | [GitHub Discussions](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/discussions) |
| **Ver código** | [GitHub Repo](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager) |
| **Changelog** | [CHANGELOG.md](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/CHANGELOG.md) |

---

## 🔗 Próximos Passos

- [Troubleshooting →](./troubleshooting.md)
- [Instalação →](./installation.md)
- [Desenvolvimento →](../development/index.md)
