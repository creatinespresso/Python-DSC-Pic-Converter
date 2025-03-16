# gui/tooltip_editor.py

import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt

class TooltipEditorDialog(QDialog):
    """
    Einfaches Dialogfenster, um 'tooltips.md' zu laden, zu bearbeiten und 
    wieder zu speichern. Die Syntax: 
        #PARAM_QUALITY
        Hier die Beschreibung ...
        #PARAM_SOMETHING
        Hier der nächste Tooltip ...
    """
    def __init__(self, tooltip_file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tooltips bearbeiten")

        self.tooltip_file_path = tooltip_file_path

        layout = QVBoxLayout(self)

        self.label_info = QLabel("Bearbeite hier den Inhalt von tooltips.md:")
        layout.addWidget(self.label_info)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # Button-Leiste
        button_layout = QHBoxLayout()
        self.btn_load = QPushButton("Laden")
        self.btn_load.clicked.connect(self.load_tooltips)
        button_layout.addWidget(self.btn_load)

        self.btn_save = QPushButton("Speichern")
        self.btn_save.clicked.connect(self.save_tooltips)
        button_layout.addWidget(self.btn_save)

        self.btn_load_other_file = QPushButton("Andere Datei...")
        self.btn_load_other_file.clicked.connect(self.load_other_file)
        button_layout.addWidget(self.btn_load_other_file)

        layout.addLayout(button_layout)

        self.resize(600, 400)
        self.load_tooltips()  # Beim Öffnen direkt laden

    def load_tooltips(self):
        """
        Lädt den Inhalt der tooltips.md (sofern vorhanden) in das Textfeld.
        """
        if os.path.isfile(self.tooltip_file_path):
            try:
                with open(self.tooltip_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_edit.setPlainText(content)
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Konnte Datei nicht lesen:\n{e}")
        else:
            self.text_edit.setPlainText("# Noch keine Tooltips hinterlegt.\n")

    def save_tooltips(self):
        """
        Speichert den Inhalt aus dem Textfeld in die tooltips.md.
        """
        content = self.text_edit.toPlainText()
        try:
            with open(self.tooltip_file_path, "w", encoding="utf-8") as f:
                f.write(content)
            QMessageBox.information(self, "Gespeichert", "Tooltips erfolgreich gespeichert.")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Konnte Datei nicht speichern:\n{e}")

    def load_other_file(self):
        """
        Ermöglicht das Laden einer anderen Markdown-Datei (z.B. alternative Tooltips).
        """
        new_path, _ = QFileDialog.getOpenFileName(self, "Tooltips-Datei auswählen", "", "Markdown-Datei (*.md)")
        if new_path:
            self.tooltip_file_path = new_path
            self.load_tooltips()
