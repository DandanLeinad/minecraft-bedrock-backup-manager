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

"""Serviço para reportar progresso de operações."""

import logging
from collections.abc import Callable

from backup_manager_mvp.models.progress_model import ProgressModel

logger = logging.getLogger(__name__)


class ProgressService:
    """Serviço para reportar progresso de operações.

    Usado por BackupService, RestoreService, e qualquer operação que
    precisa comunicar seu progresso com a UI.

    Example:
        ```python
        def on_progress_update(progress: ProgressModel) -> None:
            print(f"{progress.stage}: {progress.percentage:.1f}%")

        service = ProgressService(on_progress=on_progress_update)
        service.report(current=5, total=10, stage="Copiando arquivos")
        # Output: "Copiando arquivos: 50.0%"
        ```
    """

    def __init__(self, on_progress: Callable[[ProgressModel], None] | None = None):
        """Inicializa o serviço de progresso.

        Args:
            on_progress: Callback chamado quando progresso é reportado.
                        Recebe um ProgressModel como argumento.
                        Pode ser None (reporting desativado).
        """
        self.on_progress = on_progress

    def report(self, current: int, total: int, stage: str = "") -> None:
        """Reporta progresso de uma operação.

        Args:
            current: Número de itens processados
            total: Total de itens
            stage: Descrição da etapa (opcional)

        Note:
            Se on_progress for None, este método não faz nada.
        """
        if self.on_progress is None:
            return

        progress = ProgressModel(current=current, total=total, stage=stage)
        self.on_progress(progress)

    def set_callback(self, callback: Callable[[ProgressModel], None] | None) -> None:
        """Muda o callback de progresso dinamicamente.

        Args:
            callback: Novo callback ou None para desativar reporting

        Example:
            ```python
            service = ProgressService(on_progress=callback1)
            # ... algum progresso ...
            service.set_callback(callback2)  # Muda callback
            # ... mais progresso com callback2 ...
            service.set_callback(None)  # Desativa reporting
            ```
        """
        self.on_progress = callback
        logger.debug(f"ProgressService callback alterado: {callback}")

    def reset(self) -> None:
        """Reseta o estado do serviço.

        Útil quando começando uma nova operação após a anterior.
        """
        # Implementação simples: apenas log
        # O estado real (current/total) é mantido pelo chamador
        logger.debug("ProgressService resetado")
