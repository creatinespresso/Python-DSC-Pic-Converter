# modules/base_module.py

from abc import ABC, abstractmethod

class ImageFormatBase(ABC):
    """
    Abstrakte Basisklasse für Bildformate.
    Jeder Unterklasse sollte Methoden zur Verfügung stellen, 
    um Parameter einzulesen und das Konvertieren durchzuführen.
    """

    @abstractmethod
    def get_params(self):
        """
        Liefert ein Dictionary mit den möglichen Parametern 
        (z.B. Qualität, Farbtiefe etc.).
        Beispiel-Rückgabeformat:
        {
            "PARAM_QUALITY": {
                "type": "int",
                "default": 80,
                "min": 0,
                "max": 100
            },
            ...
        }
        """
        pass

    @abstractmethod
    def convert(self, input_path, output_path, options):
        """
        Führt die eigentliche Konvertierung durch, 
        basierend auf den übergebenen Optionen (Dictionary).
        """
        pass
