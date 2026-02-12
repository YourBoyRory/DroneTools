import barcode
from barcode.writer import ImageWriter

# Data you want encoded
data = "02-1290"
code128 = barcode.get("Code128", data, writer=ImageWriter())
img = code128.render(
    {
        #"module_width": 0.2,
        #"module_height": 15,
        "quiet_zone": 2,
        "dpi": 600,
        "write_text": False,
        "foreground": (220, 20, 30),
        "background": (1, 1, 1)
    }
)
img.save("test.png")
