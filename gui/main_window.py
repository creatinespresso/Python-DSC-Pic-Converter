# -*- coding: utf-8 -*-
# gui/main_window.py

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, 
    QFileDialog, QHBoxLayout, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt

from modules import get_format_class
from gui.param_form import ParamForm
from gui.tooltip_editor import TooltipEditorDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DSC-Pic-Converter")
        self.resize(900, 600)

        # Attribute zum Merken der Pfade und des ausgewählten Formats
        self.input_path = None
        self.output_path = None

        # Haupt-Widget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # =========== QUELLE / ZIEL-AUSWAHL ===========
        # Horizontal: Button "Quelle wählen" und Anzeige
        source_layout = QHBoxLayout()
        self.btn_select_source = QPushButton("Quelle wählen")
        self.btn_select_source.clicked.connect(self.select_source)
        source_layout.addWidget(self.btn_select_source)

        self.label_source_path = QLabel("Keine Datei gewählt.")
        source_layout.addWidget(self.label_source_path, 1)  # Dehnt sich

        main_layout.addLayout(source_layout)

        # Horizontal: Button "Ziel wählen" und Anzeige
        target_layout = QHBoxLayout()
        self.btn_select_target = QPushButton("Ziel wählen")
        self.btn_select_target.clicked.connect(self.select_target)
        target_layout.addWidget(self.btn_select_target)

        self.label_target_path = QLabel("Keine Zieldatei gewählt.")
        target_layout.addWidget(self.label_target_path, 1)

        main_layout.addLayout(target_layout)

        # =========== FORMAT-AUSWAHL + PARAMETERFORM ===========
        # Horizontal: ComboBox für Format und daneben ParamForm
        format_layout = QHBoxLayout()

        # ComboBox: Mögliche Formate (per get_format_class abfragbar)
        # Wir wissen dank modules/__init__.py, welche Formate "jpg", "png", "ico", "svg" registriert sind
        self.combo_format = QComboBox()
        # Man könnte Format-Liste hart eintragen oder per modules.registered_formats.keys()
        from modules import registered_formats  # Sofern wir es direkt nutzen wollen
        available = sorted(list(registered_formats.keys()))
        self.combo_format.addItems(available)
        self.combo_format.currentTextChanged.connect(self.on_format_changed)

        format_layout.addWidget(self.combo_format, 0)

        # ParamForm (zunächst leer, füllen wir in on_format_changed)
        self.param_form = ParamForm(params={})
        format_layout.addWidget(self.param_form, 1)

        main_layout.addLayout(format_layout)

        # =========== BUTTONS (Konvertierung, Tooltip-Editor) ===========
        button_layout = QHBoxLayout()

        # Button: Tooltip-Editor
        self.btn_tooltip_editor = QPushButton("Tooltip-Editor")
        self.btn_tooltip_editor.clicked.connect(self.open_tooltip_editor)
        button_layout.addWidget(self.btn_tooltip_editor)

        # Button: Konvertierung starten
        self.btn_convert = QPushButton("Konvertierung starten")
        self.btn_convert.clicked.connect(self.start_conversion)
        button_layout.addWidget(self.btn_convert)

        main_layout.addLayout(button_layout)

        # Beim Start gleich das erste Format in der ComboBox laden
        self.on_format_changed(self.combo_format.currentText())

    def select_source(self):
        """Öffnet einen Dateidialog zum Auswählen einer Bilddatei."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Bilddatei auswählen", 
            "", 
            "Bilddateien (*.png *.jpg *.ico *.bmp *.jpeg *.gif)"
        )
        if file_path:
            self.input_path = file_path
            self.label_source_path.setText(f"Quelle: {file_path}")

            # Falls noch kein Ziel gesetzt ist, schlagen wir automatisch einen vor
            if not self.output_path:
                base, ext = os.path.splitext(file_path)
                selected_format = self.combo_format.currentText()
                # z.B. an Dateinamen anhängen:  base + "_converted." + selected_format
                # Aber "svg" ist kein Bild-Container => wir verwenden denselben Dateinamen, nur mit passender Endung
                new_target = f"{base}_converted.{selected_format}"
                self.output_path = new_target
                self.label_target_path.setText(f"Zieldatei: {new_target}")

    def select_target(self):
        """Dateidialog zum Auswählen/Angeben einer Zieldatei."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Zieldatei wählen",
            "",
            "Alle Dateien (*.*)"
        )
        if file_path:
            self.output_path = file_path
            self.label_target_path.setText(f"Zieldatei: {file_path}")

    def on_format_changed(self, new_format):
        """Wird aufgerufen, wenn der Nutzer ein neues Zielformat im ComboBox auswählt."""
        FormatClass = get_format_class(new_format)
        if not FormatClass:
            return  # Unbekannt, sollte nicht vorkommen

        # Neue Instanz holen
        format_instance = FormatClass()
        param_def = format_instance.get_params()  # Dictionary
        # Neue ParamForm anlegen (oder updaten)
        # Hier machen wir es einfach: Erzeugen ein neues Widget und ersetzen
        new_form = ParamForm(param_def)

        # Altes Widget entfernen, das neue einsetzen
        parent_layout = self.param_form.parentWidget().layout()
        parent_layout.removeWidget(self.param_form)
        self.param_form.deleteLater()

        self.param_form = new_form
        parent_layout.addWidget(self.param_form)

        # Falls wir schon eine Quelldatei haben, passen wir den Dateinamen an
        if self.input_path and self.output_path:
            base, _ = os.path.splitext(self.output_path)
            updated_target = f"{base}.{new_format}"
            self.output_path = updated_target
            self.label_target_path.setText(f"Zieldatei: {updated_target}")

    def open_tooltip_editor(self):
        """Öffnet den Dialog zum Bearbeiten der tooltips.md."""
        tooltip_file_path = os.path.join(os.path.dirname(__file__), "..", "resources", "tooltips.md")
        dialog = TooltipEditorDialog(os.path.normpath(tooltip_file_path), parent=self)
        dialog.exec()

    def start_conversion(self):
        """Führt die eigentliche Konvertierung durch, basierend auf den gewählten Parametern."""
        if not self.input_path or not os.path.isfile(self.input_path):
            QMessageBox.warning(self, "Fehler", "Bitte zuerst eine gültige Quelldatei auswählen!")
            return

        if not self.output_path:
            QMessageBox.warning(self, "Fehler", "Bitte eine Zieldatei festlegen!")
            return

        # Format ermitteln und passende Klasse laden
        chosen_format = self.combo_format.currentText()
        FormatClass = get_format_class(chosen_format)
        if not FormatClass:
            QMessageBox.critical(self, "Fehler", f"Unbekanntes Zielformat: {chosen_format}")
            return

        # ParamForm-Werte abholen
        options = self.param_form.get_values()

        try:
            instance = FormatClass()
            instance.convert(self.input_path, self.output_path, options)
            QMessageBox.information(self, "Erfolg", f"Datei erfolgreich konvertiert:\n{self.output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Fehler bei Konvertierung", str(e))
