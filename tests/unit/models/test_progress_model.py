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

"""Testes para ProgressModel - MC-2 Progress Bar Feature."""

import pytest

from backup_manager_mvp.models.progress_model import ProgressModel


class TestProgressModelInitialization:
    """Testa criação e inicialização do ProgressModel."""

    def test_create_progress_model_with_valid_data(self):
        """Cria ProgressModel com dados válidos."""
        progress = ProgressModel(current=5, total=10, stage="Copiando arquivos")

        assert progress.current == 5
        assert progress.total == 10
        assert progress.stage == "Copiando arquivos"

    def test_progress_model_percentage_calculation(self):
        """Calcula percentagem corretamente."""
        progress = ProgressModel(current=5, total=10, stage="Processando")

        # 5/10 = 50%
        assert progress.percentage == 50.0

    def test_progress_model_0_percent(self):
        """Calcula 0% quando current=0."""
        progress = ProgressModel(current=0, total=10, stage="Iniciando")

        assert progress.percentage == 0.0

    def test_progress_model_100_percent(self):
        """Calcula 100% quando current==total."""
        progress = ProgressModel(current=10, total=10, stage="Concluído")

        assert progress.percentage == 100.0

    def test_progress_model_partial_percentage(self):
        """Calcula percentagens intermediárias corretamente."""
        # 1/4 = 25%
        assert ProgressModel(current=1, total=4, stage="").percentage == 25.0
        # 3/4 = 75%
        assert ProgressModel(current=3, total=4, stage="").percentage == 75.0

    def test_progress_model_zero_total_raises_error(self):
        """Levanta erro quando total é zero."""
        with pytest.raises(ValueError, match="total deve ser maior que 0"):
            ProgressModel(current=0, total=0, stage="")

    def test_progress_model_negative_current_raises_error(self):
        """Levanta erro quando current é negativo."""
        with pytest.raises(ValueError, match="current não pode ser negativo"):
            ProgressModel(current=-1, total=10, stage="")

    def test_progress_model_current_exceeds_total(self):
        """Permite current > total mas limita percentage a 100%."""
        progress = ProgressModel(current=15, total=10, stage="")

        # Deve retornar 100% como máximo
        assert progress.percentage == 100.0

    def test_progress_model_empty_stage(self):
        """Aceita stage vazio."""
        progress = ProgressModel(current=1, total=10, stage="")

        assert progress.stage == ""

    def test_progress_model_is_complete(self):
        """Verifica se progresso é completo (current == total)."""
        assert ProgressModel(current=10, total=10, stage="").is_complete() is True
        assert ProgressModel(current=5, total=10, stage="").is_complete() is False

    def test_progress_model_percentage_precision(self):
        """Calcula percentagem com precisão de 1 casa decimal."""
        # 1/3 ≈ 33.33...%
        progress = ProgressModel(current=1, total=3, stage="")

        # Deve ter no máximo 2 casas decimais
        assert round(progress.percentage, 2) == 33.33
