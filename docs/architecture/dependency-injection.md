---
icon: lucide/puzzle
---

# Injeção de Dependência (Composition Root)

Como o `BackupManagerApp` monta a aplicação: instancia repositórios, injeta em services, injeta na UI e conecta callbacks.

---

## 🎯 Visão Geral

O `BackupManagerApp` atua como **Composition Root** e **Application Controller**:

```mermaid
flowchart TB
    subgraph ENTRY["Entry Point"]
        MAIN["main.py:83<br/>main()"]
    end

    subgraph APP["BackupManagerApp (Composition Root + App Controller)"]
        INIT["__init__()"]
        DI["Instancia Repositórios<br/>FileSystemWorldRepository<br/>FileSystemBackupRepository"]
        SVCS["Instancia Services<br/>WorldService(repo)<br/>BackupService(repo)"]
        UI["Instancia UI<br/>CustomTkinterUIController(app=self)"]
        WIRE["Conecta Callbacks<br/>UI → App Handlers"]
    end

    subgraph RUNTIME["Runtime"]
        RUN["run() → ui.run()"]
        MAIN_LOOP["CustomTkinter mainloop()"]
    end

    MAIN -->|import / instancia| APP
    APP --> DI
    DI --> SVCS
    SVCS --> UI
    UI --> WIRE
    APP --> RUN
    RUN --> MAIN_LOOP

    classDef entry fill:#1e293b,stroke:#64748b,color:#fff;
    classDef app fill:#312e81,stroke:#6366f1,color:#fff;
    classDef di fill:#065f46,stroke:#10b981,color:#fff;

    class MAIN entry;
    class APP,INIT,WIRE,RUN app;
    class DI,SVCS,UI di;
```

---

## 🔧 Código: main.py (Entry Point)

```python
# main.py:66-83
def main():
    """Função principal - ponto de entrada da aplicação."""
    try:
        _configure_logging()
        logger = logging.getLogger(__name__)

        logger.info("=== Backup Manager Iniciando ===")
        logger.info(f"Log registrado em: {LOG_FILE}")

        app = BackupManagerApp()  # Composition Root
        app.run()                 # Inicia App Controller
    except Exception as e:
        logger.critical(f"Erro crítico ao iniciar: {e}", exc_info=True)


if __name__ == "__main__":
    main()
```

**Responsabilidades do `main.py`:**
1. Configura logging
2. **Instancia o `BackupManagerApp`** (Composition Root)
3. Chama `app.run()` para iniciar o loop

---

## 🏗️ BackupManagerApp.__init__() — Composition Root

```python
# application.py:43-56
def __init__(self):
    """Inicializa a aplicação com serviços e UI."""
    # 1. Instancia Repositórios (Infrastructure)
    self.world_service = WorldService(FileSystemWorldRepository())
    self.backup_service = BackupService(FileSystemBackupRepository())

    # 2. Instancia UI (Adapter)
    self.ui = CustomTkinterUIController(app=self)

    # 3. Conecta Callbacks (UI → App Handlers)
    self.ui.set_callback_world_selected(self._handle_world_selected)
    self.ui.set_callback_create_backup(self._handle_create_backup)
    self.ui.set_callback_restore_backup(self._handle_restore_backup)
    self.ui.set_callback_back(self._handle_back)

    # 4. Estado
    self.current_world: WorldModel | None = None
```

### O que acontece aqui:

| Passo | Código | Padrão |
|-------|--------|--------|
| **1. Repositories** | `FileSystemWorldRepository()` | Instancia adapters concretos |
| **2. Services** | `WorldService(repo)` | Injeta Port no Service (DI manual) |
| **3. UI** | `CustomTkinterUIController(app=self)` | Injeta App Controller na UI (callback registry) |
| **4. Callbacks** | `ui.set_callback_*(self._handle_*)` | Wiring: UI → App Handlers |

---

## 🔄 Injeção de Dependência Manual (DI)

### Service ← Port

```python
# application.py:45-46
self.world_service = WorldService(FileSystemWorldRepository())
self.backup_service = BackupService(FileSystemBackupRepository())
```

**WorldService** recebe `WorldRepositoryPort` (interface):
```python
# world_service.py:34-36
def __init__(self, repository: WorldRepositoryPort):
    self.repository = repository
```

### UI ← App Controller

```python
# application.py:47
self.ui = CustomTkinterUIController(app=self)
```

**UIController** recebe `app` para registrar callbacks:
```python
# customtkinter_ui.py:89-93
def __init__(self, app=None):
    self.app = app
    # ...
```

### Callback Registry (UI → App)

```python
# application.py:50-53
self.ui.set_callback_world_selected(self._handle_world_selected)
self.ui.set_callback_create_backup(self._handle_create_backup)
self.ui.set_callback_restore_backup(self._handle_restore_backup)
self.ui.set_callback_back(self._handle_back)
```

