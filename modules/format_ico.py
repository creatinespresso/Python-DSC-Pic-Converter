# modules/format_ico.py

from PIL import Image
from .base_module import ImageFormatBase

class FormatICO(ImageFormatBase):
    def get_params(self):
        return {
            "PARAM_SIZES": {
                "type": "list_of_int_tuples",
                "default": [(16,16), (32,32), (48,48), (64,64), (128,128)]
            }
        }

    def convert(self, input_path, output_path, options):
        """
        Konvertiert ein beliebiges Bild nach ICO (Windows Icon).
        options: z.B. {"PARAM_SIZES": [(16,16), (32,32), (48,48)]}
        """
        with Image.open(input_path) as img:
            sizes = options.get("PARAM_SIZES", [(16,16), (32,32), (48,48), (64,64), (128,128)])
            img.save(output_path, format="ICO", sizes=sizes)
