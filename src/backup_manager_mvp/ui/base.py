# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Núcleo de abstração para UI - permitindo migração entre frameworks."""

from abc import ABC, abstractmethod
from collections.abc import Callable

from backup_manager_mvp.core.models.backup_model import BackupModel
from backup_manager_mvp.core.models.world_model import WorldModel


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
