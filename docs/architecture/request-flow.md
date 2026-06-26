---
icon: lucide/arrow-right-left
---

# Fluxo de Requisição

Detalhamento de como as operações de **Backup** e **Restore** percorrem o sistema, incluindo threading, callbacks de progresso e feature flags.

---

## 🎯 Visão Geral

Este documento complementa a [Visão Arquitetural](../index.md#arquitetura-em-resumo) mostrando o fluxo de execução real de uma requisição.

```mermaid
flowchart TB
    subgraph USER["User Action"]
        CLICK["Clique no Botão"]
    end

    subgraph UI_LAYER["UI Layer (CustomTkinter)"]
        BTN["Botão: Fazer Backup / Restaurar"]
        SCR["Screen Handler"]
        HND["Handler (thin wrapper)"]
        UIUP["UI Update"]
    end

    subgraph APP_LAYER["Application Controller"]
        APP_NODE["BackupManagerApp"]
        CB["Callback Registry"]
    end

    subgraph THREAD["Background Thread"]
        THR["threading.Thread (daemon=True)"]
        SVC["Service"]
        PORT["Repository Port"]
        REPO["FileSystem Repository"]
    end

    subgraph PROGRESS["Progress Tracking"]
        PC["Progress Callback"]
        AFTER["main_window.after()"]
    end

    CLICK --> BTN
    BTN --> SCR
    SCR --> HND
    HND --> APP_NODE
    APP_NODE --> CB
    CB --> THR
    THR --> SVC
    SVC --> PORT
    PORT --> REPO
    REPO -->|Progress| PC
    PC --> AFTER
    AFTER --> UIUP
    UIUP --> BTN

    classDef user fill:#1e293b,stroke:#64748b,color:#fff
    classDef ui fill:#1e40af,stroke:#3b82f6,color:#fff
    classDef app fill:#312e81,stroke:#6366f1,color:#fff
    classDef thread fill:#7c2d12,stroke:#f97316,color:#fff
    classDef prog fill:#065f46,stroke:#10b981,color:#fff

    class CLICK user
    class BTN,SCR,HND,UIUP ui
    class APP_NODE,CB app
    class THR,SVC,PORT,REPO thread
    class PC,AFTER prog
```

---

## 1️⃣ Backup Flow

```mermaid
sequenceDiagram
    actor U as User
    participant UI as CustomTkinter UI
    participant H as Backup Handler
    participant A as BackupManagerApp
    participant TH as threading.Thread
    participant BS as BackupService
    participant BR as BackupRepositoryPort
    participant FR as FileSystemBackupRepo
    participant PC as Progress Callback
    participant MW as main_window.after()

    U->>UI: Clica "Fazer Backup"
    UI->>H: on_create_backup(world)
    H->>A: _handle_create_backup(world)
    A->>A: show_progress_bar() / disable_buttons()
    A->>TH: threading.Thread(target=run_backup)
    TH->>BS: create_backup(world, progress_callback)
    BS->>FR: copy_tree_with_progress(world.path, backup_path)
    FR-->>BS: (current, total) por arquivo
    BS->>PC: ProgressModel(current, total, stage)
    PC->>MW: main_window.after(0, ui.update_progress)
    MW->>UI: UI Thread: update_progress()
    BS-->>TH: BackupModel
    TH->>A: on_success() via main_window.after()
    A->>UI: show_info_dialog + show_screen_world_details
```

### Pontos-Chave

| Etapa | Código | Responsabilidade |
|-------|--------|------------------|
| **Threading** | `application.py:160` | `threading.Thread(target=run_backup, daemon=True)` |
| **Progress** | `backup_service.py:119` | `copy_tree_with_progress()` chama callback `(current, total)` |
| **Thread-Safety** | `application.py:119` | `main_window.after(0, lambda: ui.update_progress(progress))` |
| **Model** | `backup_service.py:143` | Retorna `BackupModel` com `created_at`, `backup_path`, `size_display` |

---

## 2️⃣ Restore Flow (com Feature Flag)

```mermaid
sequenceDiagram
    actor U as User
    participant UI as CustomTkinter UI
    participant H as Restore Handler
    participant A as BackupManagerApp
    participant TH as threading.Thread
    participant BS as BackupService
    participant BR as BackupRepositoryPort
    participant FR as FileSystemBackupRepo
    participant PC as Progress Callback
    participant MW as main_window.after()

    U->>UI: Clica "Restaurar" em backup
    UI->>H: on_restore_backup(backup, world)

    alt FF_RESTORE_PREVIEW = true
        H->>A: _handle_restore_backup(backup, world)
        A->>BS: get_backup_preview_info(backup)
        BS-->>A: preview_info (files, dirs, size, top_items)
        A->>UI: show_screen_restore_preview(world, backup, preview_info)
        U->>UI: Confirma no Preview
        UI->>H: on_restore_backup(backup, world)
    else
        H->>A: _handle_restore_backup(backup, world)
    end

    Note right of UI: FF_RESTORE_PREVIEW padrão é true

    A->>A: show_progress_bar() / disable_buttons()
    A->>TH: threading.Thread(target=run_restore)
    TH->>BS: restore_backup(backup, world, progress_callback)
    BS->>FR: delete_tree(world.path) + copy_tree_with_progress()
    FR-->>BS: (current, total) por arquivo
    BS->>PC: ProgressModel(current, total, stage)
    PC->>MW: main_window.after(0, ui.update_progress)
    MW->>UI: UI Thread: update_progress()
    BS-->>TH: Concluído
    TH->>A: on_success() via main_window.after()
    A->>UI: show_info_dialog + show_screen_world_details(world, backups)
```

### Branch da Feature Flag

```mermaid
flowchart TD
    RESTORE[Restaurar Clicado] --> FLAG{FF_RESTORE_PREVIEW?}
    FLAG -->|true (padrão)| PREVIEW[show_screen_restore_preview]
    FLAG -->|false| DIRECT[Direct Restore]
    PREVIEW --> CONFIRM{Usuário Confirma?}
    CONFIRM -->|Sim| DIRECT
    CONFIRM -->|Não| CANCEL[Cancelar]
    DIRECT --> THREAD[threading.Thread]
    THREAD --> RESTORE_SVC[BackupService.restore_backup]
    RESTORE_SVC --> REPO[FileSystemBackupRepo]
    REPO --> PROG[Progress Callback]
    PROG --> AFTER[main_window.after]
    AFTER --> UI[UI Update]
```

### Estados da Feature Flag

| Flag | Valor | Comportamento |
|------|-------|---------------|
| `FF_RESTORE_PREVIEW` | `true` (padrão) | Preview → Confirmação → Executa |
| `FF_RESTORE_PREVIEW` | `false` | Restore direto → Confirmação → Executa |

---

## 3️⃣ Threading Model

```mermaid
flowchart LR
    subgraph MAIN["Main Thread (UI)"]
        UI[CustomTkinter Event Loop]
        MW[main_window]
        AFTER["after(0, callback)"]
    end

    subgraph BG["Background Thread"]
        TH["threading.Thread<br/>daemon=True"]
        SVC["Service.run_*()"]
        REPO[Repository.copy_tree_with_progress]
    end

    subgraph PROG["Progress Pipeline"]
        CB["ProgressModel<br/>(current, total, stage)"]
        AFTER2["after(0, ...)"]
    end

    UI -->|click| TH
    TH -->|ProgressModel| CB
    CB -->|"after(0, lambda)"| AFTER
    AFTER -->|schedule| UI
    UI -.->|update_progress| UI

    classDef main fill:#1e40af,stroke:#3b82f6,color:#fff;
    classDef bg fill:#7c2d12,stroke:#f97316,color:#fff;
    classDef prog fill:#065f46,stroke:#10b981,color:#fff;

    class UI,MW,AFTER main;
    class TH,SVC,REPO bg;
    class CB,AFTER2 prog;
```

### Padrão Thread-Safe

```python
# Em BackupManagerApp._handle_create_backup()
def on_progress(progress: ProgressModel) -> None:
    if self.ui.main_window:
        self.ui.main_window.after(0, lambda: self.ui.update_progress(progress))

# Service chama callback vindo do Repository
self.repository.copy_tree_with_progress(
    world.path, backup_path,
    progress_callback=internal_callback  # recebe (current, total)
)
```

### Regras de Ouro

| Regra | Código | Por quê |
|-------|--------|---------|
| **UI só na Main Thread** | `main_window.after(0, ...)` | CustomTkinter/Tkinter não é thread-safe |
| **Background = daemon** | `threading.Thread(daemon=True)` | Não bloqueia encerramento do app |
| **Progress = DTO** | `ProgressModel(current, total, stage)` | Imutável, serializável, thread-safe |
| **Callbacks via after()** | `main_window.after(0, callback)` | Agenda na event loop da UI |

---

## 4️⃣ Feature Flags Flow

```mermaid
flowchart TD
    START[App Inicia] --> LOAD[Carrega feature_flags.py]
    LOAD --> PARSE["os.getenv('FF_*', defaults)"]

    PARSE --> ICON[FF_WORLD_ICON_PREVIEW]
    PARSE --> PREVIEW[FF_RESTORE_PREVIEW]
    PARSE --> MT[FF_MULTI_THREADING]
    PARSE --> LOG[FF_ADVANCED_LOGGING]

    ICON -->|true (padrão)| ICON_ON[World Icon Preview ativo]
    PREVIEW -->|true (padrão)| PREVIEW_ON[Restore com Preview]
    MT -->|true| MT_ON[Threading experimental]
    LOG -->|true| LOG_ON[Debug verbose]

    classDef flag fill:#1e40af,stroke:#3b82f6,color:#fff;
    classDef on fill:#065f46,stroke:#10b981,color:#fff;

    class ICON,PREVIEW,MT,LOG flag;
    class ICON_ON,PREVIEW_ON,MT_ON,LOG_ON on;
```

### Tabela de Flags

| Flag | Env Var | Padrão | Status | Descrição |
|------|---------|--------|--------|-----------|
| World Icon Preview | `FF_WORLD_ICON_PREVIEW` | `true` | ✅ Ativo | Preview de ícone do mundo na lista |
| Restore Preview | `FF_RESTORE_PREVIEW` | `true` | ✅ Ativo | Preview antes de restaurar |
| Multi-threading | `FF_MULTI_THREADING` | `false` | ⚡ Experimental | Operações paralelas |
| Advanced Logging | `FF_ADVANCED_LOGGING` | `false` | ⚡ Experimental | Logs verbosos |

### Uso

```bash
# Desenvolvimento - ativar experimentais
FF_MULTI_THREADING=true FF_ADVANCED_LOGGING=true uv run task dev

# Testes CI - desativar previews se necessário
FF_WORLD_ICON_PREVIEW=false FF_RESTORE_PREVIEW=false uv run task test
```

---

## 5️⃣ Referências de Código

| Fluxo | Arquivo | Função/Classe |
|-------|---------|---------------|
| **Backup** | `application.py:105` | `_handle_create_backup()` |
| **Backup Thread** | `application.py:160` | `threading.Thread(target=run_backup)` |
| **Progress Callback** | `application.py:117` | `on_progress()` + `main_window.after()` |
| **Service Backup** | `backup_service.py:64` | `create_backup()` |
| **Repo Copy** | `backup_repository.py:72` | `copy_tree_with_progress()` |
| **Restore** | `application.py:163` | `_handle_restore_backup()` |
| **Restore Thread** | `application.py:218` | `threading.Thread(target=run_restore)` |
| **Feature Flag** | `feature_flags.py` | `FEATURE_FLAGS.ENABLE_RESTORE_PREVIEW` |
| **Preview** | `backup_service.py:278` | `get_backup_preview_info()` |
| **UI Progress** | `customtkinter_ui.py:411` | `update_progress()` |

---

## 📚 Leituras Relacionadas

- [Visão Arquitetural](../index.md#arquitetura-em-resumo) — Diagrama 1
- [Dependency Injection](./dependency-injection.md) — Diagrama 3
- [Feature Flags Guide](../development/feature-flags.md)
- [Código: application.py](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/application.py)
- [Código: backup_service.py](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/core/services/backup_service.py)
- [Código: customtkinter_ui.py](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/ui/customtkinter/customtkinter_ui.py)
