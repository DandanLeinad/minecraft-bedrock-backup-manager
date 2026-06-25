# Arquitetura do Minecraft Bedrock Backup Manager

## Visão Geral

Aplicação desktop Windows para gerenciar backups de mundos Minecraft Bedrock Edition. Segue arquitetura **Ports & Adapters (Hexagonal)** com separação clara entre domínio, aplicação e infraestrutura.

```
┌─────────────────────────────────────────────────────────────────┐
│                        UI (CustomTkinter)                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │ Worlds List     │  │ World Details   │  │ Restore Flow   │  │
│  └────────┬────────┘  └────────┬────────┘  └───────┬────────┘  │
└───────────┼────────────────────┼────────────────────┼───────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                          │
│  ┌──────────────────────┐  ┌────────────────────────────────┐  │
│  │ WorldService         │  │ BackupService                  │  │
│  │ - list_worlds()      │  │ - create_backup()              │  │
│  │ - get_metadata()     │  │ - list_backups()               │  │
│  │ - get_levelname()    │  │ - restore_backup()             │  │
│  └──────────┬───────────┘  └──────────────┬────────────────┘  │
└─────────────┼─────────────────────────────┼────────────────────┘
              │                             │
              ▼                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Domain Layer                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ WorldModel       │  │ BackupModel      │  │ ProgressModel│  │
│  │ (Pydantic)       │  │ (Pydantic)       │  │ (Pydantic)   │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────┘
              │                             │
              ▼                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Ports (Interfaces)                         │
│  ┌──────────────────────┐  ┌────────────────────────────────┐  │
│  │ WorldRepositoryPort  │  │ BackupRepositoryPort           │  │
│  │ (ABC)                │  │ (ABC)                          │  │
│  └──────────┬───────────┘  └──────────────┬────────────────┘  │
└─────────────┼─────────────────────────────┼────────────────────┘
              │                             │
              ▼                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                         │
│  ┌──────────────────────┐  ┌────────────────────────────────┐  │
│  │ FileSystemWorldRepo  │  │ FileSystemBackupRepo           │  │
│  │ (impl)               │  │ (impl)                         │  │
│  └──────────────────────┘  └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Camadas

### 1. Domain (`core/models/`)
Modelos de dados puros com validação Pydantic:
- `WorldModel`: Representa um mundo (folder_name 12 chars + "=", levelname, path, account_id, version com 5 ints)
- `BackupModel`: Representa um backup (world_folder_name, world_account_id, created_at, backup_path)
- `ProgressModel`: Progresso de operações (current, total, stage)

### 2. Ports (`core/ports/`)
Interfaces abstratas (ABC) - definem **contratos**, não implementação:
- **WorldRepositoryPort**: Operações de leitura do FS de mundos (listar, ler levelname.txt, calcular tamanho)
- **BackupRepositoryPort**: Operações de backup no FS (copiar árvore, listar, deletar, progresso)

### 3. Services (`core/services/`)
Lógica de negócio, **sem dependência de UI ou FS concreto**:
- **WorldService**: Descoberta de mundos em 3 fontes (contas normais, UWP Store, Shared), metadados
- **BackupService**: Criação/restauração de backups com progresso, preview, listagem ordenada
- **ProgressService**: Gerenciamento de callbacks de progresso

### 4. Infrastructure (`infra/repository/`)
Implementações concretas dos Ports usando `pathlib`, `shutil`:
- **FileSystemWorldRepository**: Implementa WorldRepositoryPort
- **FileSystemBackupRepository**: Implementa BackupRepositoryPort

### 5. UI (`ui/customtkinter/`)
CustomTkinter (Windows 10/11):
- **Screens**: WorldsList, WorldDetails, RestorePreview, RestoreConfirmation
- **Handlers**: Separação de lógica de UI (navigation, backup, restore, world)
- **Components**: Botões, frames, labels, dialogs reutilizáveis
- **Theme**: Tema customizado, ícones, loading states

## Fluxo Principal

### Listar Mundos
```
UI → WorldService.list_worlds()
         │
         ├─► FileSystemWorldRepo.get_worlds_base_path()
         ├─► FileSystemWorldRepo.get_uwp_store_path()
         ├─► FileSystemWorldRepo.get_shared_path()
         │
         └─► Para cada source: _list_worlds_from_path()
                 │
                 ├─► FileSystemWorldRepo.list_directory()
                 ├─► FileSystemWorldRepo.read_text_file(levelname.txt)
                 └─► WorldModel(folder_name, levelname, path, account_id, version)
```

### Criar Backup
```
UI → BackupService.create_backup(world, progress_callback)
         │
         ├─► timestamp = now()
         ├─► backup_path = backup_base / folder_name / timestamp
         ├─► FileSystemBackupRepo.ensure_directory()
         ├─► FileSystemBackupRepo.copy_tree_with_progress(world.path, backup_path)
         │       └─► progress_callback(ProgressModel)
         └─► BackupModel(world_folder_name, world_account_id, created_at, backup_path)
```

### Restaurar Backup
```
UI → BackupService.restore_backup(backup, world, progress_callback)
         │
         ├─► FileSystemBackupRepo.delete_tree(world.path contents)
         ├─► FileSystemBackupRepo.copy_tree_with_progress(backup.backup_path, world.path)
         │       └─► progress_callback(ProgressModel)
         └─► Concluído
```

## Padrões Utilizados

| Padrão | Onde | Benefício |
|--------|------|-----------|
| **Ports & Adapters** | core/ports + infra/repository | Testável, desacoplado, trocável |
| **Dependency Injection** | Services recebem Port no `__init__` | Fácil mock em testes |
| **Repository Pattern** | Ports abstraem FS | Isola lógica de domínio |
| **Feature Flags** | config/feature_flags.py | Integração contínua segura |
| **Progress Callback** | BackupService + UI | UX responsiva em operações longas |

## Tecnologias

| Camada | Stack |
|--------|-------|
| Linguagem | Python 3.14+ |
| UI | CustomTkinter 5.2+ |
| Validação | Pydantic 2.13+ |
| Testes | pytest 9+, pytest-cov |
| Lint/Format | Ruff 0.15+ |
| Types | Pyright 1.1+ |
| Build | PyInstaller 6.21+ |
| Versionamento | Commitizen (Conventional Commits) |
| Docs | Zensical (MkDocs-based) |

## Pontos de Extensão

1. **Novo storage**: Implementar `WorldRepositoryPort` / `BackupRepositoryPort` (ex: cloud, zip)
2. **Nova UI**: Implementar `ui/base.py` interface (ex: Tauri/React futuro)
3. **Nova feature**: Service + Port + Model + Feature Flag
4. **Nova plataforma**: Apenas trocar `infra/repository` (lógica de domínio inalterada)

## Referências

- [Ports & Models](./ports-and-models.md) — Detalhes de contratos e modelos
- [Fluxo de Requisição](./request-flow.md) — Backup/Restore Flow, Threading, Feature Flags
- [Injeção de Dependência](./dependency-injection.md) — Composition Root, DI Manual, Callback Wiring
- [ADR 0001](../decisions/0001-python-now-rust-tauri-future.md) — Decisão de tecnologia
- [Development Setup](../getting-started/usage.md) — Como rodar localmente
