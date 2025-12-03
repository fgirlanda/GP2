import sys
from pathlib import Path


def get_base_path() -> Path:
    """
    Restituisce il path base dell'applicazione.
    Funziona sia in sviluppo che come .exe
    """
    if getattr(sys, 'frozen', False):
        # Eseguibile PyInstaller - le risorse sono in _MEIPASS
        return Path(getattr(sys, '_MEIPASS', '.'))
    else:
        # Sviluppo normale - risali dalla cartella utils/
        return Path(__file__).parent.parent.parent


def get_resource_path(filename: str) -> str:
    """
    Restituisce il path assoluto di una risorsa.

    Args:
        filename: Nome del file (es. "cerca.png")

    Returns:
        Path assoluto come stringa
    """
    return str(get_base_path() / "resources" / filename)
