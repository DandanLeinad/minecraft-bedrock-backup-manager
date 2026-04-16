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

"""Application Controller - Orquestra serviços e UI."""

import logging

from backup_manager_mvp.models.backup_model import BackupModel
from backup_manager_mvp.models.world_model import WorldModel
from backup_manager_mvp.services.backup_service import BackupService
from backup_manager_mvp.services.world_service import WorldService
from backup_manager_mvp.ui import CustomTkinterUIController

logger = logging.getLogger(__name__)


class BackupManagerApp:
    """Orquestrador principal da aplicação.

    Coordena os serviços (WorldService, BackupService) com a UI (UIController).
    Implementa o padrão Application Controller.
    """

    def __init__(self):
        """Inicializa a aplicação com serviços e UI."""
        self.world_service = WorldService()
        self.backup_service = BackupService()
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
                "Erro ao listar mundos", f"Não foi possível listar os mundos: {str(e)}"
            )

    def _handle_world_selected(self, world: WorldModel) -> None:
        """Chamado quando um mundo é selecionado."""
        if world is None:
            logger.warning("Mundo selecionado é None")
            self.ui.show_error_dialog(
                "Erro", "Mundo selecionado é None. Tente novamente."
            )
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
                f"Erro ao carregar informações do mundo: {str(e)}",
            )

    def _handle_create_backup(self, world: WorldModel) -> None:
        """Chamado quando usuário clica 'Fazer Backup Agora'."""
        try:
            logger.info(f"Criando backup para: {world.levelname}")

            # Mostrar loading e desabilitar botões
            self.ui.show_loading(f"Criando backup de '{world.levelname}'...")
            self.ui.disable_buttons()

            backup = self.backup_service.create_backup(world)
            logger.info(f"Backup criado com sucesso: {backup.backup_path}")

            # Esconder loading e reabilitar botões
            self.ui.hide_loading()
            self.ui.enable_buttons()

            self.ui.show_info_dialog(
                "✅ Backup Criado com Sucesso!",
                f"O backup do mundo '{world.levelname}' foi criado com sucesso!\n\n📁 Local: {backup.backup_path}\n\n💾 Tamanho: {backup.size_display}",
            )
            # Recarregar a lista de backups
            backups = self.backup_service.list_backups(world)
            self.ui.show_screen_world_details(world, backups)
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}", exc_info=True)

            # Esconder loading e reabilitar botões mesmo em erro
            self.ui.hide_loading()
            self.ui.enable_buttons()

            self.ui.show_error_dialog(
                "❌ Erro ao Criar Backup",
                f"Não foi possível criar o backup: {str(e)}\n\n🔍 Verifique:\n• As permissões da pasta\n• Espaço em disco disponível\n• Se o mundo está sendo usado",
            )

    def _handle_restore_backup(self, backup: BackupModel, world: WorldModel) -> None:
        """Chamado quando usuário confirma restauração."""
        try:
            logger.info(
                f"Restaurando backup de {world.levelname} de {backup.created_at}"
            )

            # Mostrar loading e desabilitar botões
            self.ui.show_loading(
                f"Restaurando mundo '{world.levelname}'...\n\nIsso pode levar alguns minutos..."
            )
            self.ui.disable_buttons()

            self.backup_service.restore_backup(backup, world)
            logger.info(f"Backup restaurado com sucesso para {world.levelname}")

            # Esconder loading e reabilitar botões
            self.ui.hide_loading()
            self.ui.enable_buttons()

            self.ui.show_info_dialog(
                "✅ Backup Restaurado com Sucesso!",
                f"✨ O mundo '{world.levelname}' foi restaurado com sucesso!\n\n🎮 Você pode abrir o Minecraft agora para ver as alterações.\n\n⚡ Dica: Faça um novo backup se quiser manter o progresso atual.",
            )
            # ✅ Voltar para a tela de backups do MESMO mundo (não para lista de mundos)
            backups = self.backup_service.list_backups(world)
            self.ui.show_screen_world_details(world, backups)
        except Exception as e:
            logger.error(f"Erro ao restaurar backup: {e}", exc_info=True)

            # Esconder loading e reabilitar botões mesmo em erro
            self.ui.hide_loading()
            self.ui.enable_buttons()

            self.ui.show_error_dialog(
                "❌ Erro ao Restaurar Backup",
                f"Não foi possível restaurar o mundo: {str(e)}\n\n🔍 Verifique:\n• As permissões da pasta\n• Se o mundo está bloqueado\n• Espaço em disco disponível",
            )

    def _handle_back(self) -> None:
        """Chamado quando usuário clica voltar/cancelar."""
        if self.current_world:
            # Se estávamos em detalhes, voltar para lista
            self._refresh_worlds_list()
            self.current_world = None
