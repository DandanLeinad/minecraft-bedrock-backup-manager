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

"""Implementação da UI em CustomTkinter para Backup Manager MVP.

Baseada em CustomTkinter 5.2.2 oficial:
- CTk (janela principal)
- CTkFrame (containers)
- CTkScrollableFrame (conteúdo scrollável)
- CTkLabel (texto)
- CTkButton (botões)
- messagebox (dialogs - Tkinter padrão)
"""

import logging
from collections.abc import Callable

import customtkinter as ctk

from backup_manager_mvp.config.feature_flags import FEATURE_FLAGS
from backup_manager_mvp.models.backup_model import BackupModel
from backup_manager_mvp.models.progress_model import ProgressModel
from backup_manager_mvp.models.world_model import WorldModel
from backup_manager_mvp.ui.base import UIController
from backup_manager_mvp.ui.customtkinter.cache import BackupCache
from backup_manager_mvp.ui.customtkinter.core import DisclaimerDialog, WindowManager
from backup_manager_mvp.ui.customtkinter.handlers import (
    on_back,
    on_cancel_restore,
    on_restore_backup,
    on_world_selected,
)
from backup_manager_mvp.ui.customtkinter.loading import LoadingManager
from backup_manager_mvp.ui.customtkinter.notifications import ToastManager
from backup_manager_mvp.ui.customtkinter.progress_widget import ProgressBarWidget
from backup_manager_mvp.ui.customtkinter.screens import (
    show_screen_restore_confirmation,
    show_screen_restore_preview,
    show_screen_world_details,
    show_screen_worlds_list,
)
from backup_manager_mvp.ui.customtkinter.theme import configure_theme

logger = logging.getLogger(__name__)

# === CONFIGURAR TEMA ===
configure_theme()


# ========== WIDGETS CUSTOMIZADOS ==========

# Não há widgets customizados necessários - usar apenas CTkFrame, CTkLabel, CTkButton direto


# ========== CONTROLADOR PRINCIPAL ==========


