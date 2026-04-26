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

from unittest.mock import Mock

from backup_manager_mvp.core.models.progress_model import ProgressModel
from backup_manager_mvp.core.services.progress_service import ProgressService


class TestProgressServiceInitialization:
    def test_create_progress_service_with_callback(self):
        callback = Mock()
        service = ProgressService(on_progress=callback)

        assert service.on_progress == callback

    def test_create_progress_service_without_callback(self):
        service = ProgressService()

        assert service.on_progress is None


class TestProgressServiceReporting:
    def test_report_progress_calls_callback(self):
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=5, total=10, stage="Processando")

        callback.assert_called_once()
        args = callback.call_args[0]
        assert isinstance(args[0], ProgressModel)
        assert args[0].current == 5
        assert args[0].total == 10
        assert args[0].stage == "Processando"

    def test_report_progress_without_callback_does_not_crash(self):
        service = ProgressService()

        service.report(current=5, total=10, stage="Processando")

    def test_report_progress_multiple_times(self):
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=1, total=10, stage="Etapa 1")
        service.report(current=5, total=10, stage="Etapa 2")
        service.report(current=10, total=10, stage="Concluído")

        assert callback.call_count == 3

    def test_report_progress_with_different_stages(self):
        callback = Mock()
        service = ProgressService(on_progress=callback)

        stages = ["Iniciando", "Copiando", "Finalizando"]
        for i, stage in enumerate(stages, 1):
            service.report(current=i, total=3, stage=stage)

        for i, call in enumerate(callback.call_args_list):
            progress = call[0][0]
            assert progress.stage == stages[i]


class TestProgressServiceReset:
    def test_reset_progress(self):
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=5, total=10, stage="Processando")
        service.reset()

        assert service.on_progress == callback

    def test_reset_allows_new_progress(self):
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=5, total=10, stage="Operação 1")
        service.reset()
        service.report(current=3, total=5, stage="Operação 2")

        assert callback.call_count == 2


class TestProgressServiceCallback:
    def test_change_callback(self):
        callback1 = Mock()
        callback2 = Mock()

        service = ProgressService(on_progress=callback1)
        service.report(current=1, total=10, stage="Com callback1")

        service.set_callback(callback2)
        service.report(current=2, total=10, stage="Com callback2")

        assert callback1.call_count == 1
        assert callback2.call_count == 1

    def test_set_callback_none_disables_reporting(self):
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.set_callback(None)
        service.report(current=1, total=10, stage="Teste")

        callback.assert_not_called()
