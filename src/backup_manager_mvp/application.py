# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Application Controller - Orquestra serviços e UI."""

import logging
import threading

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.progress_model import ProgressModel
from backup_manager_mvp.core.models.world_model import WorldModel
from backup_manager_mvp.core.services.backup_service import BackupService
from backup_manager_mvp.core.services.world_service import WorldService
from backup_manager_mvp.infra.repository import (
    FileSystemBackupRepository,
    FileSystemWorldRepository,
)
from backup_manager_mvp.ui import CustomTkinterUIController

logger = logging.getLogger(__name__)


class BackupManagerApp:
    """Orquestrador principal da aplicação.

    Coordena os serviços (WorldService, BackupService) com a UI (UIController).
    Implementa o padrão Application Controller.
    """

    def __init__(self):
        """Inicializa a aplicação com serviços e UI."""
        self.world_service = WorldService(FileSystemWorldRepository())
        self.backup_service = BackupService(FileSystemBackupRepository())
        self.ui = CustomTkinterUIController(app=self)

        # Conectar callbacks da UI aos handlers da aplicação
        self.ui.set_callback_world_selected(self._handle_world_selected)
        self.ui.set_callback_create_backup(self._handle_create_backup)
        self.ui.set_callback_restore_backup(self._handle_restore_backup)
        self.ui.set_callback_back(self._handle_back)

        # Estado da navegação
        self.current_world: WorldModel | None = None

    def run(self):
        """Inicia a aplicação."""
        try:
            logger.info("Iniciando aplicação...")
            logger.info("UI iniciada com sucesso")
            self.ui.run()
        except Exception as e:
            logger.error(f"Erro ao iniciar aplicação: {e}", exc_info=True)

    def get_worlds_list(self) -> list[WorldModel]:
        """Retorna lista de mundos (chamado por UI ao inicializar)."""
        worlds = self.world_service.list_worlds()
        logger.info(f"Listados {len(worlds)} mundo(s)")
        return worlds

    def _refresh_worlds_list(self) -> None:
        """Atualiza e exibe a tela de lista de mundos."""
        try:
            worlds = self.world_service.list_worlds()
            logger.info(f"Listados {len(worlds)} mundo(s)")
            self.ui.show_screen_worlds_list(worlds)
        except Exception as e:
            logger.error(f"Erro ao listar mundos: {e}", exc_info=True)
            self.ui.show_error_dialog(
                "Erro ao listar mundos", f"Não foi possível listar os mundos: {e!s}"
            )

    def _handle_world_selected(self, world: WorldModel) -> None:
        """Chamado quando um mundo é selecionado."""
        if world is None:
            logger.warning("Mundo selecionado é None")
            self.ui.show_error_dialog("Erro", "Mundo selecionado é None. Tente novamente.")
            return

        logger.info(f"Mundo selecionado: {world.levelname}")
        self.current_world = world
        try:
            backups = self.backup_service.list_backups(world)
            logger.info(f"Encontrados {len(backups)} backup(s) para {world.levelname}")
            self.ui.show_screen_world_details(world, backups)
        except Exception as e:
            logger.error(f"Erro ao carregar detalhes do mundo: {e}", exc_info=True)
            self.ui.show_error_dialog(
                "Erro ao carregar detalhes",
                f"Erro ao carregar informações do mundo: {e!s}",
            )

    def _handle_create_backup(self, world: WorldModel) -> None:
        """Chamado quando usuário clica 'Fazer Backup Agora'.

        Executa o backup em uma thread de background para não bloquear a UI.
        """
        logger.info(f"Iniciando backup em background para: {world.levelname}")

        # Mostrar barra de progresso e desabilitar botões (na thread principal)
        self.ui.show_progress_bar()
        self.ui.disable_buttons()

        # Criar callback de progresso que usa after() para thread-safety
        def on_progress(progress: ProgressModel) -> None:
            if self.ui.main_window:
                self.ui.main_window.after(0, lambda: self.ui.update_progress(progress))

        # Executar backup em background thread
        def run_backup() -> None:
            try:
                backup = self.backup_service.create_backup(world, progress_callback=on_progress)
                logger.info(f"Backup criado com sucesso: {backup.backup_path}")

                # Sucesso: agendar UI updates na thread principal
                def on_success() -> None:
                    self.ui.hide_progress_bar()
                    self.ui.enable_buttons()

                    self.ui.show_info_dialog(
                        "✅ Backup Criado com Sucesso!",
                        f"O backup do mundo '{world.levelname}' foi criado com sucesso!\n\n📁 Local: {backup.backup_path}\n\n💾 Tamanho: {backup.size_display}",
                    )
                    # Recarregar a lista de backups
                    backups = self.backup_service.list_backups(world)
                    self.ui.show_screen_world_details(world, backups)

                if self.ui.main_window:
                    self.ui.main_window.after(0, on_success)

            except Exception as exc:
                logger.error(f"Erro ao criar backup: {exc}", exc_info=True)

                # Erro: agendar UI updates na thread principal
                def on_error(err=exc) -> None:
                    self.ui.hide_progress_bar()
                    self.ui.enable_buttons()

                    self.ui.show_error_dialog(
                        "❌ Erro ao Criar Backup",
                        f"Não foi possível criar o backup: {err!s}\n\n🔍 Verifique:\n• As permissões da pasta\n• Espaço em disco disponível\n• Se o mundo está sendo usado",
                    )

                if self.ui.main_window:
                    self.ui.main_window.after(0, on_error)

        # Iniciar thread de background
        thread = threading.Thread(target=run_backup, daemon=True)
        thread.start()

    def _handle_restore_backup(self, backup: BackupModel, world: WorldModel) -> None:
        """Chamado quando usuário confirma restauração.

        Executa a restauração em uma thread de background para não bloquear a UI.
        """
        logger.info(f"Iniciando restauração em background para: {world.levelname}")

        # Mostrar barra de progresso e desabilitar botões (na thread principal)
        self.ui.show_progress_bar()
        self.ui.disable_buttons()

        # Criar callback de progresso que usa after() para thread-safety
        def on_progress(progress) -> None:  # progress: ProgressModel
            if self.ui.main_window:
                self.ui.main_window.after(0, lambda: self.ui.update_progress(progress))

        # Executar restauração em background thread
        def run_restore() -> None:
            try:
                self.backup_service.restore_backup(backup, world, progress_callback=on_progress)
                logger.info(f"Backup restaurado com sucesso para {world.levelname}")

                # Sucesso: agendar UI updates na thread principal
                def on_success() -> None:
                    self.ui.hide_progress_bar()
                    self.ui.enable_buttons()

                    self.ui.show_info_dialog(
                        "✅ Backup Restaurado com Sucesso!",
                        f"✨ O mundo '{world.levelname}' foi restaurado com sucesso!\n\n🎮 Você pode abrir o Minecraft agora para ver as alterações.\n\n⚡ Dica: Faça um novo backup se quiser manter o progresso atual.",
                    )
                    # ✅ Voltar para a tela de backups do MESMO mundo (não para lista de mundos)
                    backups = self.backup_service.list_backups(world)
                    self.ui.show_screen_world_details(world, backups)

                if self.ui.main_window:
                    self.ui.main_window.after(0, on_success)

            except Exception as exc:
                logger.error(f"Erro ao restaurar backup: {exc}", exc_info=True)

                # Erro: agendar UI updates na thread principal
                def on_error(err=exc) -> None:
                    self.ui.hide_progress_bar()
                    self.ui.enable_buttons()

                    self.ui.show_error_dialog(
                        "❌ Erro ao Restaurar Backup",
                        f"Não foi possível restaurar o mundo: {err!s}\n\n🔍 Verifique:\n• As permissões da pasta\n• Se o mundo está bloqueado\n• Espaço em disco disponível",
                    )

                if self.ui.main_window:
                    self.ui.main_window.after(0, on_error)

        # Iniciar thread de background
        thread = threading.Thread(target=run_restore, daemon=True)
        thread.start()

    def _handle_back(self) -> None:
        """Chamado quando usuário clica voltar/cancelar."""
        if self.current_world:
            # Se estávamos em detalhes, voltar para lista
            self._refresh_worlds_list()
            self.current_world = None
