# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Handlers para navegação entre telas."""

import logging

logger = logging.getLogger(__name__)


def on_back(callback) -> None:
    """Handler para voltar à tela anterior.

    Args:
        callback: Callback para executar navegação
    """
    logger.debug("Voltando à lista de mundos")
    if callback:
        callback()
