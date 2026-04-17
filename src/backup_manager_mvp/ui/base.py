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

"""Núcleo de abstração para UI - permitindo migração entre frameworks."""

from abc import ABC, abstractmethod
from collections.abc import Callable

from backup_manager_mvp.models.backup_model import BackupModel
from backup_manager_mvp.models.world_model import WorldModel


class UIController(ABC):
    """Interface abstrata para controlar a UI.

    Esta classe define o contrato que qualquer implementação de UI
    (DearPyGui, Flet, etc.) deve seguir.

    Facilita migração entre frameworks mantendo a lógica de negócio
    separada da apresentação.
    """

    @abstractmethod
    def run(self) -> None:
        """Inicia a aplicação UI."""

    @abstractmethod
    def show_screen_worlds_list(self, worlds: list[WorldModel]) -> None:
        """Exibe a tela 1: Lista de mundos.

        Args:
            worlds: Lista de mundos encontrados no sistema.
        """

    @abstractmethod
    def show_screen_world_details(self, world: WorldModel, backups: list[BackupModel]) -> None:
        """Exibe a tela 2: Detalhes do mundo e seus backups.

        Args:
            world: Mundo selecionado.
            backups: Lista de backups para este mundo.
        """

    @abstractmethod
    def show_screen_restore_confirmation(self, world: WorldModel, backup: BackupModel) -> None:
        """Exibe a tela 3: Confirmação de restauração.

        Args:
            world: Mundo que será restaurado.
            backup: Backup a ser restaurado.
        """

    @abstractmethod
    def show_info_dialog(self, title: str, message: str) -> None:
        """Exibe um diálogo informativo.

        Args:
            title: Título do diálogo.
            message: Mensagem principal.
        """

    @abstractmethod
    def show_error_dialog(self, title: str, message: str) -> None:
        """Exibe um diálogo de erro.

        Args:
            title: Título do diálogo.
            message: Mensagem de erro.
        """

    @abstractmethod
    def set_callback_world_selected(self, callback: Callable[[WorldModel], None]) -> None:
        """Define callback para quando um mundo é selecionado.

        Args:
            callback: Função que será chamada com o WorldModel selecionado.
        """

    @abstractmethod
    def set_callback_create_backup(self, callback: Callable[[WorldModel], None]) -> None:
        """Define callback para quando usuário clica 'Fazer Backup Agora'.

        Args:
            callback: Função que será chamada com o WorldModel.
        """

    @abstractmethod
    def set_callback_restore_backup(
        self, callback: Callable[[BackupModel, WorldModel], None]
    ) -> None:
        """Define callback para quando usuário confirma restauração.

        Args:
            callback: Função que será chamada com (BackupModel, WorldModel).
        """

    @abstractmethod
    def set_callback_back(self, callback: Callable[[], None]) -> None:
        """Define callback para quando usuário clica botão voltar/cancelar.

        Args:
            callback: Função que será chamada sem argumentos.
        """

    @abstractmethod
    def show_loading(self, message: str = "Processando...") -> None:
        """Exibe modal de loading com mensagem.

        Args:
            message: Mensagem a ser exibida durante o processamento.
        """

    @abstractmethod
    def hide_loading(self) -> None:
        """Esconde modal de loading."""

    @abstractmethod
    def disable_buttons(self) -> None:
        """Desabilita botões de ação durante operações."""

    @abstractmethod
    def enable_buttons(self) -> None:
        """Habilita botões de ação após operações."""
