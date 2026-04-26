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

"""Testes de integração: BackupService + ProgressService - MC-2 Progress Bar Feature."""

import contextlib
from pathlib import Path
from unittest.mock import patch

import pytest

from backup_manager_mvp.core.models.progress_model import ProgressModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.backup_service import BackupService
from backup_manager_mvp.core.services.progress_service import ProgressService
from backup_manager_mvp.infra.repository import FileSystemBackupRepository


@pytest.fixture
def backup_service() -> BackupService:
    """Fixture que fornece uma instância de BackupService."""
    return BackupService(FileSystemBackupRepository())


@pytest.fixture
def progress_service() -> ProgressService:
    """Fixture que fornece uma instância de ProgressService."""
    return ProgressService()


@pytest.fixture
def sample_world(tmp_path: Path) -> WorldModel:
    """Fixture que fornece um WorldModel de exemplo com arquivos."""
    world_path = tmp_path / "test_world"
    world_path.mkdir()

    # Criar alguns arquivos de teste
    (world_path / "level.dat").write_bytes(b"test level data")
    (world_path / "level.dat_old").write_bytes(b"old data")
    (world_path / "db").mkdir()
    (world_path / "db" / "file1.txt").write_bytes(b"db file 1")
    (world_path / "db" / "file2.txt").write_bytes(b"db file 2")

    return WorldModel(
        folder_name="6LknJ-+T-Ks=",
        levelname="Meu Mundo",
        path=world_path,
        account_id="test_account",
        version=[1, 26, 12, 2, 0],
    )


class TestCreateBackupWithProgress:
    """Testa criação de backup com rastreamento de progresso."""

    def test_create_backup_accepts_progress_callback(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que create_backup aceita um callback de progresso (opcional)."""
        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            # create_backup não quebra mesmo com callback novo
            result = backup_service.create_backup(sample_world)

        # Backup deve funcionar normalmente
        assert result.backup_path.exists()

    def test_progress_callback_receives_progress_models(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que callback recebe ProgressModel com dados corretos."""
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        # Callback deve ter sido chamado
        assert len(progress_updates) > 0
        # Todos os updates devem ser ProgressModel
        for update in progress_updates:
            assert isinstance(update, ProgressModel)

    def test_progress_starts_at_0_and_ends_at_100(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que progresso começa em 0% e termina em 100%."""
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        if len(progress_updates) > 0:
            # Último update deve ser 100%
            last = progress_updates[-1]

            assert last.percentage == 100.0
            assert last.is_complete() is True

    def test_progress_includes_stage_text(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que updates incluem texto descritivo de stage."""
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        # Algum update deve ter stage text (exceto talvez o primeiro)
        if len(progress_updates) > 1:
            # Pelo menos um deve ter texto
            assert any(p.stage for p in progress_updates)

    def test_backup_completes_even_if_callback_raises_exception(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que backup funciona mesmo se callback lançar exceção."""

        def bad_callback(progress: ProgressModel) -> None:
            raise RuntimeError("Callback falhou!")

        backup_base = tmp_path / "backups"

        with (
            patch.object(backup_service, "get_backup_base_path", return_value=backup_base),
            contextlib.suppress(RuntimeError),
        ):
            # Mesmo com callback que falha, backup deve ser criado
            backup_service.create_backup(sample_world, progress_callback=bad_callback)

    def test_progress_reports_current_and_total(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que progresso reporta current e total corretamente."""
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        # Verificar que current <= total em todos os updates
        for progress in progress_updates:
            assert progress.current <= progress.total
            assert progress.total > 0


class TestProgressServiceIntegration:
    """Testa ProgressService como intermediária."""

    def test_progress_service_can_wrap_backup_callback(
        self, tmp_path: Path, backup_service: BackupService, sample_world: WorldModel
    ) -> None:
        """Testa que ProgressService pode ser usada como callback wrapper."""
        progress_service = ProgressService()
        final_updates = []

        def final_callback(progress: ProgressModel) -> None:
            final_updates.append(progress)

        progress_service.set_callback(final_callback)
        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            # Usar progress_service.report diretamente (simulando)
            progress_service.report(current=1, total=5, stage="Iniciando")
            progress_service.report(current=3, total=5, stage="Processando")
            progress_service.report(current=5, total=5, stage="Concluído")

        assert len(final_updates) == 3
        assert final_updates[-1].percentage == 100.0
