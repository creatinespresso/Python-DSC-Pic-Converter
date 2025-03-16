# -*- coding: utf-8 -*-
# modules/__init__.py

import pkgutil
import importlib
import os

# Dictionary, in dem wir Format-Namen (z.B. 'jpg', 'png') auf Klassen mappen
registered_formats = {}

def load_format_modules():
    """
    Lädt alle Python-Module in diesem Ordner (die mit 'format_' beginnen)
    und registriert deren Klassen, die auf 'ImageFormatBase' basieren.
    """
    package_dir = os.path.dirname(__file__)  # Verzeichnis dieses Pakets
    package_name = __name__  # "modules"

    for module_info in pkgutil.iter_modules([package_dir]):
        if module_info.name.startswith("format_"):
            # modul importieren
            full_module_name = f"{package_name}.{module_info.name}"
            module = importlib.import_module(full_module_name)

            # Durchsuche die Attribute nach Klassen, die ImageFormatBase erben
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, "__bases__"):
                    bases = attr.__bases__
                    if any("ImageFormatBase" == base.__name__ for base in bases):
                        # z.B. 'format_jpg' -> 'jpg'
                        format_name = module_info.name.replace("format_", "")
                        registered_formats[format_name] = attr

# Beim Import automatisch laden
load_format_modules()

def get_format_class(format_name):
    """
    Gibt die entsprechende Klasse zurück, z.B. 'FormatJPG' 
    für 'jpg', oder None, wenn unbekannt.
    """
    return registered_formats.get(format_name.lower())
