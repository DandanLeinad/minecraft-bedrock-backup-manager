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

"""Porta de persistencia para operacoes de mundos."""

from abc import ABC, abstractmethod
from pathlib import Path


class WorldRepositoryPort(ABC):
    """Contrato para acesso a sistema de arquivos de mundos do Minecraft."""

    @abstractmethod
    def get_worlds_base_path(self) -> Path:
        """Retorna caminho base de contas."""

    @abstractmethod
    def get_uwp_store_path(self) -> Path:
        """Retorna caminho de mundos da versao UWP."""

    @abstractmethod
    def get_shared_path(self, worlds_base_path: Path) -> Path:
        """Retorna caminho de mundos compartilhados."""

    @abstractmethod
    def path_exists(self, path: Path) -> bool:
        """Retorna se caminho existe."""

    @abstractmethod
    def list_directory(self, path: Path) -> list[Path]:
        """Lista itens de um diretorio."""

    @abstractmethod
    def is_directory(self, path: Path) -> bool:
        """Retorna se caminho e diretorio."""

    @abstractmethod
    def read_text_file(self, path: Path) -> str:
        """Le arquivo texto em UTF-8 e retorna conteudo."""

    @abstractmethod
    def calculate_total_size(self, path: Path) -> int:
        """Calcula tamanho total recursivo do diretorio em bytes."""
