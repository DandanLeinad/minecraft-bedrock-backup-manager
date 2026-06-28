# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Configuração centralizada de paths da aplicação."""

from pathlib import Path

# Diretório raiz para backups e logs
BACKUPS_ROOT = Path.home() / "Documents" / "MinecraftBackups"

# Arquivo de log
LOG_FILE = BACKUPS_ROOT / "app.log"

# Diretório de backups
BACKUPS_DIR = BACKUPS_ROOT / "backups"


def ensure_directories():
    """Garante que todos os diretórios necessários existem."""
    BACKUPS_ROOT.mkdir(parents=True, exist_ok=True)
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
