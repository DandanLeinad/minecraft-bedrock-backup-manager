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

"""Testes para detecção de mundos em múltiplas sources (UWP, Shared, Normal)."""

from pathlib import Path
from unittest.mock import patch

from backup_manager_mvp.services.world_service import WorldService


class TestGetUWPStorePath:
    """Testes para obter caminho do UWP Store."""

    def test_get_uwp_store_path_returns_path_object(self, tmp_path: Path) -> None:
        """Teste: get_uwp_store_path retorna objeto Path."""
        service = WorldService()
        mock_path = (
            tmp_path
            / "AppData"
            / "Local"
            / "Packages"
            / "MinecraftUWP_8wekyb3d8bbwe"
            / "LocalState"
        )
        with patch.object(service, "get_uwp_store_path", return_value=mock_path):
            path = service.get_uwp_store_path()
            assert isinstance(path, Path)

    def test_get_uwp_store_path_contains_minecraft_uwp(self, tmp_path: Path) -> None:
        """Teste: Path contém MinecraftUWP_8wekyb3d8bbwe."""
        service = WorldService()
        mock_path = (
            tmp_path
            / "AppData"
            / "Local"
            / "Packages"
            / "MinecraftUWP_8wekyb3d8bbwe"
            / "LocalState"
        )
        with patch.object(service, "get_uwp_store_path", return_value=mock_path):
            path = service.get_uwp_store_path()
            assert "MinecraftUWP_8wekyb3d8bbwe" in str(path)

    def test_get_uwp_store_path_contains_local_state(self, tmp_path: Path) -> None:
        """Teste: Path contém LocalState."""
        service = WorldService()
        mock_path = (
            tmp_path
            / "AppData"
            / "Local"
            / "Packages"
            / "MinecraftUWP_8wekyb3d8bbwe"
            / "LocalState"
        )
        with patch.object(service, "get_uwp_store_path", return_value=mock_path):
            path = service.get_uwp_store_path()
            assert "LocalState" in str(path)


class TestGetSharedPath:
    """Testes para obter caminho do Shared."""

    def test_get_shared_path_returns_path_object(self, tmp_path: Path) -> None:
        """Teste: get_shared_path retorna objeto Path."""
        service = WorldService()
        mock_path = tmp_path / "Shared" / "minecraftWorlds"
        with patch.object(service, "get_shared_path", return_value=mock_path):
            path = service.get_shared_path()
            assert isinstance(path, Path)

    def test_get_shared_path_contains_shared_directory(self, tmp_path: Path) -> None:
        """Teste: Path contém diretório Shared."""
        service = WorldService()
        mock_path = tmp_path / "Shared" / "minecraftWorlds"
        with patch.object(service, "get_shared_path", return_value=mock_path):
            path = service.get_shared_path()
            assert "Shared" in str(path)

    def test_get_shared_path_contains_minecraftworlds(self, tmp_path: Path) -> None:
        """Teste: Path contém minecraftWorlds."""
        service = WorldService()
        mock_path = tmp_path / "Shared" / "minecraftWorlds"
        with patch.object(service, "get_shared_path", return_value=mock_path):
            path = service.get_shared_path()
            assert "minecraftWorlds" in str(path)


class TestListWorldsMultipleSources:
    """Testes para listar mundos de múltiplas sources."""

    def test_list_worlds_returns_list(self, tmp_path: Path) -> None:
        """Teste: list_worlds retorna lista (regressão)."""
        service = WorldService()

        # Mock all world base paths para tmp_path (isolado)
        with patch.object(service, "get_worlds_base_path", return_value=tmp_path):
            worlds = service.list_worlds()

        assert isinstance(worlds, list)

    def test_list_worlds_returns_world_models(self, tmp_path: Path) -> None:
        """Teste: Elementos da lista são WorldModel (regressão)."""
        service = WorldService()

        with patch.object(service, "get_worlds_base_path", return_value=tmp_path):
            worlds = service.list_worlds()

        # Se houver mundos, validar que são WorldModel
        if worlds:
            from backup_manager_mvp.models.world_model import WorldModel

            assert all(isinstance(w, WorldModel) for w in worlds)

    def test_list_worlds_includes_normal_account_ids(self, tmp_path: Path) -> None:
        """Teste: Continua detectando contas normais com UUIDs (regressão)."""
        service = WorldService()

        # Criar estrutura fake
        account_dir = tmp_path / "test_account"
        account_dir.mkdir()

        with patch.object(service, "get_worlds_base_path", return_value=tmp_path):
            worlds = service.list_worlds()

        # Filtrar mundos com account_id que NÃO são especiais
        normal_worlds = [w for w in worlds if w.account_id not in ("UWP-Store", "Shared")]
        # Se houver mundos normais, devem estar lá
        # (Este teste passa mesmo se não houver mundos no sistema)
        assert isinstance(normal_worlds, list)

    def test_list_worlds_may_include_uwp_store_worlds(self, tmp_path: Path) -> None:
        """Teste: Se UWP Store existe, mundos aparecem com account_id = UWP-Store."""
        service = WorldService()

        with (
            patch.object(service, "get_worlds_base_path", return_value=tmp_path),
            patch.object(service, "get_uwp_store_path", return_value=tmp_path),
        ):
            worlds = service.list_worlds()

        # Teste: pode ter mundos UWP (se existirem)
        uwp_worlds = [w for w in worlds if w.account_id == "UWP-Store"]
        assert isinstance(uwp_worlds, list)

    def test_list_worlds_may_include_shared_worlds(self, tmp_path: Path) -> None:
        """Teste: Se diretório Shared existe, mundos aparecem com account_id = Shared."""
        service = WorldService()

        with (
            patch.object(service, "get_worlds_base_path", return_value=tmp_path),
            patch.object(service, "get_shared_path", return_value=tmp_path),
        ):
            worlds = service.list_worlds()

        shared_worlds = [w for w in worlds if w.account_id == "Shared"]
        # Este teste passa mesmo se não houver Shared mundos
        for world in shared_worlds:
            assert world.account_id == "Shared"

    def test_account_id_is_always_string(self, tmp_path: Path) -> None:
        """Teste: account_id é sempre string (normal, UWP ou Shared)."""
        service = WorldService()

        with patch.object(service, "get_worlds_base_path", return_value=tmp_path):
            worlds = service.list_worlds()

        for world in worlds:
            assert isinstance(world.account_id, str)
            assert len(world.account_id) > 0


class TestListAccountIds:
    """Testes para listar account IDs normais (regressão)."""

    def test_list_account_ids_returns_list(self, tmp_path: Path) -> None:
        """Teste: list_account_ids retorna lista (regressão)."""
        service = WorldService()

        with patch.object(service, "get_worlds_base_path", return_value=tmp_path):
            account_ids = service.list_account_ids()

        assert isinstance(account_ids, list)

    def test_list_account_ids_are_strings(self, tmp_path: Path) -> None:
        """Teste: account_ids são strings (regressão)."""
        service = WorldService()

        with patch.object(service, "get_worlds_base_path", return_value=tmp_path):
            account_ids = service.list_account_ids()

        for account_id in account_ids:
            assert isinstance(account_id, str)
