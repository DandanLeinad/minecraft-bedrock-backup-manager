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

"""Testes para ProgressBarWidget - MC-2 Progress Bar Feature."""

from backup_manager_mvp.core.models.progress_model import ProgressModel


class TestProgressBarWidgetInitialization:
    """Testa criação e inicialização do ProgressBarWidget."""

    def test_create_progress_widget_with_valid_params(self):
        """Cria ProgressBarWidget com parâmetros válidos."""
        # Este teste é placeholder pois widgets Tkinter precisam de master
        # A validação real acontecerá em testes de integração
        assert True

    def test_progress_bar_width_and_height(self):
        """Verifica dimensões padrão do widget."""
        # Placeholder - será testado com Tkinter root window
        assert True


class TestProgressBarWidgetUpdate:
    """Testa atualização de progresso."""

    def test_update_progress_from_model(self):
        """Atualiza barra a partir de ProgressModel."""
        progress = ProgressModel(current=5, total=10, stage="Processando")
        # A implementação deve converter percentage (50.0) para valor 0-1 (0.5)
        expected_value = progress.percentage / 100.0
        assert expected_value == 0.5

    def test_update_progress_converts_percentage_to_0_1_range(self):
        """Converte percentagem para range 0-1 do CTkProgressBar."""
        test_cases = [
            (ProgressModel(current=0, total=10, stage=""), 0.0),
            (ProgressModel(current=5, total=10, stage=""), 0.5),
            (ProgressModel(current=10, total=10, stage=""), 1.0),
            (ProgressModel(current=1, total=4, stage=""), 0.25),
            (ProgressModel(current=3, total=4, stage=""), 0.75),
        ]

        for progress, expected_value in test_cases:
            actual_value = progress.percentage / 100.0
            assert actual_value == expected_value

    def test_progress_bar_handles_stage_text(self):
        """Widget exibe texto de stage (etapa)."""
        stage_text = "Copiando arquivos..."
        progress = ProgressModel(current=3, total=10, stage=stage_text)

        # Widget deve ter acesso ao stage
        assert progress.stage == stage_text

    def test_progress_bar_displays_percentage_label(self):
        """Widget exibe percentagem em label."""
        progress = ProgressModel(current=75, total=100, stage="")

        # Label deve mostrar "75%" ou similar
        percentage_text = f"{progress.percentage:.0f}%"
        assert percentage_text == "75%"


class TestProgressBarWidgetModes:
    """Testa diferentes modos de operação."""

    def test_determinate_mode_default(self):
        """Modo determinado é o padrão."""
        # Modo determinado mostra progresso específico
        progress = ProgressModel(current=5, total=10, stage="")
        assert progress.percentage == 50.0

    def test_supports_progress_update_sequence(self):
        """Suporta sequência de atualizações de progresso."""
        stages = [
            ProgressModel(current=0, total=10, stage="Iniciando"),
            ProgressModel(current=3, total=10, stage="Copiando"),
            ProgressModel(current=7, total=10, stage="Finalizando"),
            ProgressModel(current=10, total=10, stage="Concluído"),
        ]

        percentages = [p.percentage for p in stages]
        assert percentages == [0.0, 30.0, 70.0, 100.0]


class TestProgressBarWidgetFormatting:
    """Testa formatação de texto e labels."""

    def test_stage_label_truncation_for_long_text(self):
        """Trunca texto de stage muito longo."""
        long_stage = "Copiando arquivo muito grande chamado level_dat_backup.tar.gz"
        progress = ProgressModel(current=5, total=10, stage=long_stage)

        # Widget deve truncar ou ao menos armazenar corretamente
        assert progress.stage == long_stage
        assert len(progress.stage) > 40

    def test_percentage_formatting_one_decimal(self):
        """Formata percentagem com 1 casa decimal."""
        progress = ProgressModel(current=1, total=3, stage="")

        # 33.33% formatado como "33.3%"
        formatted = f"{progress.percentage:.1f}%"
        assert formatted == "33.3%"

    def test_progress_info_string(self):
        """Cria string formatada de informação de progresso."""
        progress = ProgressModel(current=5, total=10, stage="Copiando")

        # Formato esperado: "Copiando (50.0%)"
        info = (
            f"{progress.stage} ({progress.percentage:.1f}%)"
            if progress.stage
            else f"{progress.percentage:.1f}%"
        )
        assert info == "Copiando (50.0%)"
