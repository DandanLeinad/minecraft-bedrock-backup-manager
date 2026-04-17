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

"""Ponto de entrada da aplicação Minecraft Bedrock Backup Manager.

Este módulo apenas:
1. Configura logging
2. Inicializa o ApplicationController
3. Inicia a aplicação

A orquestração de serviços e UI está em application.py (BackupManagerApp).
"""

import logging
import os
import sys

from backup_manager_mvp.application import BackupManagerApp
from backup_manager_mvp.utils.paths import LOG_FILE, ensure_directories

# Fix para PyInstaller --nowindow: sys.stdout/stderr podem ser None
# Isso evita AttributeError de bibliotecas que tentam acessar essas streams
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")  # noqa: SIM115
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")  # noqa: SIM115


def _configure_logging() -> None:
    """Configura logging para arquivo e console."""
    ensure_directories()

    # Detectar se está em modo desenvolvimento (para logging DEBUG)
    is_debug_mode = "-v" in sys.argv or "--debug" in sys.argv or "flet" in sys.argv[0]

    log_level = logging.DEBUG if is_debug_mode else logging.INFO
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        if is_debug_mode
        else "%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout),  # Também mostrar no console
        ],
    )


def main():
    """Função principal - ponto de entrada da aplicação."""
    try:
        _configure_logging()
        logger = logging.getLogger(__name__)

        logger.info("=== Backup Manager Iniciando ===")
        logger.info(f"Log registrado em: {LOG_FILE}")

        app = BackupManagerApp()
        app.run()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.critical(f"Erro crítico ao iniciar: {e}", exc_info=True)


if __name__ == "__main__":
    main()
