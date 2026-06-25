# Ports & Models — Contratos e Modelos de Domínio

## Ports (Interfaces/Contratos)

Definem **o que** a aplicação precisa, não **como** faz. Implementações em `infra/repository/`.

---

### WorldRepositoryPort

```python
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

### BackupRepositoryPort

```python
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

## Models (Pydantic)

Validação automática, serialização, type hints.

---

### WorldModel

```python
class WorldModel(BaseModel):
    """Mundo Minecraft Bedrock detectado no sistema."""

    folder_name: str = Field(..., min_length=1, max_length=12)
        # Nome da pasta (base64 + padding =) — EX: "6LknJ3qXcJo="
        # Validação: exatamente 12 chars, termina com "="

    levelname: str = Field(..., min_length=1)
        # Nome exibido no jogo — lido de levelname.txt

    world_icon_path: Path | None = Field(default=None)
        # Caminho para world_icon.jpeg (pode não existir)

    path: Path = Field(...)
        # Caminho completo da pasta do mundo
        # Validação: não None, não vazio, não "."

    account_id: str = Field(..., min_length=1)
        # UUID da conta Microsoft ou "UWP-Store" / "Shared"
        # Validação: não apenas whitespace

    version: list[int] = Field(..., min_length=5, max_length=5)
        # lastOpenedWithVersion — 5 inteiros não-negativos
        # EX: [1, 26, 12, 2, 0]
```

**Validadores:**
- `folder_name`: 12 chars + termina com `=`
- `path`, `world_icon_path`: não vazio
- `levelname`, `account_id`: não apenas whitespace
- `version`: lista de 5 ints >= 0

**Uso:** Retornado por `WorldService.list_worlds()`, consumido por `BackupService`.

---

### BackupModel

```python
class BackupModel(BaseModel):
    """Backup de um mundo."""

    world_folder_name: str = Field(..., min_length=1)
        # Referência ao WorldModel.folder_name (UUID Bedrock)
        Permite encontrar backups mesmo se mundo renomeado

    world_account_id: str = Field(..., min_length=1)
        Referência ao WorldModel.account_id

    created_at: datetime = Field(...)
        Timestamp da criação do backup

    backup_path: Path = Field(...)
        Caminho completo da pasta de backup
        Estrutura: backup_base / folder_name / YYYY-MM-DD_HH-MM-SS
```

**Properties:**
```python
@property
def name(self) -> str:
    """Nome do diretório (timestamp)."""
    return self.backup_path.name

@property
def size_display(self) -> str:
    """Tamanho legível: B, KB, MB, GB."""
    # Calcula recursivo via rglob
```

**Uso:** Retornado por `BackupService.create_backup()` e `list_backups()`.

---

### ProgressModel

```python
class ProgressModel(BaseModel):
    """Progresso de operação longa (backup/restore)."""

    current: int = Field(ge=0)
        Itens processados até agora

    total: int = Field(ge=1)
        Total de itens esperados

    stage: str = Field(...)
        Descrição da fase: "Preparando...", "Copiando arquivos...", "Concluído"
```

**Uso:** Callback `progress_callback(ProgressModel)` na UI para barra de progresso.

---

## Injeção de Dependência

Services recebem Ports no construtor — **fácil teste com mocks**:

```python
# Produção
world_repo = FileSystemWorldRepository()
world_service = WorldService(world_repo)

backup_repo = FileSystemBackupRepository()
backup_service = BackupService(backup_repo)

# Teste (unitário, sem FS real)
class MockWorldRepo(WorldRepositoryPort):
    def list_directory(self, path): return [Path("fake_world")]
    def read_text_file(self, path): return "Meu Mundo"
    # ... outros métodos mockados

world_service = WorldService(MockWorldRepo())
worlds = world_service.list_worlds()  # Rápido, determinístico
```

---

## Estrutura de Pastas (Runtime)

```
%AppData%\Minecraft Bedrock\Users\           ← WorldRepositoryPort.get_worlds_base_path()
├── {account_id}\
│   └── games\com.mojang\minecraftWorlds\    ← Mundos por conta
│       └── 6LknJ3qXcJo=\                    ← folder_name (12 chars + =)
│           ├── levelname.txt                ← "Meu Mundo Sobrevivência"
│           ├── world_icon.jpeg
│           └── ... (arquivos do mundo)

%LocalAppData%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds\  ← UWP Store

%UserProfile%\Documents\MinecraftBackups\backups\  ← BackupRepositoryPort.get_backup_base_path()
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

Testes usam implementações reais (`TestFileSystemWorldRepository`) com temp dirs:

```python
# tests/unit/world/test_world_service.py
def test_list_worlds_creates_correct_models(tmp_path):
    repo = FileSystemWorldRepository()  # Real impl
    # Setup: criar estrutura fake em tmp_path
    service = WorldService(repo)
    worlds = service.list_worlds()
    assert len(worlds) == 1
    assert worlds[0].folder_name == "6LknJ3qXcJo="
    assert worlds[0].levelname == "Meu Mundo"
```

---

## Referências

- [Architecture Overview](./overview.md)
- [WorldService](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/core/services/world_service.py) — Uso dos Ports/Models
- [BackupService](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/core/services/backup_service.py) — Uso dos Ports/Models
- [FileSystemWorldRepo](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/infra/repository/filesystem_world_repository.py) — Implementação
- [FileSystemBackupRepo](https://github.com/DandanLeinad/minecraft-bedrock-backup-manager/blob/main/src/backup_manager_mvp/infra/repository/filesystem_backup_repository.py) — Implementação
