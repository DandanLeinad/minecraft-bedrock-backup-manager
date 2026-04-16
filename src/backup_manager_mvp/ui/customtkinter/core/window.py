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

"""Gerenciador da janela principal."""

import logging

import customtkinter as ctk

from backup_manager_mvp.ui.customtkinter.constants import (
    APP_TITLE,
    COLORS,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_PREFERRED_HEIGHT,
    WINDOW_PREFERRED_WIDTH,
)
from backup_manager_mvp.utils.version import __version__

logger = logging.getLogger(__name__)


class WindowManager:
    """Gerencia a criação e configuração da janela principal."""

    def __init__(self):
        """Inicializa o gerenciador de janela."""
        self.main_window: ctk.CTk | None = None
        self._main_frame: ctk.CTkFrame | None = None
        self._notifications_frame: ctk.CTkFrame | None = None

    def create_main_window(self) -> ctk.CTk:
        """Cria e configura a janela principal.

        Returns:
            Janela CTk criada
        """
        self.main_window = ctk.CTk()
        self.main_window.title(APP_TITLE)
        self.main_window.geometry(f"{WINDOW_PREFERRED_WIDTH}x{WINDOW_PREFERRED_HEIGHT}")
        self.main_window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # === FOOTER COM DISCLAIMER ===
        self._setup_footer()

        # === FRAME DE NOTIFICAÇÕES (EMPACOTADO APENAS QUANDO HÁ TOAST) ===
        self._setup_notifications_frame()

        # === FRAME PRINCIPAL ===
        self._setup_main_frame()

        return self.main_window

    def _setup_footer(self) -> None:
        """Cria o footer com disclaimer e versão."""
        footer_frame = ctk.CTkFrame(
            self.main_window,
            fg_color=COLORS["accent_red"],
            border_width=0,
            height=28,
        )
        footer_frame.pack(fill="x", padx=0, pady=0, side="bottom")

        # === DISCLAIMER (ESQUERDA) ===
        disclaimer_label = ctk.CTkLabel(
            footer_frame,
            text="NOT AN OFFICIAL MINECRAFT PRODUCT  •  NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT",
            font=ctk.CTkFont(size=9),
            text_color="white",
            fg_color="transparent",
        )
        disclaimer_label.pack(side="left", expand=True, pady=4, padx=10)

        # === VERSÃO (DIREITA) ===
        version_label = ctk.CTkLabel(
            footer_frame,
            text=f"Version {__version__}",
            font=ctk.CTkFont(size=8),
            text_color="white",
            fg_color="transparent",
        )
        version_label.pack(side="right", pady=4, padx=10)

    def _setup_notifications_frame(self) -> None:
        """Cria o frame para notificações."""
        self._notifications_frame = ctk.CTkFrame(
            self.main_window, fg_color="transparent"
        )
        # NÃO empacotar aqui - apenas quando houver notificação

    def _setup_main_frame(self) -> None:
        """Cria o frame principal."""
        self._main_frame = ctk.CTkFrame(self.main_window)
        self._main_frame.pack(fill="both", expand=True, padx=0, pady=0)

    def get_main_window(self) -> ctk.CTk:
        """Retorna a janela principal.

        Returns:
            Janela CTk
        """
        return self.main_window

    def get_main_frame(self) -> ctk.CTkFrame:
        """Retorna o frame principal.

        Returns:
            Frame principal
        """
        return self._main_frame

    def get_notifications_frame(self) -> ctk.CTkFrame:
        """Retorna o frame de notificações.

        Returns:
            Frame de notificações
        """
        return self._notifications_frame
