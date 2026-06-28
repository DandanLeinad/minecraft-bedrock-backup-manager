# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

from unittest.mock import Mock

from backup_manager_mvp.core.models.progress_model import ProgressModel
from backup_manager_mvp.core.services.progress_service import ProgressService


class TestProgressServiceInitialization:
    """Tests for ProgressService initialization.

    Rules:
    - Can be created with optional on_progress callback
    - Default on_progress is None
    """

    def test_should_store_callback_when_provided(self):
        """
        ProgressService should store the provided on_progress callback.
        """
        callback = Mock()
        service = ProgressService(on_progress=callback)

        assert service.on_progress == callback

    def test_should_have_none_callback_when_not_provided(self):
        """
        ProgressService should have None as on_progress when not provided.
        """
        service = ProgressService()

        assert service.on_progress is None


class TestProgressServiceReporting:
    """Tests for ProgressService report method.

    Rules:
    - Calls callback with ProgressModel when callback is set
    - Does not crash when callback is None
    - Supports multiple sequential calls
    - Passes correct ProgressModel with current, total, stage
    """

    def test_should_call_callback_with_progress_model(self):
        """
        report should call the callback with a ProgressModel containing
        current, total, and stage values.
        """
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=5, total=10, stage="Processing")

        callback.assert_called_once()
        args = callback.call_args[0]
        assert isinstance(args[0], ProgressModel)
        assert args[0].current == 5
        assert args[0].total == 10
        assert args[0].stage == "Processing"

    def test_should_not_crash_when_callback_is_none(self):
        """
        report should not crash when no callback is configured.
        """
        service = ProgressService()

        service.report(current=5, total=10, stage="Processing")

    def test_should_support_multiple_sequential_reports(self):
        """
        report should support being called multiple times sequentially.
        """
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=1, total=10, stage="Stage 1")
        service.report(current=5, total=10, stage="Stage 2")
        service.report(current=10, total=10, stage="Completed")

        assert callback.call_count == 3

    def test_should_pass_correct_stage_for_each_report(self):
        """
        report should pass the correct stage text for each call.
        """
        callback = Mock()
        service = ProgressService(on_progress=callback)

        stages = ["Starting", "Copying", "Finalizing"]
        for i, stage in enumerate(stages, 1):
            service.report(current=i, total=3, stage=stage)

        for i, call in enumerate(callback.call_args_list):
            progress = call[0][0]
            assert progress.stage == stages[i]


class TestProgressServiceReset:
    """Tests for ProgressService reset functionality.

    Rules:
    - Reset preserves the callback
    - Reset allows new progress reporting
    """

    def test_should_preserve_callback_on_reset(self):
        """
        reset should preserve the callback.
        """
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=5, total=10, stage="Processing")
        service.reset()

        assert service.on_progress == callback

    def test_should_allow_new_progress_after_reset(self):
        """
        reset should allow new progress reporting.
        """
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.report(current=5, total=10, stage="Operation 1")
        service.reset()
        service.report(current=3, total=5, stage="Operation 2")

        assert callback.call_count == 2


class TestProgressServiceCallback:
    """Tests for ProgressService callback management.

    Rules:
    - Callback can be changed at runtime
    - Setting callback to None disables reporting
    """

    def test_should_change_callback_at_runtime(self):
        """
        set_callback should change the active callback at runtime.
        """
        callback1 = Mock()
        callback2 = Mock()

        service = ProgressService(on_progress=callback1)
        service.report(current=1, total=10, stage="With callback1")

        service.set_callback(callback2)
        service.report(current=2, total=10, stage="With callback2")

        assert callback1.call_count == 1
        assert callback2.call_count == 1

    def test_should_disable_reporting_when_callback_set_to_none(self):
        """
        set_callback(None) should disable progress reporting.
        """
        callback = Mock()
        service = ProgressService(on_progress=callback)

        service.set_callback(None)
        service.report(current=1, total=10, stage="Test")

        callback.assert_not_called()
