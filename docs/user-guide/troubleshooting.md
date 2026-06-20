---
icon: lucide/alert-triangle
---

# Troubleshooting

Soluções para problemas comuns.

---

## 🚫 App Não Abre / Crash Imediato

### Sintoma
Duplo clique no `.exe` → nada acontece / janela fecha instantaneamente.

### Causas Comuns

| Causa | Solução |
|-------|---------|
| **Antivírus bloqueando** | Adicione exceção para o `.exe` ou pasta |
| **Windows SmartScreen** | "Mais informações" → "Executar mesmo assim" |
| **Arquivo corrompido** | Baixe novamente da [página de releases](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/releases/latest) |
| **Faltando VC++ Redist** | Instale [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) |

### Debug via Terminal

```powershell
# Execute no PowerShell para ver erro
.\MinecraftBedrockBackupManager.exe
```

---

## 🔍 Mundos Não Aparecem / Lista Vazia

### Sintoma
App abre mas lista de mundos está vazia.

### Verificações

1.  **Minecraft Bedrock instalado?** Precisa ter pelo menos um mundo criado no jogo.
2.  **Versão do Minecraft?** App suporta Bedrock 1.19+ (pasta `minecraftWorlds`).
3.  **Permissões de pasta?** App precisa ler `%AppData%` e `%LocalAppData%`.

### Forçar Re-detecção

```powershell
# Feche o app completamente
# Reabra - ele faz scan automático ao iniciar
```

### Caminhos Verificados pelo App

```
%AppData%\Minecraft Bedrock\Users\{account_id}\games\com.mojang\minecraftWorlds\
%LocalAppData%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds\
%AppData%\Minecraft Bedrock\Users\Shared\games\com.mojang\minecraftWorlds\
```

---

## 💾 Backup Falha / Erro

### Erro: "Permission denied" / "Access denied"

| Causa | Solução |
|-------|---------|
| **Antivírus** | Desative temporariamente / adicione exceção |
| **Pasta só leitura** | Botão direito → Propriedades → Desmarque "Somente leitura" |
| **Arquivo em uso** | Feche Minecraft completamente (inclui tray) |
| **Disco cheio** | Libere espaço |

### Erro: "Backup path not found"

-   Pasta `Documentos\MinecraftBackups` não existe → App cria automaticamente
-   Se deletou manualmente, reabra o app

### Erro: "levelname.txt not found"

-   Pasta do mundo corrompida/incompleta
-   Tente reparar no Minecraft ou delete o mundo problemático

---

## 🔄 Restauração Falha

### Erro: "World not found" / "Backup not found"

-   Caminho do mundo ou backup foi movido/deletado fora do app
-   Reinicie o app para re-escanear

### Erro: "Permission denied" durante restauração

-   Antivírus bloqueando escrita na pasta do Minecraft
-   Pasta `minecraftWorlds` ou pai está como somente leitura

### Mundo não aparece no Minecraft após restaurar

1.  Feche e reabra o Minecraft Bedrock
2.  Verifique se o mundo está na lista "Meus Mundos"
3.  Se não, verifique se a pasta tem `levelname.txt` e `level.dat`

---

## ⚡ Performance / Lento

### Backup muito demorado

| Fator | Impacto | Melhoria |
|-------|---------|----------|
| **HDD vs SSD** | Alto | Use SSD |
| **Muitos arquivos pequenos** | Médio | Normal no Bedrock (milhares de `.ldb`) |
| **Antivírus escaneando** | Alto | Adicione exceção |
| **Mundo > 1 GB** | Médio | Paciência / futuro: multi-threading |

### App travando durante backup

-   Normal em mundos grandes — a UI pode parecer congelada mas o backup continua em background
-   Ative `FF_ADVANCED_LOGGING=true` para ver progresso no terminal

---

## 📋 Coletar Logs para Reportar Bug

### Via Terminal (Recomendado)

```powershell
# Logs detalhados
$env:BACKUP_MANAGER_LOG_LEVEL = "DEBUG"
$env:FF_ADVANCED_LOGGING = "true"
.\MinecraftBedrockBackupManager.exe
```

### Copie a saída do terminal e anexe no [GitHub Issue](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/issues/new).

---

## 📋 Checklist Antes de Reportar Bug

- [ ] Testou na versão mais recente? ([Releases](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/releases/latest))
- [ ] Fez backup manual dos mundos importantes antes?
- [ ] Testou com antivírus desativado?
- [ ] Minecraft estava **fechado** durante backup/restauração?
- [ ] Incluiu logs de erro (terminal com `DEBUG`)?
- [ ] Descreveu passos para reproduzir?
- [ ] Incluiu: Windows version, Minecraft version, tamanho do mundo?

---

## 🔗 Links Úteis

| Recurso | Link |
|---------|------|
| **Reportar Bug** | [GitHub Issues](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/issues/new) |
| **FAQ** | [FAQ](./faq.md) |
| **Changelog** | [CHANGELOG.md](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/CHANGELOG.md) |
| **Discussões** | [GitHub Discussions](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/discussions) |

---

## 🔗 Próximos Passos

- [FAQ →](./faq.md)
- [Configurações →](./settings.md)
- [Instalação →](./installation.md)
