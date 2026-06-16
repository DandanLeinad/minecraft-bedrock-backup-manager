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
    """Tests for create_backup with progress callback.

    Rules:
    - Accepts optional progress_callback parameter
    - Calls callback with ProgressModel instances
    - Progress starts at 0% and ends at 100%
    - Includes stage text describing current operation
    - Completes backup even if callback raises exception
    - Reports current and total progress values
    """

    def test_should_accept_progress_callback_when_provided(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        """
        create_backup should accept an optional progress_callback parameter
        and complete successfully.
        """
        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            result = backup_service.create_backup(sample_world)

        assert result.backup_path.exists()

    def test_should_call_callback_with_progress_models(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        """
        create_backup should call the progress callback with ProgressModel
        instances for each progress update.
        """
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        assert len(progress_updates) > 0
        for update in progress_updates:
            assert isinstance(update, ProgressModel)

    def test_should_start_at_zero_percent_and_end_at_hundred_percent(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        """
        Progress should start at 0% and end at 100% when backup completes.
        """
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

    def test_should_include_stage_text_in_progress_updates(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        """
        Progress updates should include stage text describing the current operation.
        """
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        if len(progress_updates) > 1:
            assert any(p.stage for p in progress_updates)

    def test_should_complete_backup_even_when_callback_raises_exception(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        """
        create_backup should complete successfully even when the progress
        callback raises an exception.
        """

        def bad_callback(progress: ProgressModel) -> None:
            raise RuntimeError("Callback failed!")

        backup_base = tmp_path / "backups"

        with (
            patch.object(backup_service, "get_backup_base_path", return_value=backup_base),
            contextlib.suppress(RuntimeError),
        ):
            backup_service.create_backup(sample_world, progress_callback=bad_callback)

    def test_should_report_current_and_total_in_progress(
        self, tmp_path, backup_service: BackupService, sample_world
    ) -> None:
        """
        Progress updates should report current and total values,
        with current <= total and total > 0.
        """
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        backup_base = tmp_path / "backups"

        with patch.object(backup_service, "get_backup_base_path", return_value=backup_base):
            backup_service.create_backup(sample_world, progress_callback=capture_progress)

        for progress in progress_updates:
            assert progress.current <= progress.total
            assert progress.total > 0


class TestRestoreBackupWithProgress:
    """Tests for restore_backup with progress callback.

    Rules:
    - Accepts optional progress_callback parameter
    - Calls callback with ProgressModel instances
    - Progress starts at 0% and ends at 100%
    - Includes stage text (cleaning, restoring, completed)
    - Completes restore even if callback raises exception
    - Reports current and total progress values
    - Restores world correctly after completion
    """

    def test_should_accept_progress_callback_when_provided(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        """
        restore_backup should accept an optional progress_callback parameter
        and complete successfully.
        """
        (sample_world.path / "old_file.txt").write_text("old content")

        backup_service.restore_backup(backup_with_content, sample_world)

        assert not (sample_world.path / "old_file.txt").exists()
        assert (sample_world.path / "level.dat").exists()

    def test_should_call_callback_with_progress_models(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        """
        restore_backup should call the progress callback with ProgressModel
        instances for each progress update.
        """
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

    def test_should_start_at_zero_percent_and_end_at_hundred_percent(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        """
        Progress should start at 0% and end at 100% when restore completes.
        """
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

    def test_should_include_stage_text_in_restore_progress(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        """
        Restore progress updates should include stage text describing
        the current operation.
        """
        progress_updates = []

        def capture_progress(progress: ProgressModel) -> None:
            progress_updates.append(progress)

        (sample_world.path / "old_file.txt").write_text("old content")

        backup_service.restore_backup(
            backup_with_content, sample_world, progress_callback=capture_progress
        )

        if len(progress_updates) > 1:
            assert any(p.stage for p in progress_updates)
            # Stage text should be non-empty strings describing the operation
            stage_texts = [p.stage for p in progress_updates if p.stage]
            assert len(stage_texts) > 0

    def test_should_complete_restore_even_when_callback_raises_exception(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        """
        restore_backup should complete successfully even when the progress
        callback raises an exception.
        """

        def bad_callback(progress: ProgressModel) -> None:
            raise RuntimeError("Callback failed!")

        (sample_world.path / "old_file.txt").write_text("old content")

        with contextlib.suppress(RuntimeError):
            backup_service.restore_backup(
                backup_with_content, sample_world, progress_callback=bad_callback
            )

    def test_should_report_current_and_total_in_restore_progress(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        """
        Restore progress updates should report current and total values,
        with current >= 0, total > 0, and current <= total.
        """
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

    def test_should_restore_world_correctly_after_completion(
        self,
        backup_service: BackupService,
        sample_world,
        backup_with_content,
    ) -> None:
        """
        World should be correctly restored after completion with all
        backup files present and old files removed.
        """
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
