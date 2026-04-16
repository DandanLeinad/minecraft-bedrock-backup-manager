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
