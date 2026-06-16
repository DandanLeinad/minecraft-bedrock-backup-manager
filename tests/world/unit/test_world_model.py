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
from typing import TypedDict

import pytest
from pydantic import ValidationError

from backup_manager_mvp.core.models.world_model import WorldModel


class ValidWorldModelData(TypedDict):
    folder_name: str
    levelname: str
    world_icon_path: Path
    path: Path
    account_id: str
    version: list[int]


class TestWorldModelConstruction:
    """Tests for valid WorldModel creation."""

    def test_should_create_world_model_when_all_fields_valid(
        self, valid_world_model_data: ValidWorldModelData
    ) -> None:
        """
        A valid WorldModel should be created when all required fields
        are provided with valid values.
        """
        world_model = WorldModel(**valid_world_model_data)

        assert world_model.folder_name == valid_world_model_data["folder_name"]
        assert world_model.levelname == valid_world_model_data["levelname"]
        assert world_model.world_icon_path == valid_world_model_data["world_icon_path"]
        assert world_model.path == valid_world_model_data["path"]
        assert world_model.account_id == valid_world_model_data["account_id"]
        assert world_model.version == valid_world_model_data["version"]

    def test_should_reject_world_model_when_required_field_missing(self) -> None:
        """
        WorldModel should reject creation when required fields
        are missing.
        """
        with pytest.raises(ValidationError):
            WorldModel(
                folder_name="6LknJ3qXcJo=",
                levelname="My World",
                world_icon_path=Path(
                    "C:/Users/usuario/AppData/Roaming/Minecraft Bedrock/Users/9603359306719601750/games/com.mojang/minecraftWorlds/6LknJ3qXcJo=/world_icon.jpeg"
                ),
                path=Path(
                    "C:/Users/usuario/AppData/Roaming/Minecraft Bedrock/Users/9603359306719601750/games/com.mojang/minecraftWorlds/6LknJ3qXcJo="
                ),
                account_id="9603359306719601750",
                version=[1, 2, 3, 4, 5, 6],
            )


class TestFolderNameValidation:
    """Tests for folder_name field validation rules.

    Rules:
    - Must be a string (not int, not None)
    - Cannot be empty
    - Cannot contain only whitespace
    - Must have exactly 12 characters
    - Must end with '=' (Minecraft Bedrock base64 padding)
    """

    @pytest.mark.parametrize(
        "invalid_value,description",
        [
            (123, "not_a_string"),
            (None, "none"),
            ("", "empty"),
            ("   ", "whitespace_only"),
            ("6LknJ3qXcJo", "wrong_length_11_chars"),
            ("6LknJ3qXcJoX", "missing_padding"),
        ],
        ids=[
            "type_int",
            "none",
            "empty",
            "whitespace_only",
            "wrong_length",
            "missing_padding",
        ],
    )
    def test_should_reject_invalid_folder_name(
        self, invalid_value, description, make_invalid_world_model_data
    ) -> None:
        """
        folder_name should be rejected when:
        - not a string
        - is None
        - is empty
        - contains only whitespace
        - does not have exactly 12 characters
        - does not end with '='
        """
        with pytest.raises(ValidationError):
            WorldModel(**make_invalid_world_model_data("folder_name", invalid_value))


class TestLevelNameValidation:
    """Tests for levelname field validation rules.

    Rules:
    - Must be a string (not int, not None)
    - Cannot be empty
    - Cannot contain only whitespace
    """

    @pytest.mark.parametrize(
        "invalid_value,description",
        [
            (123, "not_a_string"),
            (None, "none"),
            ("", "empty"),
            ("   ", "whitespace_only"),
        ],
        ids=[
            "type_int",
            "none",
            "empty",
            "whitespace_only",
        ],
    )
    def test_should_reject_invalid_levelname(
        self, invalid_value, description, make_invalid_world_model_data
    ) -> None:
        """
        levelname should be rejected when:
        - not a string
        - is None
        - is empty
        - contains only whitespace
        """
        with pytest.raises(ValidationError):
            WorldModel(**make_invalid_world_model_data("levelname", invalid_value))


class TestAccountIdValidation:
    """Tests for account_id field validation rules.

    Rules:
    - Must be a string (not int, not None)
    - Cannot be empty
    - Cannot contain only whitespace
    """

    @pytest.mark.parametrize(
        "invalid_value,description",
        [
            (123, "not_a_string"),
            (None, "none"),
            ("", "empty"),
            ("   ", "whitespace_only"),
        ],
        ids=[
            "type_int",
            "none",
            "empty",
            "whitespace_only",
        ],
    )
    def test_should_reject_invalid_account_id(
        self, invalid_value, description, make_invalid_world_model_data
    ) -> None:
        """
        account_id should be rejected when:
        - not a string
        - is None
        - is empty
        - contains only whitespace
        """
        with pytest.raises(ValidationError):
            WorldModel(**make_invalid_world_model_data("account_id", invalid_value))


class TestVersionValidation:
    """Tests for version field validation rules.

    Rules:
    - Must be a list (not string, not None)
    - Must have exactly 5 elements
    - All elements must be non-negative integers
    """

    @pytest.mark.parametrize(
        "invalid_value,description",
        [
            ("not_a_list", "not_a_list"),
            (None, "none"),
            ([], "empty"),
            ([1, 2, 3, 4], "too_short"),
            ([1, 2, 3, 4, 5, 6], "too_long"),
            ([1, -26, 12, 2, 0], "negative_value"),
        ],
        ids=[
            "type_string",
            "none",
            "empty",
            "too_short",
            "too_long",
            "negative_value",
        ],
    )
    def test_should_reject_invalid_version(
        self, invalid_value, description, make_invalid_world_model_data
    ) -> None:
        """
        version should be rejected when:
        - not a list
        - is None
        - is empty
        - has fewer than 5 elements
        - has more than 5 elements
        - contains negative integer
        """
        with pytest.raises(ValidationError):
            WorldModel(**make_invalid_world_model_data("version", invalid_value))


class TestPathValidation:
    """Tests for path and world_icon_path field validation rules.

    Rules:
    - Cannot be None
    - Cannot be empty
    - Cannot be "." (current directory)
    """

    @pytest.mark.parametrize(
        "field,invalid_value,description",
        [
            ("world_icon_path", None, "none"),
            ("path", None, "none"),
            ("world_icon_path", Path(""), "empty"),
            ("path", Path(""), "empty"),
        ],
        ids=[
            "world_icon_path_none",
            "path_none",
            "world_icon_path_empty",
            "path_empty",
        ],
    )
    def test_should_reject_invalid_path_fields(
        self, field, invalid_value, description, make_invalid_world_model_data
    ) -> None:
        """
        path and world_icon_path should be rejected when:
        - are None
        - are empty
        """
        with pytest.raises(ValidationError):
            WorldModel(**make_invalid_world_model_data(field, invalid_value))
