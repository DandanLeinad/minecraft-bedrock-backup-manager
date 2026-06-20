---
icon: lucide/plug
---

# Ports — Interfaces (ABCs)

Contratos abstratos que definem **o que** a aplicação precisa, não **como** faz. Implementações em `infra/repository/`.

---

## WorldRepositoryPort

```python title="src/backup_manager_mvp/core/ports/world_repository.py"
class WorldRepositoryPort(ABC):
    """Contrato para acesso a sistema de arquivos de mundos do Minecraft."""

    @abstractmethod
    def get_worlds_base_path(self) -> Path:
        """Caminho base: %AppData%\\Minecraft Bedrock\\Users\\"""

    @abstractmethod
    def get_uwp_store_path(self) -> Path:
        """Caminho UWP Store: %LocalAppData%\\Packages\\Microsoft.MinecraftUWP_...\\minecraftWorlds"""

    @abstractmethod
    def get_shared_path(self, worlds_base_path: Path) -> Path:
        """Caminho Shared: base_path/../Shared/games/com.mojang/minecraftWorlds"""

    @abstractmethod
    def path_exists(self, path: Path) -> bool:
        """Verifica existência de caminho."""

    @abstractmethod
    def list_directory(self, path: Path) -> list[Path]:
        """Lista itens de um diretório."""

    @abstractmethod
    def is_directory(self, path: Path) -> bool:
        """Verifica se é diretório."""

    @abstractmethod
    def read_text_file(self, path: Path) -> str:
        """Lê arquivo texto UTF-8 (levelname.txt)."""

    @abstractmethod
    def calculate_total_size(self, path: Path) -> int:
        """Tamanho total recursivo em bytes."""
```

**Implementação:** `FileSystemWorldRepository` — usa `pathlib.Path`, `shutil`, `os.walk`.

---

## BackupRepositoryPort

```python title="src/backup_manager_mvp/core/ports/backup_repository.py"
class BackupRepositoryPort(ABC):
    """Contrato para operações de backup no sistema de arquivos."""

    @abstractmethod
    def get_backup_base_path(self) -> Path:
        """Base: %UserProfile%\\Documents\\MinecraftBackups\\backups\\"""

    @abstractmethod
    def ensure_directory(self, path: Path) -> None:
        """Cria diretório se não existe (mkdir -p)."""

    @abstractmethod
    def path_exists(self, path: Path) -> bool:
        """Verifica existência."""

    @abstractmethod
    def delete_tree(self, path: Path) -> None:
        """Remove árvore recursivamente (shutil.rmtree)."""

    @abstractmethod
    def copy_tree(self, source: Path, destination: Path, *, dirs_exist_ok: bool = False) -> None:
        """Copia árvore (shutil.copytree)."""

    @abstractmethod
    def list_directory(self, path: Path) -> list[Path]:
        """Lista itens."""

    @abstractmethod
    def is_directory(self, path: Path) -> bool:
        """Verifica se é diretório."""

    @abstractmethod
    def delete_file(self, path: Path) -> None:
        """Remove arquivo."""

    @abstractmethod
    def copy_file(self, source: Path, destination: Path) -> None:
        """Copia arquivo preservando metadados (shutil.copy2)."""

    @abstractmethod
    def read_tree_stats(self, root: Path) -> tuple[int, int, int]:
        """Retorna (total_files, total_dirs, total_size_bytes)."""

    @abstractmethod
    def read_top_level_items(self, root: Path) -> list[dict[str, int | str]]:
        """Itens nível 1: [{"name": str, "type": "file|dir", "size": int}, ...]"""

    @abstractmethod
    def copy_tree_with_progress(
        self,
        source: Path,
        destination: Path,
        progress_callback: Callable[[int, int], None] | None = None,
        *,
        dirs_exist_ok: bool = False,
    ) -> None:
        """Copia com callback de progresso (current, total) por arquivo."""
```

**Implementação:** `FileSystemBackupRepository` — usa `pathlib`, `shutil`, `os.walk` com callback.

---

## Injeção de Dependência

Services recebem Ports no construtor — **fácil teste com mocks**:

```python title="Produção"
world_repo = FileSystemWorldRepository()
world_service = WorldService(world_repo)

backup_repo = FileSystemBackupRepository()
backup_service = BackupService(backup_repo)
```

