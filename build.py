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

"""Build script for Minecraft Bedrock Backup Manager using PyInstaller.

Segue recomendações do CustomTkinter: usa --onedir ao invés de --onefile
porque CustomTkinter inclui arquivos de dados que não podem ser empacotados
em um único arquivo.

Uso:
    python build.py              # Build padrão (onedir, sem console)
    python build.py --debug      # Build com console para debug
    python build.py --clean      # Limpar artifacts de build anterior
    python build.py --help       # Mostrar ajuda

Resultado:
    dist/minecraft-bedrock-backup-manager/  (diretório com executável + deps)
"""

import argparse
import logging
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# === CONFIGURAÇÕES ===
PROJECT_ROOT = Path(__file__).parent
BUILD_DIR = PROJECT_ROOT / "build" / "pyinstaller"
DIST_DIR = PROJECT_ROOT / "dist"
APP_NAME = "minecraft-bedrock-backup-manager"
SRC_DIR = PROJECT_ROOT / "src" / "backup_manager_mvp"
MAIN_SCRIPT = PROJECT_ROOT / "src" / "backup_manager_mvp" / "main.py"
VERSION_JSON = SRC_DIR / "version.json"
ICON_FILE = SRC_DIR / "ui" / "customtkinter" / "assets" / "icon.ico"

# === LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def clean_build_artifacts() -> None:
    """Remove build artifacts de execuções anteriores."""
    logger.info("Limpando artifacts de build anterior...")

    for path in [BUILD_DIR, DIST_DIR]:
        if path.exists():
            logger.info(f"  Removendo {path}")
            shutil.rmtree(path)

    logger.info("✓ Limpeza concluída")


def get_version() -> str:
    """Lê a versão do version.json.

    Returns:
        Versão do aplicativo
    """
    import json

    try:
        with open(VERSION_JSON, encoding="utf-8") as f:
            data = json.load(f)
            return data.get("current", "unknown")
    except Exception as e:
        logger.warning(f"Não foi possível ler versão: {e}")
        return "unknown"


def copy_runtime_files() -> None:
    """Copia arquivos necessários em runtime para o diretório de build."""
    logger.info("Copiando arquivos de runtime...")

    # Criar diretório de distribuição se não existir
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    # Copiar version.json
    if VERSION_JSON.exists():
        version_dest = DIST_DIR / "version.json"
        shutil.copy2(VERSION_JSON, version_dest)
        logger.info(f"  ✓ Copiado version.json para {version_dest}")
    else:
        logger.warning(f"  ⚠ version.json não encontrado em {VERSION_JSON}")


