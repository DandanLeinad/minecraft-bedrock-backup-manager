# minecraft-bedrock-backup-manager
# Copyright (C) 2026  DandanLeinad
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class WorldModel(BaseModel):
    """Modelo de dados para representar um mundo do Minecraft Bedrock Edition.

    Attributes:
        folder_name (str): Nome da pasta do mundo (obrigatório, min 1 caractere).
        levelname (str): Nome do mundo exibido no jogo (obrigatório, min 1 caractere).
        path (Path): Caminho completo para a pasta do mundo. Rejeita None, vazio ou ".".
        account_id (str): ID da conta Microsoft (obrigatório, min 1 caractere).
        version (list[int]): Versão do mundo - exatamente 5 inteiros (ex: [1, 26, 12, 2, 0]).

    Raises:
        ValidationError: Se algum campo não passar nas validações Pydantic.
    """

    folder_name: str = Field(..., min_length=1, max_length=12)  # Nome da pasta do mundo
    levelname: str = Field(..., min_length=1)  # Nome do mundo exibido no jogo
    path: Path = Field(...)  # Caminho completo para a pasta do mundo
    account_id: str = Field(..., min_length=1)  # ID da conta da Microsoft associada ao mundo
    version: list[int] = Field(
        ..., min_length=5, max_length=5
    )  # Versão do Mundo (lastOpenedWithVersion)

    @field_validator("path", mode="before")
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
