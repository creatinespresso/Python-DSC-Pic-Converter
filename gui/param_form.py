# gui/param_form.py

from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QCheckBox, QSpinBox, QLabel
)
from PySide6.QtCore import Qt

class ParamForm(QWidget):
    """
    Dynamisch erzeugte Eingabefelder für die Format-Parameter.

    Aufrufbeispiel:
        param_def = {
            "PARAM_QUALITY": {"type": "int", "default": 80, "min": 0, "max": 100},
            "PARAM_OPTIMIZE": {"type": "bool", "default": True}
        }
        form = ParamForm(param_def)
    """

    def __init__(self, params: dict, parent=None):
        super().__init__(parent)
        self.params = params  # Dictionary der Parameter-Definitionen
        self.form_layout = QFormLayout(self)
        self.form_layout.setLabelAlignment(Qt.AlignRight)

        # Hier speichern wir die Widgets und ihre Keys, 
        # um später die Werte auszulesen:
        self.widgets_by_key = {}

        self.build_form()

    def build_form(self):
        """Erzeugt pro Parameter ein passendes Widget."""
        for key, definition in self.params.items():
            param_type = definition.get("type")
            default_val = definition.get("default")

            if param_type == "int":
                widget = QSpinBox()
                widget.setRange(definition.get("min", 0), definition.get("max", 100))
                widget.setValue(default_val)
                self.form_layout.addRow(key, widget)
                self.widgets_by_key[key] = widget

            elif param_type == "bool":
                widget = QCheckBox()
                widget.setChecked(bool(default_val))
                self.form_layout.addRow(key, widget)
                self.widgets_by_key[key] = widget

            elif param_type == "list_of_int_tuples":
                # Nur ein Label als Platzhalter – 
                # in Wirklichkeit bräuchte man evtl. 
                # eine komplexere UI (Tabelle/Mehrfach-Eingabefelder).
                label = QLabel(f"{default_val}")
                self.form_layout.addRow(key, label)
                self.widgets_by_key[key] = label

            else:
                # Standard-Case: String
                line = QLineEdit(str(default_val))
                self.form_layout.addRow(key, line)
                self.widgets_by_key[key] = line

    def get_values(self):
        """
        Liest die Nutzer-Eingaben aus und 
        liefert ein Dict: {param_key: user_value}
        """
        result = {}
        for key, widget in self.widgets_by_key.items():
            if isinstance(widget, QSpinBox):
                result[key] = widget.value()
            elif isinstance(widget, QCheckBox):
                result[key] = widget.isChecked()
            elif isinstance(widget, QLabel):
                # Hier ggf. Parsen, falls wir was Editierbares bräuchten
                result[key] = widget.text()  
                # oder man implementiert separate Edit-Fenster
            elif isinstance(widget, QLineEdit):
                result[key] = widget.text()
            else:
                # Fallback
                result[key] = None
        return result
