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

"""Modelo para rastrear progresso de operações (backup/restore)."""

from dataclasses import dataclass


@dataclass
class ProgressModel:
    """Modelo para rastrear progresso de uma operação.

    Genérico e reutilizável para qualquer serviço (backup, restore, cloud sync, etc).

    Attributes:
        current: Número de itens processados
        total: Número total de itens
        stage: Descrição da etapa atual (ex: "Copiando arquivos...")

    Raises:
        ValueError: Se current < 0 ou total <= 0
    """

    current: int
    total: int
    stage: str = ""

    def __post_init__(self) -> None:
        """Validação após inicialização."""
        if self.current < 0:
            raise ValueError("current não pode ser negativo")
        if self.total <= 0:
            raise ValueError("total deve ser maior que 0")

    @property
    def percentage(self) -> float:
        """Calcula o percentual de progresso (0-100).

        Returns:
            float: Percentual de conclusão (0.0 a 100.0), limitado a 100%

        Example:
            >>> progress = ProgressModel(current=5, total=10, stage="Processando")
            >>> progress.percentage
            50.0
        """
        percentage = (self.current / self.total) * 100.0
        # Limitar a 100% como máximo
        return min(percentage, 100.0)

    def is_complete(self) -> bool:
        """Verifica se a operação está completa.

        Returns:
            bool: True se current == total

        Example:
            >>> progress = ProgressModel(current=10, total=10, stage="Pronto")
            >>> progress.is_complete()
            True
        """
        return self.current == self.total