def build_executable(debug: bool = False) -> bool:
    """Executa PyInstaller para gerar o executável.

    Segue recomendações do CustomTkinter: usar --onedir ao invés de --onefile
    porque CustomTkinter inclui arquivos de dados (.json, .otf) que não podem
    ser empacotados em um único arquivo.

    Args:
        debug: Se True, inclui console para debug

    Returns:
        True se build foi bem-sucedido
    """
    version = get_version()
    logger.info(f"Construindo {APP_NAME} v{version}...")

    # === ENCONTRAR CUSTOMTKINTER PATH ===
    import customtkinter

    customtkinter_path = str(Path(customtkinter.__file__).parent)
    logger.info(f"CustomTkinter path: {customtkinter_path}")

    # === PARÂMETROS BASE ===
    pyinstaller_args = [
        str(MAIN_SCRIPT),
        "--name",
        APP_NAME,
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR / "work"),
        "--specpath",
        str(BUILD_DIR / "spec"),
        # ✅ USAR --onedir (NÃO --onefile)
        # CustomTkinter recomenda --onedir porque inclui arquivos de dados
        "--onedir",
    ]

    if debug:
        logger.info("  Modo DEBUG: console visível")
        pyinstaller_args.append("--console")
    else:
        logger.info("  Modo RELEASE: sem console")
        pyinstaller_args.append("--windowed")

    # === ADICIONAR CUSTOMTKINTER MANUALMENTE ===
    # CustomTkinter recomenda adicionar o diretório manualmente com --add-data
    add_data_customtkinter = f"{customtkinter_path};customtkinter"
    pyinstaller_args.extend(["--add-data", add_data_customtkinter])
    logger.info("  CustomTkinter incluído")

    # Ícone (se existir)
    if ICON_FILE.exists():
        pyinstaller_args.extend(["--icon", str(ICON_FILE)])
        logger.info(f"  Ícone: {ICON_FILE}")
    else:
        logger.warning(f"  ⚠ Ícone não encontrado: {ICON_FILE}")

    # === HIDDEN IMPORTS (pacotes que PyInstaller não detecta automaticamente) ===
    hidden_imports = [
        "customtkinter",
        "backup_manager_mvp",
        "backup_manager_mvp.models",
        "backup_manager_mvp.services",
        "backup_manager_mvp.ui",
        "backup_manager_mvp.ui.customtkinter",
        "backup_manager_mvp.utils",
        "pydantic",
    ]

    for imp in hidden_imports:
        pyinstaller_args.extend(["--hidden-import", imp])

    # === ADICIONAR DADOS (version.json) ===
    # Formato: --add-data "source;dest" (Windows usa ;)
    add_data = f"{VERSION_JSON};backup_manager_mvp"
    pyinstaller_args.extend(["--add-data", add_data])
    logger.info("  Dados incluidos: version.json")

    # === EXECUTAR PYINSTALLER ===
    logger.info("\nExecutando PyInstaller...")
    try:
        subprocess.run(
            ["pyinstaller", *pyinstaller_args],
            check=True,
            capture_output=False,
        )
        logger.info("✓ Build bem-sucedido!")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"✗ Build falhou com erro: {e}")
        return False
    except FileNotFoundError:
        logger.error("✗ PyInstaller não encontrado. Instale com: pip install pyinstaller")
        return False


def create_build_info() -> None:
    """Cria arquivo de informação de build."""
    version = get_version()
    now = datetime.now().isoformat()

    build_info = f"""# Build Information

**Versão**: {version}
**Data de Build**: {now}
**Plataforma**: Windows (PyInstaller)
**Modo**: {"Debug" if False else "Release"}

## Arquivos Inclusos

- minecraft-bedrock-backup-manager.exe (executável principal)
- version.json (metadados de versão)

## Instruções

1. Execute o arquivo .exe
2. Aceite o disclaimer
3. Selecione seus mundos Minecraft Bedrock
4. Crie e restaure backups conforme necessário

## Requisitos

- Windows 7 ou superior
- Minecraft Bedrock Edition instalado

## Suporte

Para problemas, consulte:
- README.md
- CHANGELOG.md
- Logs em: %APPDATA%/minecraft-bedrock-backup-manager/

---
**Generated by build.py**
"""

    build_info_path = DIST_DIR / "BUILD_INFO.md"
    with open(build_info_path, "w", encoding="utf-8") as f:
        f.write(build_info)

    logger.info(f"✓ Build info criado: {build_info_path}")


def main() -> int:
    """Função principal de build."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Build com console para debug",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Limpar artifacts de build anterior",
    )

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info(f"Build Script - {APP_NAME}")
    logger.info("=" * 60)

    # === LIMPEZA (OPCIONAL) ===
    if args.clean:
        clean_build_artifacts()

    # === COPIAR ARQUIVOS DE RUNTIME ===
    copy_runtime_files()

    # === BUILD ===
    if not build_executable(debug=args.debug):
        return 1

    # === CRIAR BUILD INFO ===
    create_build_info()

    # === RESUMO FINAL ===
    logger.info("\n" + "=" * 60)
    logger.info("✓ BUILD CONCLUÍDO COM SUCESSO!")
    logger.info("=" * 60)
    logger.info(f"Executável: {DIST_DIR / f'{APP_NAME}.exe'}")
    logger.info(f"Diretório: {DIST_DIR}")
    logger.info("\nPróximos passos:")
    logger.info("  1. Teste o executável localmente")
    logger.info("  2. Crie um ZIP para distribuição")
    logger.info("  3. Faça upload para GitHub Releases")
    logger.info("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
