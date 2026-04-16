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

"""Gerenciador de notificações toast."""

import logging

import customtkinter as ctk

from backup_manager_mvp.ui.customtkinter.constants import COLORS

logger = logging.getLogger(__name__)


class ToastManager:
    """Gerencia notificações toast na UI."""

    def __init__(
        self,
        main_window: ctk.CTk,
        notifications_frame: ctk.CTkFrame,
        main_frame: ctk.CTkFrame,
    ):
        """Inicializa o gerenciador de toasts.

        Args:
            main_window: Janela principal (CTk)
            notifications_frame: Frame para notificações
            main_frame: Frame principal (para posicionar before)
        """
        self.main_window = main_window
        self._notifications_frame = notifications_frame
        self._main_frame = main_frame
        self._toast_label: ctk.CTkLabel | None = None

    def show_toast(
        self, message: str, success: bool = True, duration: int = 2000
    ) -> None:
        """Exibe toast notification temporal.

        Args:
            message: Mensagem a exibir
            success: True para verde (sucesso), False para vermelho (erro)
            duration: Duração em ms
        """
        try:
            # Empacotar o frame de notificações se ainda não está empacotado
            if not self._notifications_frame.winfo_viewable():
                self._notifications_frame.pack(
                    fill="x", padx=10, pady=(5, 0), before=self._main_frame
                )

            # Limpar toasts antigos
            for widget in self._notifications_frame.winfo_children():
                widget.destroy()

            # Criar novo toast
            self._toast_label = ctk.CTkLabel(
                self._notifications_frame,
                text=message,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#FFFFFF",
                fg_color=COLORS["accent_green"] if success else COLORS["accent_red"],
                corner_radius=6,
            )
            self._toast_label.pack(pady=5, padx=10)
            self.main_window.update()

            # Auto-hide após duration
            self.main_window.after(duration, lambda: self.hide_toast())
        except Exception as e:
            logger.error(f"Erro ao mostrar toast: {e}", exc_info=True)

    def hide_toast(self) -> None:
        """Esconde toast e unpack do frame se vazio."""
        try:
            # Limpar todos os widgets do frame
            for widget in self._notifications_frame.winfo_children():
                widget.destroy()

            # Se frame ficou vazio, fazer unpack para não ocupar espaço
            if not self._notifications_frame.winfo_children():
                self._notifications_frame.pack_forget()
        except Exception as e:
            logger.debug(f"Erro ao esconder toast: {e}")
