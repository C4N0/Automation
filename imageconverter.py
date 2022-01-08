from PIL import Image
import glob

png_list = glob.glob('C:\\Users\matt_\\PycharmProjects\\pythonProject\\imageconversion\\*.png')

for file in png_list:
    im = Image.open(file)
    rgb_im = im.convert("RGB")
    rgb_im.save(file.replace("png", "jpg"), quality = 95)