---
icon: lucide/download
---

# Instalação

Como baixar, instalar e executar o Minecraft Bedrock Backup Manager.

---

## 📥 Baixar

1.  Acesse a [página de Releases](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/releases/latest)
2.  Baixe o arquivo `MinecraftBedrockBackupManager.exe` (versão mais recente)
3.  O arquivo tem aproximadamente **5 MB**

!!! tip "Verificação de Integridade"
    Verifique o hash SHA256 na página de releases para garantir que o arquivo não foi corrompido ou modificado.

---

## 🛡️ Antivírus / SmartScreen

Como o executável não é assinado digitalmente (certificado custa $$), o Windows Defender ou SmartScreen podem avisar:

=== "Windows Defender SmartScreen"
    1.  Clique em **Mais informações**
    2.  Clique em **Executar mesmo assim**

=== "Antivírus de terceiros"
    Adicione uma exceção para a pasta onde salvou o `.exe` ou desative temporariamente durante a primeira execução.

!!! warning "Falso Positivo"
    Isso é comum em projetos open source sem certificado de assinatura (code signing). O código é público e auditável no [GitHub](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager).

---

## ▶️ Executar

!!! info "Sem Instalação Necessária"
    O app é **portátil** — basta dar dois cliques no `.exe` para rodar. Não há instalador, não modifica o registro do Windows.

### Opções de Execução

| Método | Descrição |
|--------|-----------|
| **Duplo clique** | Execução normal (sem console) |
| **Terminal** | `.\MinecraftBedrockBackupManager.exe` — vê logs no terminal |
| **Atalho** | Crie atalho na Área de Trabalho ou Menu Iniciar |

---

## ✅ Primeiro Uso

Ao abrir pela primeira vez:

1.  O app escaneia automaticamente por mundos Minecraft Bedrock
2.  Lista todos os mundos encontrados (contas Microsoft, UWP Store, Shared)
3.  Selecione um mundo na lista lateral
4.  Clique em **"Fazer Backup"**

---

## 📋 Requisitos do Sistema

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| **SO** | Windows 10 (1903+) | Windows 11 |
| **Arquitetura** | x64 | x64 |
| **RAM** | 100 MB livres | 500 MB livres |
| **Disco** | 50 MB para o app | 1 GB+ para backups |
| **Minecraft** | Bedrock Edition instalado | Última versão |

---

## 🔧 Portátil vs Instalado

| Aspecto | Portátil (.exe) | Instalado (futuro) |
|---------|-----------------|-------------------|
| **Instalação** | Nenhuma | Instalador (MSI/EXE) |
| **Atualizações** | Manual (baixar novo) | Auto-update (Tauri futuro) |
| **Dados** | `Documentos\MinecraftBackups` | Mesmo |
| **Configuração** | Feature flags (env vars) | Arquivo config + UI |

---

## 🗑️ Desinstalar

Simplesmente **delete o arquivo `.exe`** e a pasta de backups (se quiser remover tudo):

```powershell
# Remover app
del MinecraftBedrockBackupManager.exe

# Remover backups (CUIDADO: apaga TODOS os backups!)
Remove-Item -Recurse -Force "$env:USERPROFILE\Documents\MinecraftBackups"
```

---

## 🔗 Próximos Passos

- [Primeiro Backup →](first-backup.md)
- [Onde Ficam os Backups →](backup-location.md)
- [Troubleshooting →](troubleshooting.md)
