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

"""Widget de barra de progresso baseado em CustomTkinter.

Usado para mostrar progresso de operações (backup, restore, etc).
Integra-se com ProgressModel e ProgressService.

Baseado na documentação de CustomTkinter:
https://customtkinter.tomschimansky.com/documentation/widgets/progressbar
"""

import logging

import customtkinter as ctk

from backup_manager_mvp.models.progress_model import ProgressModel

logger = logging.getLogger(__name__)


class ProgressBarWidget(ctk.CTkFrame):
    """Widget de barra de progresso com labels de stage e percentual.

    Exibe:
    - Barra de progresso visual (CTkProgressBar)
    - Texto de etapa (stage)
    - Percentual de conclusão

    Example:
        ```python
        progress_widget = ProgressBarWidget(master=parent_frame)
        progress_widget.pack(fill="x", padx=10, pady=10)

        # Atualizar progresso
        progress_model = ProgressModel(current=5, total=10, stage="Copiando...")
        progress_widget.update_progress(progress_model)
        ```
    """

    def __init__(self, master=None, **kwargs):
        """Inicializa o widget de progresso.

        Args:
            master: Widget pai (obrigatório para Tkinter)
            **kwargs: Argumentos adicionais para CTkFrame (bg_color, etc)
        """
        super().__init__(master, **kwargs)

        # === CONTAINER PRINCIPAL ===
        self.configure(fg_color="transparent")

        # === LABELS (stage + percentage) ===
        self._label_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._label_frame.pack(fill="x", pady=(0, 8))

        self._stage_label = ctk.CTkLabel(
            self._label_frame,
            text="",
            font=("Arial", 12),
            text_color=("gray10", "gray90"),
        )
        self._stage_label.pack(side="left", fill="x", expand=True)

        self._percentage_label = ctk.CTkLabel(
            self._label_frame,
            text="0%",
            font=("Arial", 11),
            text_color=("gray50", "gray50"),
        )
        self._percentage_label.pack(side="right")

        # === BARRA DE PROGRESSO ===
        # Modo determinado: mostra progresso específico (não animado)
        self._progress_bar = ctk.CTkProgressBar(
            self,
            height=20,
            corner_radius=5,
            fg_color=("gray70", "gray30"),  # (light mode, dark mode)
            progress_color=("blue", "darkblue"),  # (light mode, dark mode)
            mode="determinate",  # Modo determinado (não indeterminado)
        )
        self._progress_bar.pack(fill="x", pady=(0, 0))
        self._progress_bar.set(0)  # Iniciar em 0%

        # === ESTADO ===
        self._current_progress: ProgressModel | None = None

    def update_progress(self, progress: ProgressModel) -> None:
        """Atualiza a barra de progresso com um modelo.

        Args:
            progress: ProgressModel com current, total, stage, percentage

        Example:
            ```python
            progress = ProgressModel(current=5, total=10, stage="Copiando")
            widget.update_progress(progress)
            # Barra mostrará 50%, com "Copiando 50%" embaixo
            ```
        """
        self._current_progress = progress

        # === ATUALIZAR BARRA ===
        # CTkProgressBar usa range 0.0 - 1.0, então converter percentagem
        progress_value = progress.percentage / 100.0
        self._progress_bar.set(progress_value)

        # === ATUALIZAR LABELS ===
        # Stage + percentage
        stage_text = progress.stage
        percentage_text = f"{progress.percentage:.0f}%"

        self._stage_label.configure(text=stage_text)
        self._percentage_label.configure(text=percentage_text)

        # Log visual para debug
        logger.debug(f"Progress Bar: {percentage_text} | {stage_text}")

        # Atualizar UI (evita freezing em operações longas)
        self.update_idletasks()

    def reset(self) -> None:
        """Reseta a barra de progresso para 0%."""
        self._progress_bar.set(0)
        self._stage_label.configure(text="")
        self._percentage_label.configure(text="0%")
        self._current_progress = None
        self.update_idletasks()

    def is_complete(self) -> bool:
        """Verifica se o progresso está completo.

        Returns:
            bool: True se percentagem == 100%
        """
        if self._current_progress is None:
            return False
        return self._current_progress.is_complete()

    def get_progress(self) -> ProgressModel | None:
        """Retorna o último ProgressModel atualizado.

        Returns:
            ProgressModel ou None se nunca foi atualizado
        """
        return self._current_progress
