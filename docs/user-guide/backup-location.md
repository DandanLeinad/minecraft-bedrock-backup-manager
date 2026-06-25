---
icon: lucide/folder
---

# Onde Ficam os Backups

Localização, estrutura de pastas e como acessar seus backups.

---

## 📁 Localização Padrão

```
%USERPROFILE%\Documents\MinecraftBackups\backups\
```

**Exemplo completo (Windows):**

```
C:\Users\SEU_USUARIO\Documents\MinecraftBackups\backups\
```

---

## 🗂️ Estrutura de Pastas

```
MinecraftBackups/
└── backups/
    ├── 6LknJ3qXcJo=\                    ← folder_name do mundo (UUID Bedrock)
    │   ├── 2026-06-19_14-30-00\         ← Backup 1 (timestamp)
    │   │   ├── levelname.txt
    │   │   ├── world_icon.jpeg
    │   │   ├── level.dat
    │   │   ├── db/
    │   │   └── ... (cópia completa)
    │   ├── 2026-06-18_10-15-00\         ← Backup 2
    │   └── 2026-06-17_08-00-00\         ← Backup 3
    │
    └── abc12345678=\                    ← Outro mundo
        └── 2026-06-19_12-00-00\
```

---

## 🎯 Por que `folder_name` (UUID) e não o nome do mundo?

O Minecraft Bedrock usa **nomes de pasta codificados em base64** (ex: `6LknJ3qXcJo=`) que **não mudam** mesmo se você renomear o mundo no jogo.

| Vantagem | Explicação |
|----------|------------|
| **Persistência** | Renomear mundo no jogo não quebra histórico de backups |
| **Identificação única** | Cada mundo tem ID único global |
| **Restauração correta** | App sabe exatamente qual mundo restaurar |

---

## 📂 Como Acessar Rapidamente

### Via Explorer (Windows)

1.  `Win + E` → Abre Explorer
2.  Na barra de endereço, cole:
    ```
    %USERPROFILE%\Documents\MinecraftBackups\backups
    ```
3.  Enter

### Via Comando (PowerShell)

```powershell
# Abrir no Explorer
explorer "$env:USERPROFILE\Documents\MinecraftBackups\backups"

# Listar backups de um mundo
ls "$env:USERPROFILE\Documents\MinecraftBackups\backups\6LknJ3qXcJo="
```

### Via Terminal (CMD)

```cmd
explorer %USERPROFILE%\Documents\MinecraftBackups\backups
```

---

## 💾 Copiar/Mover Backups

### Para outro disco / backup na nuvem

```powershell
# Copiar pasta completa de backups para OneDrive/Google Drive/etc
Copy-Item -Recurse "$env:USERPROFILE\Documents\MinecraftBackups" "D:\Backups\MinecraftBackups"
```

### Restaurar manualmente (sem o app)

1.  Vá em `Documentos\MinecraftBackups\backups\{folder_name}\{timestamp}\`
2.  Copie **todo o conteúdo** dessa pasta
3.  Cole na pasta do mundo original:
    ```
    %AppData%\Minecraft Bedrock\Users\{account_id}\games\com.mojang\minecraftWorlds\{folder_name}\
    ```
    (Substitua arquivos existentes)

!!! warning "Restauração Manual"
    - Feche o Minecraft antes
    - Faça backup do estado atual primeiro
    - Substitua **todo o conteúdo**, não a pasta pai

---

## 📊 Tamanho Típico

| Tipo de Mundo | Tamanho por Backup |
|---------------|-------------------|
| Novo (vazio) | 1-5 MB |
| Sobrevivência (horas) | 50-200 MB |
| Criativo (grande) | 200 MB - 1 GB |
| Servidor/Realms | 1-5 GB+ |

---

## 🗑️ Limpar Backups Antigos

O app **não apaga backups automaticamente** (por segurança).

### Manual (Explorer)

1.  Abra a pasta de backups
2.  Entre na pasta do mundo (`6LknJ3qXcJo=`)
3.  Delete as pastas de timestamp mais antigas que não precisa

### Via PowerShell (manter últimos 10)

```powershell
$worldId = "6LknJ3qXcJo="
$backupPath = "$env:USERPROFILE\Documents\MinecraftBackups\backups\$worldId"
$keep = 10

Get-ChildItem $backupPath -Directory | Sort-Object Name -Descending | Select-Object -Skip $keep | Remove-Item -Recurse -Force
```

---

## 🔮 Futuro: Caminho Personalizado

> No MVP o caminho é fixo. Versões futuras permitirão configurar:
> - Pasta de backups customizada
> - Múltiplos destinos (local + nuvem)
> - Retenção automática (manter últimos N)

---

## 🔗 Próximos Passos

- [Configurações →](settings.md)
- [FAQ →](faq.md)
- [Troubleshooting →](troubleshooting.md)
