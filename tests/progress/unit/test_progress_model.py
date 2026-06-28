# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

import pytest

from backup_manager_mvp.core.models.progress_model import ProgressModel


class TestProgressModelInitialization:
    """Tests for ProgressModel initialization and validation.

    Rules:
    - Requires current, total, and stage parameters
    - total must be greater than 0
    - current cannot be negative
    - current exceeding total is capped at 100%
    - stage can be empty string
    """

    def test_should_create_progress_model_when_all_fields_valid(self):
        """
        ProgressModel should be created with valid current, total, and stage.
        """
        progress = ProgressModel(current=5, total=10, stage="Copying files")

        assert progress.current == 5
        assert progress.total == 10
        assert progress.stage == "Copying files"

    def test_should_calculate_percentage_correctly(self):
        """
        percentage should return correct percentage based on current/total.
        """
        progress = ProgressModel(current=5, total=10, stage="Processing")

        assert progress.percentage == 50.0

    def test_should_return_zero_percent_when_current_is_zero(self):
        """
        percentage should return 0.0 when current is 0.
        """
        progress = ProgressModel(current=0, total=10, stage="Starting")

        assert progress.percentage == 0.0

    def test_should_return_hundred_percent_when_current_equals_total(self):
        """
        percentage should return 100.0 when current equals total.
        """
        progress = ProgressModel(current=10, total=10, stage="Completed")

        assert progress.percentage == 100.0

    def test_should_calculate_partial_percentages(self):
        """
        percentage should calculate correct values for partial progress.
        """
        assert ProgressModel(current=1, total=4, stage="").percentage == 25.0
        assert ProgressModel(current=3, total=4, stage="").percentage == 75.0

    def test_should_raise_value_error_when_total_is_zero(self):
        """
        ProgressModel should raise ValueError when total is 0.
        """
        with pytest.raises(ValueError, match="total must be greater than 0"):
            ProgressModel(current=0, total=0, stage="")

    def test_should_raise_value_error_when_current_is_negative(self):
        """
        ProgressModel should raise ValueError when current is negative.
        """
        with pytest.raises(ValueError, match="current must be non-negative"):
            ProgressModel(current=-1, total=10, stage="")

    def test_should_cap_percentage_at_hundred_when_current_exceeds_total(self):
        """
        percentage should cap at 100% when current exceeds total.
        """
        progress = ProgressModel(current=15, total=10, stage="")

        assert progress.percentage == 100.0

    def test_should_allow_empty_stage(self):
        """
        ProgressModel should accept empty stage string.
        """
        progress = ProgressModel(current=1, total=10, stage="")

        assert progress.stage == ""

    def test_should_report_completion_status_correctly(self):
        """
        is_complete should return True when current >= total, False otherwise.
        """
        assert ProgressModel(current=10, total=10, stage="").is_complete() is True
        assert ProgressModel(current=5, total=10, stage="").is_complete() is False

    def test_should_calculate_percentage_with_correct_precision(self):
        """
        percentage should calculate with correct floating-point precision.
        """
        progress = ProgressModel(current=1, total=3, stage="")

        assert round(progress.percentage, 2) == 33.33
