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

"""Utilitário para carregar e redimensionar ícones de mundos."""

import logging
from typing import TYPE_CHECKING

import customtkinter as ctk
from PIL import Image

if TYPE_CHECKING:
    from backup_manager_mvp.core.models.world_model import WorldModel

logger = logging.getLogger(__name__)


class WorldIconLoader:
    """Carregador de ícones de mundos Minecraft Bedrock.

    Responsável por:
    - Carregar world_icon.jpeg do sistema de arquivos (800x450, proporção 16:9)
    - Redimensionar para tamanhos padronizados mantendo a proporção
    - Converter para CTkImage para uso no CustomTkinter
    - Cache simples em memória
    """

    # Alturas padrão (largura escala proporcionalmente 16:9)
    ICON_HEIGHT_SMALL = 48  # Lista de mundos → ~85px largura
    ICON_HEIGHT_LARGE = 128  # Detalhes do mundo → ~228px largura

    def __init__(self):
        """Inicializa o carregador com cache vazio."""
        self._cache: dict[str, ctk.CTkImage] = {}

    def load_icon(
        self,
        world: WorldModel,
        height: int = ICON_HEIGHT_SMALL,
    ) -> ctk.CTkImage | None:
        """Carrega e redimensiona a imagem do mundo mantendo proporção 16:9.

        Args:
            world: WorldModel com world_icon_path
            height: Altura desejada em pixels (largura = height * 16/9)

        Returns:
            CTkImage se encontrado e válido, None caso contrário
        """
        if world.world_icon_path is None:
            return None

        cache_key = f"{world.world_icon_path}_{height}"

        # Verificar cache
        if cache_key in self._cache:
            logger.debug(f"Cache hit para imagem: {cache_key}")
            return self._cache[cache_key]

        try:
            if not world.world_icon_path.exists():
                logger.debug(f"Imagem não encontrada: {world.world_icon_path}")
                return None

            # Carregar imagem com Pillow
            pil_image = Image.open(world.world_icon_path)

            # Converter para RGBA se necessário (para transparência)
            if pil_image.mode != "RGBA":
                pil_image = pil_image.convert("RGBA")

            # Calcular largura mantendo proporção 16:9
            target_width = int(height * 16 / 9)

            # Redimensionar mantendo proporção
            pil_image = pil_image.resize((target_width, height), Image.Resampling.LANCZOS)

            # Criar CTkImage (light e dark mode usam a mesma imagem)
            ctk_image = ctk.CTkImage(
                light_image=pil_image,
                dark_image=pil_image,
                size=(pil_image.width, pil_image.height),
            )

            # Armazenar no cache
            self._cache[cache_key] = ctk_image
            logger.debug(
                f"Imagem carregada e cacheada: {cache_key} ({pil_image.width}x{pil_image.height})"
            )

            return ctk_image

        except Exception as e:
            logger.warning(f"Erro ao carregar imagem do mundo {world.folder_name}: {e}")
            return None

    def clear_cache(self) -> None:
        """Limpa o cache de ícones."""
        self._cache.clear()
        logger.debug("Cache de ícones limpo")


# Instância global (singleton pattern simples)
_icon_loader: WorldIconLoader | None = None


def get_icon_loader() -> WorldIconLoader:
    """Retorna instância singleton do WorldIconLoader."""
    global _icon_loader
    if _icon_loader is None:
        _icon_loader = WorldIconLoader()
    return _icon_loader
