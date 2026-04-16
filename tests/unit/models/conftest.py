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

"""Fixtures compartilhadas para testes de models.

Este arquivo (conftest.py) é descoberto automaticamente pelo pytest.
Qualquer fixture definida aqui está disponível para todos os testes
em tests/unit/models/ sem necessidade de importação explícita.

Hierarquia pytest discovery:
  1. test_*.py (local - mais alta prioridade)
  2. conftest.py do subdiretório (aqui!)
  3. conftest.py do diretório pai
  4. conftest.py global
"""

from pathlib import Path

import pytest


@pytest.fixture
def valid_world_model_data() -> dict[str, Path | str | list[int]]:
    """Fornece dados válidos para criar uma instância de WorldModel.

    Esta fixture é reutilizável por qualquer teste em tests/unit/models/
    sem necessidade de importação.
    """
    return {
        "folder_name": "6LknJ3qXcJo=",
        "levelname": "My World",
        "path": Path(
            "C:/Users/usuario/AppData/Roaming/Minecraft Bedrock/Users/9603359306719601750/games/com.mojang/minecraftWorlds/6LknJ3qXcJo="
        ),
        "account_id": "9603359306719601750",
        "version": [1, 26, 12, 2, 0],
    }


@pytest.fixture
def make_invalid_world_data(valid_world_model_data):
    """Factory fixture: cria dados inválidos modificando qualquer campo.

    Padrão: (field_name, invalid_value) → dict com WorldModel inválido
    Reduz fixtures individuais a 1 factory reutilizável.

    Esta factory é compartilhada entre múltiplos testes e modelos.
    Quando criar BackupMetadata, BackupList, etc, poderão reutilizar
    o mesmo padrão factory sem duplicação.

    Exemplo:
        make_invalid_world_data("folder_name", 123)
        → {"folder_name": 123, "levelname": "My World", ...}
    """

    def _create(field_name: str, invalid_value):
        data = valid_world_model_data.copy()
        data[field_name] = invalid_value
        return data

    return _create
