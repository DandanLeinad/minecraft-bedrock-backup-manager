# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class WorldModel(BaseModel):
    """Modelo de dados para representar um mundo do Minecraft Bedrock Edition.

    Attributes:
        folder_name (str): Nome da pasta do mundo (obrigatório, min 1 caractere).
        levelname (str): Nome do mundo exibido no jogo (obrigatório, min 1 caractere).
        world_icon_path (Path): Caminho para a imagem do mundo (world_icon.jpeg).
        path (Path): Caminho completo para a pasta do mundo. Rejeita None, vazio ou ".".
        account_id (str): ID da conta Microsoft (obrigatório, min 1 caractere).
        version (list[int]): Versão do mundo - exatamente 5 inteiros (ex: [1, 26, 12, 2, 0]).

    Raises:
        ValidationError: Se algum campo não passar nas validações Pydantic.
    """

    folder_name: str = Field(..., min_length=1, max_length=12)  # Nome da pasta do mundo
    levelname: str = Field(..., min_length=1)  # Nome do mundo exibido no jogo
    world_icon_path: Path | None = Field(
        default=None
    )  # Caminho para a imagem do mundo (pode ser None se a feature estiver desativada)
    path: Path = Field(...)  # Caminho completo para a pasta do mundo
    account_id: str = Field(..., min_length=1)  # ID da conta da Microsoft associada ao mundo
    version: list[int] = Field(
        ..., min_length=5, max_length=5
    )  # Versão do Mundo (lastOpenedWithVersion)

    @field_validator("path", "world_icon_path", mode="before")
    @classmethod
    def validate_path_not_empty(cls, validate):
        """Valida que o campo path não é None, vazio ou inválido."""
        if validate is None:
            raise ValueError("path não pode ser None")
        # Verifica se é string vazia ou Path inválido
        path_str = str(validate).strip()
        if not path_str or path_str == ".":
            raise ValueError("path não pode ser vazio")
        return validate

    @field_validator("folder_name", mode="before")
    @classmethod
    def validate_folder_name_format(cls, value):
        """Valida que folder_name tem 12 caracteres, termina com = e não é apenas espaços."""
        if isinstance(value, str):
            # Verifica whitespace-only PRIMEIRO (antes de validar comprimento)
            if value.strip() == "":
                raise ValueError("folder_name não pode ser apenas espaços em branco")
            # Depois valida o formato
            if len(value) != 12:
                raise ValueError("folder_name deve ter exatamente 12 caracteres")
            if not value.endswith("="):
                raise ValueError("folder_name deve terminar com =")
        return value

    @field_validator("levelname", "account_id", mode="before")
    @classmethod
    def validate_not_whitespace_only(cls, value, info):
        """Valida que strings não contêm apenas espaços em branco.

        Aplicado a: levelname, account_id
        Padrão: Consolidação de 2 validators duplicados em 1 multi-field validator.
        """
        if isinstance(value, str) and value.strip() == "":
            field_name = info.field_name
            raise ValueError(f"{field_name} não pode ser apenas espaços em branco")
        return value

    @field_validator("version", mode="before")
    @classmethod
    def validate_version_not_negative(cls, value):
        """Valida que os números da versão não são negativos."""
        if not isinstance(value, list) or len(value) != 5:
            raise ValueError("version deve ser uma lista de exatamente 5 inteiros")
        for num in value:
            if not isinstance(num, int) or num < 0:
                raise ValueError("version deve conter apenas inteiros não negativos")
        return value
