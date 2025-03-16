# modules/format_svg.py

import os
from subprocess import run
from PIL import Image
from .base_module import ImageFormatBase

class FormatSVG(ImageFormatBase):
    def get_params(self):
        return {
            "PARAM_THRESHOLD": {
                "type": "int",
                "default": 128,
                "min": 0,
                "max": 255
            },
            # Weitere Parameter für Potrace usw.
        }

    def convert(self, input_path, output_path, options):
        """
        Ein möglicher Ansatz: 
        1) Bild als BMP speichern,
        2) Potrace aufrufen, um BMP nach SVG zu vektorisieren,
        3) SVG abspeichern.

        options: {"PARAM_THRESHOLD": 128, ...}
        """
        # Temporäre BMP-Datei
        temp_bmp = os.path.splitext(output_path)[0] + ".bmp"
        with Image.open(input_path) as img:
            # in 1-Bit (bitmap) konvertieren -> threshold
            threshold = options.get("PARAM_THRESHOLD", 128)
            # 'L' = 8-bit grayscale, dann binär konvertieren
            gray_img = img.convert("L")
            bw = gray_img.point(lambda x: 255 if x > threshold else 0, '1')
            bw.save(temp_bmp)

        # potrace-Aufruf -> 'potrace -s <datei>'
        # run kann je nach OS potenziell anders sein
        command = ["potrace", "-s", temp_bmp, "-o", output_path]
        run(command, check=True)

        # Temporäre BMP ggf. löschen
        if os.path.exists(temp_bmp):
            os.remove(temp_bmp)
