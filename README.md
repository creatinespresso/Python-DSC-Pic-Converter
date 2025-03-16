## 1. Geplante Bibliotheken und externe Module

1. **Pillow**  
   - Grundlegende Bildverarbeitung (Öffnen, Konvertieren, Resizing, Kompression etc.).  
   - Alternative: *Wand (ImageMagick-Python-Wrapper)*, aber Pillow ist sehr verbreitet und leichter in eine portable Umgebung einzubinden.

2. **PySide6** oder **PyQt5/PyQt6**  
   - Für eine moderne GUI (im Vergleich zu Tkinter).
   - Bietet auch Widgets für ToolTips und komplexere Oberflächen.

3. **Optional: Tool zur Raster-/Vektorkonvertierung**  
   - Evtl. **potrace** oder ähnliche Tools, die man ggf. per Subprozess ansteuern kann, um Rastergrafiken in einfache Vektorpfade (SVG, PDF, EPS etc.) zu wandeln.  
   - Da Raster-zu-Vektor meist nicht „perfekt“ ist (Stichwort Tracing), muss man überlegen, ob man hier nur einen Shell-Aufruf von potrace oder einem anderen Programm einbaut.

4. **(Optional) Markdown-Parser**  
   - Falls man die Tooltip-Texte und die Beschreibungen in Markdown-Format flexibel verarbeiten möchte, könnte man z.B. `markdown`-Package oder ähnliches verwenden.  
   - Ansonsten kann man die `.md`-Dateien direkt als reinen Text einlesen und nur minimal auswerten – je nach gewünschtem Funktionsumfang.

5. **(Optional) PyInstaller oder ähnliches**  
   - Zum Erstellen eines „Container“-Pakets, das möglichst portabel (als EXE auf Windows oder plattformübergreifend) ausgeliefert werden kann und alle Libraries in sich trägt.

---

## 2. Ordnerstruktur (Vorschlag)

    DSC-Pic-Converter/
    ├─ main.py                      # Startpunkt/Steuerungsprogramm
    ├─ requirements.txt            # Liste mit genutzten Bibliotheken (nur zur Doku)
    ├─ modules/
    │   ├─ __init__.py
    │   ├─ base_module.py          # Gemeinsame Funktionalität + Klassen
    │   ├─ format_jpg.py           # Logik für JPG: mögliche Parameter etc.
    │   ├─ format_png.py           # Logik für PNG: mögliche Parameter etc.
    │   ├─ format_ico.py           # Logik für ICO: mögliche Parameter etc.
    │   ├─ format_svg.py           # Logik für SVG (Vektor) - hier optional
    │   └─ ... weitere Formate ...
    ├─ resources/
    │   ├─ tooltips.md             # Enthält Mappings: #Parameter -> Beschreibung
    │   ├─ icon.png                # Symbole für GUI, falls nötig
    │   └─ ... evtl. weitere ...
    ├─ gui/
    │   ├─ __init__.py
    │   ├─ main_window.py          # Hauptfenster GUI
    │   ├─ tooltip_editor.py       # Sub-Fenster/Modul für Tooltip-Editor
    │   └─ ...
    ├─ README.md
    └─ (evtl. weitere Dateien)

Erläuterungen:

- **`main.py`**  
  - Hier startet das Programm, lädt alle notwendigen Module, initialisiert die GUI und integriert z.B. eine Logik zur Laufzeit-Erweiterung (Plug-in/Module).
- **`modules/`**  
  - Für jedes unterstützte Bildformat ein separates Modul, in dem
    - Konvertierungsfunktionen
    - Parameterdefinitionen (z.B. `PARAMS = {...}`)
    - ggf. Validierung oder spezielle Konvertierung
  - *`base_module.py`* könnte z.B. eine Basisklasse `ImageFormat` definieren mit Methoden wie `convert(input_path, output_path, options)`.
- **`resources/`**  
  - Enthält Mediendateien, z.B. Icons für die GUI und die **Markdown-Datei** (`tooltips.md`) für die Erklärungen.
- **`gui/`**  
  - PySide/PyQt-basierte Module, um das Hauptfenster und zusätzliche Dialoge (z.B. den Tooltip-Editor) zu trennen.
  - **`tooltip_editor.py`** verwaltet das Auslesen/Schreiben der `tooltips.md`, das Bearbeiten und Abspeichern.

---

## 3. Wie greifen die Teile ineinander?

1. **Start in `main.py`**  
   - Liest vorhandene Module in `modules/` ein (z.B. mittels `importlib` oder einem dynamischen Import).  
   - Baut daraus eine Liste an verfügbaren Formaten (z.B. `['jpg', 'png', 'ico']`).  
   - Initialisiert die GUI (z.B. `MainWindow` aus `gui/main_window.py`), übergibt die Liste der Formate.

2. **GUI-Aufbau (simplifiziert)**  
   - **Auswahl Eingabeformat** und **Auswahl Ausgabeformat** (Dropdown oder Buttons).  
   - **Parameterfelder**: Dynamisch generiert in Abhängigkeit vom gewählten Modul (d.h. wenn der Nutzer „JPG“ wählt, liest das Programm aus `format_jpg.py` die Parameter-Liste aus).  
   - **Tooltip-Integration**:  
     - Beim Hovern über ein Parameterfeld liest das Programm den entsprechenden Eintrag aus der `tooltips.md` (wenn vorhanden).  
     - Falls kein Eintrag für das Hashtag existiert, zeigt die GUI „Noch kein Tooltip vorhanden“.
   - **Tooltip-Editor** (ein weiterer Dialog) erlaubt es, neue Tooltips hinzuzufügen oder vorhandene zu ändern und speichert sie wieder ab.

