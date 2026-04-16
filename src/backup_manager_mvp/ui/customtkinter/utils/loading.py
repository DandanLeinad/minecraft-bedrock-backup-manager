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

"""Loading indicator utilities with spinner animation."""

import logging

import customtkinter as ctk

logger = logging.getLogger(__name__)

# Spinner frames (Braille characters for smooth animation)
SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


class LoadingSpinner:
    """Gerencia animação de spinner para loading."""

    def __init__(self):
        """Inicializa spinner."""
        self.spinner_index = 0
        self.loading_label: ctk.CTkLabel | None = None

    def update(self) -> None:
        """Atualiza animação do spinner."""
        if self.loading_label and self.loading_label.winfo_exists():
            self.spinner_index = (self.spinner_index + 1) % len(SPINNER_FRAMES)
            spinner_char = SPINNER_FRAMES[self.spinner_index]
            current_text = self.loading_label.cget("text")

            # Remover spinner anterior
            if current_text and current_text[0] in SPINNER_FRAMES:
                new_text = current_text[2:]  # Remove "⠋ "
            else:
                new_text = current_text or "Processando..."

            self.loading_label.configure(text=f"{spinner_char} {new_text}")
            # Schedule next update (80ms)
            self.loading_label.after(80, self.update)


def show_loading(
    main_frame: ctk.CTkFrame,
    message: str = "Processando...",
    spinner: LoadingSpinner | None = None,
) -> tuple[ctk.CTkLabel, LoadingSpinner]:
    """Exibe label de loading com spinner animado.

    Args:
        main_frame: Frame pai
        message: Mensagem a exibir
        spinner: Spinner existente (pode ser None)

    Returns:
        Tuple (loading_label, spinner) para reutilização
    """
    logger.debug(f"Loading: {message}")
    try:
        if spinner is None:
            spinner = LoadingSpinner()

        if not spinner.loading_label:
            spinner.loading_label = ctk.CTkLabel(
                main_frame,
                text=f"{SPINNER_FRAMES[0]} {message}",
                font=ctk.CTkFont(size=12),
            )
        else:
            spinner.loading_label.configure(text=f"{SPINNER_FRAMES[0]} {message}")

        spinner.loading_label.pack(pady=20)
        spinner.update()  # Iniciar animação
        main_frame.update()
        return spinner.loading_label, spinner
    except Exception as e:
        logger.error(f"Erro ao mostrar loading: {e}", exc_info=True)
        return None, spinner


def hide_loading(loading_label: ctk.CTkLabel | None) -> None:
    """Esconde label de loading.

    Args:
        loading_label: Label do loading a esconder
    """
    logger.debug("Loading hidden")
    try:
        if loading_label and loading_label.winfo_exists():
            loading_label.pack_forget()
    except Exception as e:
        logger.debug(f"Erro ao esconder loading: {e}")
