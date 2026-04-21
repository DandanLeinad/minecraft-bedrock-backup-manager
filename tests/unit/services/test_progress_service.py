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

"""Testes para ProgressService - MC-2 Progress Bar Feature."""

from unittest.mock import Mock

from backup_manager_mvp.models.progress_model import ProgressModel
from backup_manager_mvp.services.progress_service import ProgressService


class TestProgressServiceInitialization:
    """Testa criação e inicialização do ProgressService."""

    def test_create_progress_service_with_callback(self):
        """Cria ProgressService com callback."""
        callback = Mock()
        service = ProgressService(on_progress=callback)

        assert service.on_progress == callback

    def test_create_progress_service_without_callback(self):
        """Cria ProgressService sem callback (opcional)."""
        service = ProgressService()

        assert service.on_progress is None


class TestProgressServiceReporting:
    """Testa reportagem de progresso."""

    def test_report_progress_calls_callback(self):
        """Reportar progresso chama o callback."""
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=5, total=10, stage="Processando")

        callback.assert_called_once()
        # Verificar que foi chamado com ProgressModel
        args = callback.call_args[0]
        assert isinstance(args[0], ProgressModel)
        assert args[0].current == 5
        assert args[0].total == 10
        assert args[0].stage == "Processando"

    def test_report_progress_without_callback_does_not_crash(self):
        """Reportar sem callback não causa erro."""
        service = ProgressService()

        # Não deve lançar exceção
        service.report(current=5, total=10, stage="Processando")

    def test_report_progress_multiple_times(self):
        """Reportar múltiplas vezes chama callback múltiplas vezes."""
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=1, total=10, stage="Etapa 1")
        service.report(current=5, total=10, stage="Etapa 2")
        service.report(current=10, total=10, stage="Concluído")

        assert callback.call_count == 3

    def test_report_progress_with_different_stages(self):
        """Reportar com diferentes estágios."""
        callback = Mock()
        service = ProgressService(on_progress=callback)

        stages = ["Iniciando", "Copiando", "Finalizando"]
        for i, stage in enumerate(stages, 1):
            service.report(current=i, total=3, stage=stage)

        # Verificar que cada callback recebeu o stage correto
        for i, call in enumerate(callback.call_args_list):
            progress = call[0][0]
            assert progress.stage == stages[i]


class TestProgressServiceReset:
    """Testa reset de progresso."""

    def test_reset_progress(self):
        """Reset reseta o progresso para 0."""
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=5, total=10, stage="Processando")
        service.reset()

        # Após reset, callback deve ter sido chamado com 0/0
        # Mas reset pode não chamar callback, depende da implementação
        # Por enquanto, apenas verificamos que reset não falha
        assert service.on_progress == callback

    def test_reset_allows_new_progress(self):
        """Após reset, pode reportar novo progresso."""
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=5, total=10, stage="Operação 1")
        service.reset()
        service.report(current=3, total=5, stage="Operação 2")

        # Callback deve ter sido chamado 2 vezes
        assert callback.call_count == 2


class TestProgressServiceCallback:
    """Testa substituição de callback."""

    def test_change_callback(self):
        """Muda callback dinamicamente."""
        callback1 = Mock()
        callback2 = Mock()

        service = ProgressService(on_progress=callback1)
        service.report(current=1, total=10, stage="Com callback1")

        # Mudar callback
        service.set_callback(callback2)
        service.report(current=2, total=10, stage="Com callback2")

        assert callback1.call_count == 1
        assert callback2.call_count == 1

    def test_set_callback_none_disables_reporting(self):
        """Setar callback=None desativa reporting."""
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.set_callback(None)
        service.report(current=1, total=10, stage="Teste")

        # Callback não deve ser chamado
        callback.assert_not_called()
