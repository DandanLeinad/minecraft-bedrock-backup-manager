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

import pytest
from pydantic import ValidationError

from backup_manager_mvp.core.models.world_model import WorldModel


def test_world_model_valid(valid_world_model_data: dict[str, Path | str | list[int]]) -> None:
    world_model = WorldModel(**valid_world_model_data)

    assert world_model.folder_name == valid_world_model_data["folder_name"]
    assert world_model.levelname == valid_world_model_data["levelname"]
    assert world_model.path == valid_world_model_data["path"]
    assert world_model.account_id == valid_world_model_data["account_id"]
    assert world_model.version == valid_world_model_data["version"]


@pytest.mark.parametrize(
    "field,invalid_value,test_id",
    [
        ("folder_name", 123, "folder_name_type"),
        ("levelname", 123, "levelname_type"),
        ("account_id", 123, "account_id_type"),
        ("version", "not_a_list", "version_type"),
        ("folder_name", None, "folder_name_none"),
        ("levelname", None, "levelname_none"),
        ("account_id", None, "account_id_none"),
        ("path", None, "path_none"),
        ("version", None, "version_none"),
        ("folder_name", "", "folder_name_empty"),
        ("levelname", "", "levelname_empty"),
        ("account_id", "", "account_id_empty"),
        ("path", Path(""), "path_empty"),
        ("version", [], "version_empty"),
        ("version", [1, 2, 3, 4], "version_too_short"),
        ("version", [1, 2, 3, 4, 5, 6], "version_too_long"),
        ("version", [1, -26, 12, 2, 0], "version_negative"),
        ("folder_name", "   ", "folder_name_whitespace"),
        ("levelname", "   ", "levelname_whitespace"),
        ("account_id", "   ", "account_id_whitespace"),
        ("folder_name", "6LknJ3qXcJo", "folder_name_wrong_length"),
        ("folder_name", "6LknJ3qXcJoX", "folder_name_missing_padding"),
    ],
    ids=[
        "folder_name_type",
        "levelname_type",
        "account_id_type",
        "version_type",
        "folder_name_none",
        "levelname_none",
        "account_id_none",
        "path_none",
        "version_none",
        "folder_name_empty",
        "levelname_empty",
        "account_id_empty",
        "path_empty",
        "version_empty",
        "version_too_short",
        "version_too_long",
        "version_negative",
        "folder_name_whitespace",
        "levelname_whitespace",
        "account_id_whitespace",
        "folder_name_wrong_length",
        "folder_name_missing_padding",
    ],
)
def test_world_model_validation_error(field, invalid_value, test_id, make_invalid_world_data):
    with pytest.raises(ValidationError):
        WorldModel(**make_invalid_world_data(field, invalid_value))


def test_world_model_missing_fields() -> None:
    with pytest.raises(ValidationError):
        WorldModel(
            folder_name="6LknJ3qXcJo=",
            levelname="My World",
        )
