from PIL import Image

image = Image.open('crosshair.png')

image = image.convert("RGBA")

data = image.getdata()

new_data = []
for item in data:
    if item[:3] == (255, 255, 255):
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)

image.putdata(new_data)

image.save('useable_crosshair.png')
