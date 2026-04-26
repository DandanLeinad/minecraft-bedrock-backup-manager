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

import contextlib
from unittest.mock import patch

from backup_manager_mvp.core.models.progress_model import ProgressModel
from backup_manager_mvp.core.services.backup_service import BackupService


class TestCreateBackupWithProgress:
    def test_create_backup_accepts_progress_callback(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)

        assert result.backup_path.exists()

    def test_progress_callback_receives_progress_models(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        assert len(progress_updates) > 0
        for update in progress_updates:
            assert isinstance(update, ProgressModel)

    def test_progress_starts_at_0_and_ends_at_100(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        if len(progress_updates) > 0:
            last = progress_updates[-1]

            assert last.percentage == 100.0
            assert last.is_complete() is True

    def test_progress_includes_stage_text(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        if len(progress_updates) > 1:
            assert any(p.stage for p in progress_updates)

    def test_backup_completes_even_if_callback_raises_exception(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        def bad_callback(progress: ProgressModel) -> None:
            raise RuntimeError("Callback falhou!")

        backup_base = tmp_path / "backups"

        with (
            patch.object(backup_service, "get_backup_base_path", return_value=backup_base),
            contextlib.suppress(RuntimeError),
        ):
            backup_service.create_backup(sample_world, progress_callback=bad_callback)

    def test_progress_reports_current_and_total(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        for progress in progress_updates:
            assert progress.current <= progress.total
            assert progress.total > 0


class TestRestoreBackupWithProgressCallback:
    def test_restore_backup_accepts_progress_callback(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        (sample_world.path / "old_file.txt").write_text("old content")

        backup_service.restore_backup(backup_with_content, sample_world)

        assert not (sample_world.path / "old_file.txt").exists()
        assert (sample_world.path / "level.dat").exists()

    def test_progress_callback_receives_progress_models(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        (sample_world.path / "old_file.txt").write_text("old content")

        backup_service.restore_backup(
            backup_with_content, sample_world, progress_callback=capture_progress
        )

        assert len(progress_updates) > 0
        for update in progress_updates:
            assert isinstance(update, ProgressModel)

    def test_restore_progress_goes_from_0_to_100_percent(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        (sample_world.path / "old_file.txt").write_text("old content")

        backup_service.restore_backup(
            backup_with_content, sample_world, progress_callback=capture_progress
        )

        assert len(progress_updates) >= 2
        first = progress_updates[0]
        assert first.percentage == 0.0

        last = progress_updates[-1]
        assert last.percentage == 100.0
        assert last.is_complete() is True

    def test_restore_progress_includes_stage_text(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        (sample_world.path / "old_file.txt").write_text("old content")

        backup_service.restore_backup(
            backup_with_content, sample_world, progress_callback=capture_progress
        )

        if len(progress_updates) > 1:
            assert any(p.stage for p in progress_updates)
            stage_texts = [p.stage for p in progress_updates]
            assert any(
                "Limpando" in s or "Restaurando" in s or "concluída" in s for s in stage_texts
            )

    def test_backup_completes_even_if_callback_raises_exception(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        def bad_callback(progress: ProgressModel) -> None:
            raise RuntimeError("Callback falhou!")

        (sample_world.path / "old_file.txt").write_text("old content")

        with contextlib.suppress(RuntimeError):
            backup_service.restore_backup(
                backup_with_content, sample_world, progress_callback=bad_callback
            )

    def test_restore_progress_reports_current_and_total(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        (sample_world.path / "old_file.txt").write_text("old content")

        backup_service.restore_backup(
            backup_with_content, sample_world, progress_callback=capture_progress
        )

        for progress in progress_updates:
            assert progress.current >= 0
            assert progress.total > 0
            assert progress.current <= progress.total

    def test_restore_progress_world_restored_correctly(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        (sample_world.path / "old_file.txt").write_text("old content")
        (sample_world.path / "old_level.dat").write_bytes(b"old data")

        backup_service.restore_backup(
            backup_with_content, sample_world, progress_callback=capture_progress
        )

        assert not (sample_world.path / "old_file.txt").exists()
        assert not (sample_world.path / "old_level.dat").exists()
        assert (sample_world.path / "level.dat").exists()
        assert (sample_world.path / "level.sdat").exists()
        assert (sample_world.path / "world_data" / "file.txt").exists()
        assert (sample_world.path / "world_data" / "file.txt").read_text() == "content"
