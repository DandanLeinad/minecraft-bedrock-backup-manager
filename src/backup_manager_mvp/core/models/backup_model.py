# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class BackupModel(BaseModel):
    """Modelo de dados para representar um backup de um mundo Minecraft Bedrock.

    Attributes:
        world_folder_name (str): Nome da pasta do mundo (referência ao WorldModel.folder_name).
        world_account_id (str): ID da conta associada ao mundo (referência ao WorldModel.account_id).
        created_at (datetime): Data e hora da criação do backup.
        backup_path (Path): Caminho completo da pasta de backup.

    Raises:
        ValidationError: Se algum campo não passar nas validações Pydantic.
    """

    world_folder_name: str = Field(..., min_length=1)
    world_account_id: str = Field(..., min_length=1)
    created_at: datetime = Field(...)
    backup_path: Path = Field(...)

    @field_validator("world_folder_name", mode="before")
    @classmethod
    def validate_folder_name(cls, value: str) -> str:
        """Valida que world_folder_name não é apenas espaços."""
        if isinstance(value, str) and value.strip() == "":
            raise ValueError("world_folder_name não pode ser apenas espaços em branco")
        return value

    @field_validator("world_account_id", mode="before")
    @classmethod
    def validate_account_id(cls, value: str) -> str:
        """Valida que world_account_id não é apenas espaços."""
        if isinstance(value, str) and value.strip() == "":
            raise ValueError("world_account_id não pode ser apenas espaços em branco")
        return value

    @field_validator("backup_path", mode="before")
    @classmethod
    def validate_backup_path(cls, value: Path) -> Path:
        """Valida que backup_path não é vazio."""
        path_str = str(value).strip()
        if not path_str or path_str == ".":
            raise ValueError("backup_path não pode ser vazio")
        return value

    @property
    def name(self) -> str:
        """Retorna o nome do diretório de backup (timestamp)."""
        return self.backup_path.name

    @property
    def size_display(self) -> str:
        """Retorna o tamanho do backup em formato legível."""
        try:
            total_size = sum(f.stat().st_size for f in self.backup_path.rglob("*") if f.is_file())
            if total_size < 1024:
                return f"{total_size} B"
            elif total_size < 1024 * 1024:
                return f"{total_size / 1024:.2f} KB"
            elif total_size < 1024 * 1024 * 1024:
                return f"{total_size / (1024 * 1024):.2f} MB"
            else:
                return f"{total_size / (1024 * 1024 * 1024):.2f} GB"
        except Exception:
            return "N/A"