```python title="Teste (unitário, sem FS real)"
class MockWorldRepo(WorldRepositoryPort):
    def list_directory(self, path): return [Path("fake_world")]
    def read_text_file(self, path): return "Meu Mundo"
    # ... outros métodos mockados

world_service = WorldService(MockWorldRepo())
worlds = world_service.list_worlds()  # Rápido, determinístico
```

---

## Tabela de Métodos

### WorldRepositoryPort

| Método | Retorno | Descrição |
|--------|---------|-----------|
| `get_worlds_base_path()` | `Path` | `%AppData%\Minecraft Bedrock\Users\` |
| `get_uwp_store_path()` | `Path` | UWP Store minecraftWorlds |
| `get_shared_path(base)` | `Path` | Shared minecraftWorlds |
| `path_exists(path)` | `bool` | Verifica se caminho existe |
| `list_directory(path)` | `list[Path]` | Lista itens do diretório |
| `is_directory(path)` | `bool` | É diretório? |
| `read_text_file(path)` | `str` | Lê levelname.txt (UTF-8) |
| `calculate_total_size(path)` | `int` | Tamanho total em bytes |

### BackupRepositoryPort

| Método | Retorno | Descrição |
|--------|---------|-----------|
| `get_backup_base_path()` | `Path` | `%UserProfile%\Documents\MinecraftBackups\backups\` |
| `ensure_directory(path)` | `None` | Cria diretório (mkdir -p) |
| `path_exists(path)` | `bool` | Verifica existência |
| `delete_tree(path)` | `None` | Remove árvore recursiva |
| `copy_tree(src, dst)` | `None` | Copia árvore |
| `list_directory(path)` | `list[Path]` | Lista itens |
| `is_directory(path)` | `bool` | É diretório? |
| `delete_file(path)` | `None` | Remove arquivo |
| `copy_file(src, dst)` | `None` | Copia arquivo (shutil.copy2) |
| `read_tree_stats(root)` | `tuple[int,int,int]` | (files, dirs, bytes) |
| `read_top_level_items(root)` | `list[dict]` | Itens nível 1 para UI |
| `copy_tree_with_progress(...)` | `None` | Copia com callback progresso |

---

## Estrutura de Pastas (Runtime)

```
%AppData%\Minecraft Bedrock\Users\           ← get_worlds_base_path()
├── {account_id}\
│   └── games\com.mojang\minecraftWorlds\    ← Mundos por conta
│       └── 6LknJ3qXcJo=\                    ← folder_name (12 chars + =)
│           ├── levelname.txt                ← "Meu Mundo Sobrevivência"
│           ├── world_icon.jpeg
│           └── ... (arquivos do mundo)

%LocalAppData%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds\  ← get_uwp_store_path()

%UserProfile%\Documents\MinecraftBackups\backups\  ← get_backup_base_path()
├── 6LknJ3qXcJo=\                            ← folder_name (mesmo do mundo)
│   ├── 2026-06-19_14-30-00\                 ← timestamp
│   │   ├── levelname.txt
│   │   ├── world_icon.jpeg
│   │   └── ... (cópia completa)
│   └── 2026-06-18_10-15-00\
└── abc12345678=\                            ← Outro mundo
```

---

## Testes de Contrato

Testes usam implementações reais com temp dirs:

```python
def test_list_worlds_creates_correct_models(tmp_path):
    repo = FileSystemWorldRepository()
    # Setup: criar estrutura fake em tmp_path
    service = WorldService(repo)
    worlds = service.list_worlds()
    assert len(worlds) == 1
    assert worlds[0].folder_name == "6LknJ3qXcJo="
    assert worlds[0].levelname == "Meu Mundo"
```

---

## Referências

- [Código: world_repository.py](../../src/backup_manager_mvp/core/ports/world_repository.py)
- [Código: backup_repository.py](../../src/backup_manager_mvp/core/ports/backup_repository.py)
- [Código: filesystem_world_repository.py](../../src/backup_manager_mvp/infra/repository/filesystem_world_repository.py)
- [Código: filesystem_backup_repository.py](../../src/backup_manager_mvp/infra/repository/filesystem_backup_repository.py)
- [Models](./models.md) — Models usados pelos Ports
- [Services](./services.md) — Consumidores dos Ports