class CustomTkinterUIController(UIController):
    """Controlador de UI usando CustomTkinter 5.2.2 oficial.

    Widgets utilizados (confirmados na documentação oficial):
    - CTk (janela principal)
    - CTkFrame (containers)
    - CTkScrollableFrame (áreas scrolláveis)
    - CTkLabel (texto)
    - CTkButton (botões)
    - messagebox (dialogs Tkinter padrão)

    Telas:
    1. Lista de mundos
    2. Detalhes do mundo
    3. Confirmação de restauração (modal)
    """

    def __init__(self, app=None):
        """Inicializa o controlador CustomTkinter."""
        self.app = app
        self.main_window: ctk.CTk | None = None

        # === MANAGERS ===
        self._window_manager: WindowManager | None = None
        self._toast_manager: ToastManager | None = None
        self._loading_manager: LoadingManager | None = None
        self._disclaimer_dialog: DisclaimerDialog | None = None
        self._progress_widget: ProgressBarWidget | None = None

        # === CALLBACKS ===
        self._callback_world_selected: Callable[[WorldModel], None] | None = None
        self._callback_create_backup: Callable[[WorldModel], None] | None = None
        self._callback_restore_backup: Callable[[BackupModel, WorldModel], None] | None = None
        self._callback_back: Callable[[], None] | None = None

        # === ESTADO ===
        self._current_world: WorldModel | None = None
        self._current_backup: BackupModel | None = None
        self._worlds_list: list[WorldModel] = []
        self._backups_list: list[BackupModel] = []
        self._buttons_enabled = True

        # === COMPONENTES REUTILIZÁVEIS ===
        self._backup_create_btn: ctk.CTkButton | None = None
        self._sync_btn: ctk.CTkButton | None = None
        self._main_frame: ctk.CTkFrame | None = None

        # === CACHE ===
        self._backup_cache = BackupCache(ttl_seconds=60)

    def run(self) -> None:
        """Inicia a aplicação CustomTkinter."""
        # === CRIAR JANELA PRINCIPAL ===
        self._window_manager = WindowManager()
        self.main_window = self._window_manager.create_main_window()
        self._main_frame = self._window_manager.get_main_frame()

        # === INICIALIZAR MANAGERS ===
        self._toast_manager = ToastManager(
            self.main_window,
            self._window_manager.get_notifications_frame(),
            self._main_frame,
        )
        self._loading_manager = LoadingManager(self.main_window, self._main_frame)

        # === MOSTRAR DISCLAIMER ===
        self._disclaimer_dialog = DisclaimerDialog(self.main_window)
        self._disclaimer_dialog.show()

        # === CARREGAR MUNDOS APÓS ACEITAR ===
        if self.app and hasattr(self.app, "get_worlds_list"):
            try:
                worlds = self.app.get_worlds_list()
                self.show_screen_worlds_list(worlds)
            except Exception as e:
                logger.error(f"Erro ao carregar mundos: {e}", exc_info=True)
                self.show_error_dialog(
                    "Erro ao carregar",
                    f"Erro ao carregar lista de mundos: {e!s}",
                )

        self.main_window.mainloop()

    def _clear_frame(self, frame: ctk.CTkFrame) -> None:
        """Limpa todos os widgets de um frame."""
        for widget in frame.winfo_children():
            # Não apagar _loading_label, _toast_label e _progress_widget se estiverem visíveis
            if (
                widget is not self._loading_label
                and widget is not self._toast_label
                and widget is not self._progress_widget
            ):
                widget.destroy()

    # ========== TELAS ==========

    def show_screen_worlds_list(self, worlds: list[WorldModel]) -> None:
        """Exibe tela 1: Lista de mundos (delegado ao módulo extraído)."""
        # Esconder barra de progresso quando muda de tela
        self.hide_progress_bar()

        self._worlds_list = worlds

        # Criar callback adaptado para usar self._callback_world_selected
        def handle_world_selected(world: WorldModel) -> None:
            on_world_selected(world, self._callback_world_selected)

        # Chamar função extraída
        show_screen_worlds_list(self._main_frame, worlds, handle_world_selected, self.app)

    def show_screen_world_details(self, world: WorldModel, backups: list[BackupModel]) -> None:
        """Exibe tela 2: Detalhes do mundo (delegado ao módulo extraído)."""
        # Esconder barra de progresso quando muda de tela
        self.hide_progress_bar()

        self._current_world = world
        self._backups_list = backups

        # Criar callbacks adaptados
        def handle_back() -> None:
            on_back(self._callback_back)

        def handle_backup_selected(backup: BackupModel, world: WorldModel) -> None:
            """Chamado quando usuário seleciona um backup.

            Se FF_RESTORE_PREVIEW está ativado, mostra preview do conteúdo.
            Senão, mostra confirmação direto.
            """
            if FEATURE_FLAGS.ENABLE_RESTORE_PREVIEW and self.app:
                try:
                    # Obter preview das informações do backup
                    preview_info = self.app.backup_service.get_backup_preview_info(backup)
                    # Mostrar preview
                    self.show_screen_restore_preview(world, backup, preview_info)
                except Exception as e:
                    logger.error(f"Erro ao gerar preview do backup: {e}", exc_info=True)
                    # Fallback para confirmação normal se preview falhar
                    self.show_screen_restore_confirmation(world, backup)
            else:
                # Sem flag: mostrar confirmação direto (behavior antigo)
                self.show_screen_restore_confirmation(world, backup)

        def handle_create_backup(world: WorldModel) -> None:
            if self._callback_create_backup:
                self._callback_create_backup(world)

        def handle_sync_backups(world: WorldModel) -> None:
            # Invalidar cache e recarregar
            if self._callback_world_selected:
                # Simula uma recarga ao chamar o callback de novo
                self._callback_world_selected(world)

        # Dicts para armazenar referências dos botões (para enable/disable)
        backup_create_btn_ref = {}
        sync_btn_ref = {}

        # Chamar função extraída com argumentos na ordem correta
        show_screen_world_details(
            self._main_frame,
            world,
            backups,
            handle_create_backup,
            handle_sync_backups,
            handle_backup_selected,
            handle_back,
            backup_create_btn_ref,
            sync_btn_ref,
            self._buttons_enabled,
            self.app,
        )

        # Armazenar referências dos botões para enable/disable
        self._backup_create_btn = backup_create_btn_ref.get("button")
        self._sync_btn = sync_btn_ref.get("button")

    def show_screen_restore_confirmation(self, world: WorldModel, backup: BackupModel) -> None:
        """Exibe diálogo de confirmação de restauração (delegado ao módulo extraído)."""
        # Esconder barra de progresso quando muda de tela
        self.hide_progress_bar()

        self._current_world = world
        self._current_backup = backup

        # Criar callbacks adaptados
        def handle_cancel_restore() -> None:
            if self._backups_list:
                on_cancel_restore(
                    self._backups_list,
                    world,
                    lambda w, b: self.show_screen_world_details(w, b),
                )

        def handle_restore_confirm() -> None:
            on_restore_backup(backup, world, self._callback_restore_backup)

        # Chamar função extraída
        show_screen_restore_confirmation(
            self._main_frame,
            world,
            backup,
            handle_cancel_restore,
            handle_restore_confirm,
        )

    def show_screen_restore_preview(
        self, world: WorldModel, backup: BackupModel, preview_info: dict
    ) -> None:
        """Exibe preview do conteúdo do backup antes de restaurar (FF_RESTORE_PREVIEW)."""
        # Esconder barra de progresso quando muda de tela
        self.hide_progress_bar()

        self._current_world = world
        self._current_backup = backup

        # Criar callbacks adaptados
        def handle_cancel_preview() -> None:
            if self._backups_list:
                on_cancel_restore(
                    self._backups_list,
                    world,
                    lambda w, b: self.show_screen_world_details(w, b),
                )

        def handle_restore_confirm() -> None:
            # backup e world já estão capturados no escopo (closure)
            on_restore_backup(backup, world, self._callback_restore_backup)

        # Chamar função extraída
        show_screen_restore_preview(
            self._main_frame,
            world,
            backup,
            preview_info,
            handle_cancel_preview,
            handle_restore_confirm,  # Sem argumentos
        )

    # ========== DIÁLOGOS ==========

    @staticmethod
    def _remove_emojis(text: str) -> str:
        """Remove emojis de um texto para evitar erro de encoding no Windows.

        Args:
            text: Texto que pode conter emojis

        Returns:
            Texto sem emojis
        """
        # Remove emojis comuns usados na aplicação
        emojis = ["✅", "✨", "❌", "📁", "💾", "⚠️"]
        result = text
        for emoji in emojis:
            result = result.replace(emoji, "")
        # Remove múltiplos espaços
        result = " ".join(result.split())
        return result

    def show_info_dialog(self, title: str, message: str) -> None:
        """Exibe diálogo informativo com toast."""
        # Toast rápido
        if self._toast_manager:
            self._toast_manager.show_toast(title, success=True, duration=2000)
        # Log completo (remover emojis para evitar erro de encoding no Windows)
        log_title = self._remove_emojis(title)
        log_message = self._remove_emojis(message)
        logger.info(f"{log_title}: {log_message}")

    def show_error_dialog(self, title: str, message: str) -> None:
        """Exibe diálogo de erro com toast."""
        # Toast rápido
        if self._toast_manager:
            self._toast_manager.show_toast(title, success=False, duration=3000)
        # Log completo (remover emojis para evitar erro de encoding no Windows)
        log_title = self._remove_emojis(title)
        log_message = self._remove_emojis(message)
        logger.error(f"{log_title}: {log_message}")

    # ========== LOADING ==========

    def show_loading(self, message: str = "Processando...") -> None:
        """Exibe label de loading com spinner animado."""
        if self._loading_manager:
            self._loading_manager.show_loading(message)

    def hide_loading(self) -> None:
        """Esconde label de loading."""
        if self._loading_manager:
            self._loading_manager.hide_loading()

    def show_progress_bar(self) -> None:
        """Exibe barra de progresso para operações de backup/restore."""
        logger.debug("Showing progress bar...")
        if self._progress_widget is None:
            self._progress_widget = ProgressBarWidget(self._main_frame)
            self._progress_widget.pack(fill="x", padx=20, pady=10)
        else:
            # Se o widget existe mas não está mais no container (p.ex. após _clear_frame),
            # verificar se ele ainda tem um parent
            if self._progress_widget.winfo_exists() and self._progress_widget.winfo_manager() == "":
                # Widget existe mas não está packed/gridded, re-adicionar
                self._progress_widget.pack(fill="x", padx=20, pady=10)
            elif self._progress_widget.winfo_exists():
                # Widget existe e está no container, apenas mostrar se estava escondido
                self._progress_widget.pack(fill="x", padx=20, pady=10)

        if self.main_window:
            self.main_window.update_idletasks()

    def hide_progress_bar(self) -> None:
        """Esconde barra de progresso."""
        logger.debug("Hiding progress bar...")
        if self._progress_widget and self._progress_widget.winfo_exists():
            self._progress_widget.pack_forget()

        if self.main_window:
            self.main_window.update_idletasks()

    def update_progress(self, progress: ProgressModel) -> None:
        """Atualiza a barra de progresso com dados."""
        if self._progress_widget and self._progress_widget.winfo_exists():
            self._progress_widget.update_progress(progress)

        if self.main_window:
            self.main_window.update_idletasks()

    def disable_buttons(self) -> None:
        """Desabilita botões de ação."""
        self._buttons_enabled = False
        if self._backup_create_btn and self._backup_create_btn.winfo_exists():
            self._backup_create_btn.configure(state="disabled")
        if self._sync_btn and self._sync_btn.winfo_exists():
            self._sync_btn.configure(state="disabled")
        self.main_window.update()

    def enable_buttons(self) -> None:
        """Habilita botões de ação."""
        self._buttons_enabled = True
        if self._backup_create_btn and self._backup_create_btn.winfo_exists():
            self._backup_create_btn.configure(state="normal")
        if self._sync_btn and self._sync_btn.winfo_exists():
            self._sync_btn.configure(state="normal")
        self.main_window.update()

    # ========== CALLBACKS (REGISTRO) ==========

    def set_callback_world_selected(self, callback: Callable[[WorldModel], None]) -> None:
        """Define callback para seleção de mundo."""
        self._callback_world_selected = callback

    def set_callback_create_backup(self, callback: Callable[[WorldModel], None]) -> None:
        """Define callback para criação de backup."""
        self._callback_create_backup = callback

    def set_callback_restore_backup(
        self, callback: Callable[[BackupModel, WorldModel], None]
    ) -> None:
        """Define callback para restauração."""
        self._callback_restore_backup = callback

    def set_callback_back(self, callback: Callable[[], None]) -> None:
        """Define callback para voltar."""
        self._callback_back = callback