3. **Tooltips-Konzept** (mit `tooltips.md`)  
   - Struktur könnte so aussehen:
     ```
     #PARAM_QUALITY
     Dieses Parameter steuert den Qualitätsfaktor für die JPEG-Kompression.
     Wertebereich: 0 - 100 (wobei 100 nahe an keine Kompression ist).
     
     #PARAM_RESOLUTION
     Legt die Auflösung in DPI fest. Höher = mehr Pixel pro Inch etc.
     
     ...
     ```
   - Das Programm durchforstet nach Zeilenbeginn mit `#PARAM_NAME` und nimmt danach den zugehörigen Fließtext bis zum nächsten `#...` oder Datei-Ende als Tooltip.  
   - Falls man’s komplexer braucht, könnte man noch Markdown-Syntax anreichern (Titel, fett, kursiv etc.).

4. **Dynamisches Laden der Parameter**  
   - Jedes Format-Modul (z.B. `format_jpg.py`) könnte ein Dictionary bereitstellen (z.B. `PARAMS = { "PARAM_QUALITY": {"type": "int", "default": 80, ...}, ...}`), das Auskunft über mögliche Parameter liefert.  
   - Die GUI liest dieses Dictionary beim Umschalten auf das Format und erzeugt entsprechend Eingabefelder.  
   - Über die Keys (z.B. `"PARAM_QUALITY"`) kann das Programm die entsprechenden Tooltips aus `tooltips.md` ziehen.

5. **Konvertierung**  
   - Nach Auswahl der Parameter durch den Nutzer ruft die GUI `convert(input_path, output_path, options)` auf dem entsprechenden Formatmodul auf.  
   - Das jeweilige Modul nutzt z.B. `Pillow` zum Lesen, Konvertieren und Speichern.  
   - Ggf. Vektor-zu-Raster oder Raster-zu-Vektor via externem Tool / Library.  

---

## 4. Container-/Portable-Lösung

1. **Portabler Ordner**  
   - Alles liegt in `DSC-Pic-Converter`.  
   - Theoretisch kann man darin einen `venv/`-Ordner anlegen, in dem alle benötigten Python-Pakete installiert sind.
   - Nutzer bräuchte nur eine kompatible Python-Installation. Das `main.py` nutzt dann das lokale `venv` (wenn vorhanden) oder versucht, auf das System-Python zuzugreifen.

2. **PyInstaller/PyOxidizer**  
   - Damit könnte man eine einzige `.exe` (Windows) oder plattformabhängige Binärdatei erstellen, in der Python und die ganzen Module enthalten sind.  
   - Auf Linux/macOS kann man ähnlich verfahren – dort sind die Portable-Builds teilweise aufwändiger, aber auch machbar.

3. **Selbstentpackendes Zip**  
   - Für rein plattformunabhängig: ein „Script-Container“, der beim Ausführen sich selbst entpackt und `main.py` ausführt.  
   - Vor allem bei größeren Daten (lib-Ordner) kann das etwas sperrig werden. PyInstaller ist i.d.R. komfortabler.

---

## 5. Wichtige Parameter bei Bild-Konvertierung (Auszug)

- **Kompressionsgrad** (z.B. JPEG-Qualität, PNG-Kompressionsstufe).
- **Zielgröße** in Pixel (Breite x Höhe) oder als Prozentangabe.  
- **DPI/Resolution** (beeinflusst v.a. Druckausgabe).  
- **Farbtiefe** (8-Bit, 24-Bit, 32-Bit mit Alpha etc.).  
- **Transparenz** (Alpha-Kanal beibehalten?).  
- **Vektor-Konvertierung** (gerade bei SVG -> PNG oder Raster -> Vektor, z.B. via potrace).  
- **Seitenverhältnis beibehalten oder nicht**.  
- **Mehrseitige Formate** (TIFF-PDF-Konvertierungen oder animierte GIFs, wenn relevant).  

---

## 6. Zusammenfassung: Ablauf

1. **Start**  
   - Benutzer klickt `DSC-Pic-Converter/main.py` (oder eine erstellte `.exe`).  
2. **GUI erscheint**  
   - Nutzer wählt Eingabedatei(en).  
   - Nutzer legt Ausgabeformat (z.B. PNG, JPG, ICO) fest.  
   - GUI zeigt Parameterfelder (basierend auf Format-Modul).  
   - GUI zeigt Tooltips beim Hovern über Parameter (Markdown aus `tooltips.md`).  
3. **Konvertierung**  
   - Nutzer klickt „Konvertieren“.  
   - Programm ruft die entsprechende Funktion in `modules/format_*.py` auf.  
   - Bester/Allgemeiner Weg: Standardfunktionen von Pillow, optional Sonderfälle.  
4. **Ergebnis**  
   - Konvertierte Dateien liegen im Zielordner.  
   - Log/Status in der GUI, ggf. Fehlermeldungen.  

---

### Nächste Schritte


- **Klären**, ob man den Weg über PyInstaller gehen will (empfohlen für Windows-User).  
