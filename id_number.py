import qrcode
import base64
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer,SquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask



class DroneTag:

    def __init__(self, name, color):
        front_color = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        back_color = (1, 1, 1)

        self.drone_id = self.generate_drone_id(name)
        self.drone_qr = self.generate_drone_qr(self.drone_id, front_color, back_color)
        self.drone_tag = self.generate_drone_tag(self.drone_qr, self.drone_id, front_color, back_color)

    def save(self, path=None):
        path=f'{self.drone_id}.png'
        self.drone_tag.save(path)

    def generate_drone_tag(self, qr_img, text, front_color, back_color):
        font_size = int(qr_img.width*0.162)
        padding = font_size//4
        font = ImageFont.truetype("./assets/font.otf", font_size)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        new_img = Image.new("RGB", (qr_img.width, qr_img.height + text_height + padding), back_color)
        draw = ImageDraw.Draw(new_img)
        text_x = (new_img.width - text_width) // 2
        draw.text((text_x, 0), text, fill=front_color, font=font)
        new_img.paste(qr_img, (0, text_height + padding))
        return new_img

    def generate_drone_qr(self, data, front_color, back_color):
        qr = qrcode.QRCode(
            version=None,  # auto size
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=20,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(radius_ratio=0.8),
            eye_drawer=SquareModuleDrawer(),
            color_mask=SolidFillColorMask(
                back_color=back_color,
                front_color=front_color,
            ),
        )
        return qr_img.convert("RGB")

    def generate_drone_id(self, name, ids=[]):
        name = name.upper()
        base_number=(ord(name[0]) // 10) * 10
        id_number=f"0{ord(name[0])%10}-"
        temp=""
        if len(name) < 2: name+=name
        for i in name[1:]:
            temp+=str(abs(ord(i)-base_number))
        temp = f"{int(temp)%10000}"
        while int(temp) < 1000: temp+="0"
        id_number+=f"{temp}"
        while id_number in ids: id_number = str(int(id_number[0])+1) + id_number[1:]
        return id_number

if __name__ == "__main__":
    name="Rory"
    color = "#DC141E"

    drone_tag = DroneTag(name, color)
    drone_tag.save()


