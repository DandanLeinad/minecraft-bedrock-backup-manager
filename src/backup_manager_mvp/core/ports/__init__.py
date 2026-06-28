# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 DandanLeinad.

"""Portas do dominio (contratos para infraestrutura)."""

from .backup_repository import BackupRepositoryPort
from .world_repository import WorldRepositoryPort

__all__ = ["BackupRepositoryPort", "WorldRepositoryPort"]
