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

"""Gerenciador de loading spinner."""

import logging

import customtkinter as ctk

logger = logging.getLogger(__name__)


class LoadingManager:
    """Gerencia animação de loading com spinner."""

    def __init__(self, main_window: ctk.CTk, main_frame: ctk.CTkFrame):
        """Inicializa o gerenciador de loading.

        Args:
            main_window: Janela principal (CTk)
            main_frame: Frame principal para exibir spinner
        """
        self.main_window = main_window
        self._main_frame = main_frame
        self._loading_label: ctk.CTkLabel | None = None
        self._spinner_index = 0
        self._spinner_frames = [
            "⠋",
            "⠙",
            "⠹",
            "⠸",
            "⠼",
            "⠴",
            "⠦",
            "⠧",
            "⠇",
            "⠏",
        ]

    def _update_spinner(self) -> None:
        """Atualiza animação do spinner."""
        if self._loading_label and self._loading_label.winfo_exists():
            self._spinner_index = (self._spinner_index + 1) % len(self._spinner_frames)
            spinner_char = self._spinner_frames[self._spinner_index]
            current_text = self._loading_label.cget("text")
            # Remover spinner anterior
            if current_text and current_text[0] in self._spinner_frames:
                new_text = current_text[2:]  # Remove "⠋ "
            else:
                new_text = current_text or "Processando..."
            self._loading_label.configure(text=f"{spinner_char} {new_text}")
            self.main_window.after(80, self._update_spinner)

    def show_loading(self, message: str = "Processando...") -> None:
        """Exibe label de loading com spinner animado.

        Args:
            message: Mensagem a exibir
        """
        logger.debug(f"Loading: {message}")
        try:
            # Se label existe mas foi destruído, recriar
            if self._loading_label and not self._loading_label.winfo_exists():
                self._loading_label = None

            if not self._loading_label:
                self._loading_label = ctk.CTkLabel(
                    self._main_frame,
                    text=f"{self._spinner_frames[0]} {message}",
                    font=ctk.CTkFont(size=12),
                )

            if self._loading_label and self._loading_label.winfo_exists():
                self._loading_label.configure(
                    text=f"{self._spinner_frames[0]} {message}"
                )
                self._loading_label.pack(pady=20)
                self._update_spinner()  # Iniciar animação
                self.main_window.update()
        except Exception as e:
            logger.error(f"Erro ao mostrar loading: {e}", exc_info=True)

    def hide_loading(self) -> None:
        """Esconde label de loading."""
        logger.debug("Loading hidden")
        try:
            if self._loading_label and self._loading_label.winfo_exists():
                self._loading_label.pack_forget()
        except Exception as e:
            logger.debug(f"Erro ao esconder loading: {e}")
        self.main_window.update()