**UIController** expõe setters para callbacks:
```python
# customtkinter_ui.py:440-456
def set_callback_world_selected(self, callback: Callable[[WorldModel], None]) -> None:
    self._callback_world_selected = callback

def set_callback_create_backup(self, callback: Callable[[WorldModel], None]) -> None:
    self._callback_create_backup = callback

def set_callback_restore_backup(self, callback: Callable[[BackupModel, WorldModel], None]) -> None:
    self._callback_restore_backup = callback

def set_callback_back(self, callback: Callable[[], None]) -> None:
    self._callback_back = callback
```

---

## 🔗 Wiring Completo (Diagrama)

```mermaid
flowchart TB
    subgraph COMP["Composition Root (BackupManagerApp.__init__)"]
        REPO_W["FileSystemWorldRepository()"]
        REPO_B["FileSystemBackupRepository()"]
        SVC_W["WorldService(repo_w)"]
        SVC_B["BackupService(repo_b)"]
        UI["CustomTkinterUIController(app=self)"]
    end

    subgraph WIRE["Callback Wiring"]
        CB_W["set_callback_world_selected<br/>→ _handle_world_selected"]
        CB_B["set_callback_create_backup<br/>→ _handle_create_backup"]
        CB_R["set_callback_restore_backup<br/>→ _handle_restore_backup"]
        CB_K["set_callback_back<br/>→ _handle_back"]
    end

    subgraph HANDLERS["App Handlers (Private Methods)"]
        HW["_handle_world_selected(world)"]
        HB["_handle_create_backup(world)"]
        HR["_handle_restore_backup(backup, world)"]
        HK["_handle_back()"]
    end

    REPO_W --> SVC_W
    REPO_B --> SVC_B
    SVC_W --> UI
    SVC_B --> UI
    UI --> CB_W
    UI --> CB_B
    UI --> CB_R
    UI --> CB_K
    CB_W --> HW
    CB_B --> HB
    CB_R --> HR
    CB_K --> HK

    classDef repo fill:#374151,stroke:#9ca3af,color:#fff;
    classDef svc fill:#065f46,stroke:#10b981,color:#fff;
    classDef ui fill:#1e40af,stroke:#3b82f6,color:#fff;
    classDef wire fill:#7c2d12,stroke:#f97316,color:#fff;
    classDef handler fill:#312e81,stroke:#6366f1,color:#fff;

    class REPO_W,REPO_B repo;
    class SVC_W,SVC_B svc;
    class UI ui;
    class CB_W,CB_B,CB_R,CB_K wire;
    class HW,HB,HR,HK handler;
```

---

## 🧵 Thread Management (App Controller)

O `BackupManagerApp` gerencia threads para operações longas:

```python
# application.py:160 - Backup
thread = threading.Thread(target=run_backup, daemon=True)
thread.start()

# application.py:218 - Restore
thread = threading.Thread(target=run_restore, daemon=True)
thread.start()
```

**Padrão:**
- Operações longas (backup/restore) → **Background Thread** (`daemon=True`)
- Progress updates → `main_window.after(0, callback)` → **Main Thread (UI)**
- Thread-safe via `main_window.after(0, callback)`

---

## 📦 Resumo da DI

| Dependência | Tipo | Injetado Em | Via |
|-------------|------|-------------|-----|
| `WorldRepositoryPort` | Interface | `WorldService` | Construtor |
| `BackupRepositoryPort` | Interface | `BackupService` | Construtor |
| `WorldService` | Concreto | `BackupManagerApp` | Atributo |
| `BackupService` | Concreto | `BackupManagerApp` | Atributo |
| `BackupManagerApp` | Concreto | `CustomTkinterUIController` | Construtor (`app=self`) |
| `_handle_*` | Methods | `UIController` | Setters (`set_callback_*`) |

---

## 🎯 Por que DI Manual (sem framework)?

| Vantagem | Explicação |
|----------|------------|
| **Zero dependências** | Não precisa de `injector`, `dependency-injector`, etc. |
| **Explícito** | Fluxo de dependências visível no código |
| **Testável** | Fácil mock: `WorldService(MockWorldRepo())` |
| **Simples** | 45 linhas em `__init__`, fácil de entender |
| **Pythonico** | `__init__` é o local natural para DI em Python |

---

## 🧪 Testabilidade

```python
# Teste unitário - mock do repositório
class MockWorldRepo(WorldRepositoryPort):
    def list_directory(self, path): return [Path("fake_world")]
    def read_text_file(self, path): return "Mundo Teste"
    # ... outros métodos

# Instancia service com mock
world_service = WorldService(MockWorldRepo())
worlds = world_service.list_worlds()  # Rápido, sem FS real
```

---

## 📚 Referências

- [Código: main.py](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/main.py) — Entry Point
- [Código: application.py](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/application.py) — Composition Root + App Controller
- [Código: world_service.py](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/core/services/world_service.py) — Service com Port
- [Código: customtkinter_ui.py](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/ui/customtkinter/customtkinter_ui.py) — UI com Callback Registry
- [Request Flow](./request-flow.md) — Como as requisições percorrem o sistema
- [Request Flow - Threading](./request-flow.md#3-threading-model) — Threading Model
