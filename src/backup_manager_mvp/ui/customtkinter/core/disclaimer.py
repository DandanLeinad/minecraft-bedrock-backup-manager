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

"""Dialog de disclaimer obrigatório."""

import logging

import customtkinter as ctk

from backup_manager_mvp.ui.customtkinter.constants import COLORS

logger = logging.getLogger(__name__)


class DisclaimerDialog:
    """Dialog com aviso legal e MVP."""

    def __init__(self, parent_window: ctk.CTk):
        """Inicializa o dialog.

        Args:
            parent_window: Janela pai (CTk principal)
        """
        self.parent_window = parent_window
        self.disclaimer_window: ctk.CTkToplevel | None = None

    def show(self) -> bool:
        """Exibe o dialog e aguarda resposta.

        Returns:
            True se aceito, False se rejeitado
        """
        # Criar janela de disclaimer
        self.disclaimer_window = ctk.CTkToplevel(self.parent_window)
        self.disclaimer_window.title("Aviso Importante")
        self.disclaimer_window.geometry("600x450")
        self.disclaimer_window.resizable(False, False)
        self.disclaimer_window.grab_set()

        # Centralizar janela
        self.disclaimer_window.transient(self.parent_window)

        # === CONTEÚDO ===
        container = ctk.CTkScrollableFrame(
            self.disclaimer_window,
            fg_color=("gray95", "gray15"),
            orientation="vertical",
        )
        container.pack(fill="both", expand=True, padx=24, pady=24)

        # === TÍTULO ===
        title = ctk.CTkLabel(
            container,
            text="Aviso Legal e de Produto",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray10", "gray90"),
        )
        title.pack(anchor="w", pady=(0, 16))

        # === AVISO MINECRAFT - DESTAQUE ===
        legal_frame = ctk.CTkFrame(
            container,
            fg_color=COLORS["accent_red"],
            border_width=0,
            corner_radius=8,
        )
        legal_frame.pack(fill="x", pady=(0, 16))

        legal_text = ctk.CTkLabel(
            legal_frame,
            text="NOT AN OFFICIAL MINECRAFT PRODUCT\nNOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="white",
            justify="center",
            wraplength=500,
            fg_color="transparent",
        )
        legal_text.pack(padx=16, pady=16)

        # === DESCRIÇÃO LEGAL ===
        legal_desc = ctk.CTkLabel(
            container,
            text="Este software é uma ferramenta independente para gerenciar backups do Minecraft Bedrock Edition. Não é afiliado, endossado ou aprovado pela Mojang Studios ou Microsoft Corporation.",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray65"),
            justify="left",
            wraplength=500,
            fg_color="transparent",
        )
        legal_desc.pack(anchor="w", pady=(0, 24))

        # === SEPARADOR ===
        separator = ctk.CTkFrame(container, height=1, fg_color=("gray70", "gray40"))
        separator.pack(fill="x", pady=16)

        # === AVISO MVP ===
        mvp_label = ctk.CTkLabel(
            container,
            text="Fase MVP / Teste (Alpha)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["accent_orange"],
            fg_color="transparent",
        )
        mvp_label.pack(anchor="w", pady=(0, 8))

        mvp_desc = ctk.CTkLabel(
            container,
            text="Este é um protótipo em fase de testes. Algumas funcionalidades podem não estar completamente implementadas ou estáveis. Use por sua conta e risco e sempre mantenha cópias de segurança dos seus dados importantes.",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray65"),
            justify="left",
            wraplength=500,
            fg_color="transparent",
        )
        mvp_desc.pack(anchor="w")

        # === BOTÃO DE ACEITAR ===
        button_frame = ctk.CTkFrame(self.disclaimer_window, fg_color="transparent")
        button_frame.pack(fill="x", padx=24, pady=(0, 24))

        accept_btn = ctk.CTkButton(
            button_frame,
            text="Entendi e Continuar",
            command=self.disclaimer_window.destroy,
            height=40,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=COLORS["accent_green"],
            hover_color=("#00A840", "#00A840"),
            text_color="white",
        )
        accept_btn.pack(fill="x")

        # Aguardar fechamento do disclaimer
        self.disclaimer_window.update()
        self.parent_window.wait_window(self.disclaimer_window)

        return True
