import numpy as np
import matplotlib.pyplot as plt

import PIL
from PIL import Image

import sys

# Convert Pixel Value to Digital Number
def gray_to_DN(im, z):
    scale_factor = 2**14/float((np.max(im)-np.min(im)))
    z = np.uint16(z * scale_factor);
    return z

# Convert Digital Number to Temperature
def DN_to_temperature(DN, camera_temperature=20):
    if camera_temperature == 20:
        return (DN-7593)/25
    elif camera_temperature == 38:
        return (DN-8748)/23
    else:
        return -1

class Formatter(object):
    def __init__(self, im):
        self.im = im

    def __call__(self, x, y):
        z = np.array(self.im)[int(y), int(x)]
        DN = gray_to_DN(self.im, z)
        temperature = DN_to_temperature(DN)
        
        return 'x={:.01f}, y={:.01f}, Digital Number={:.01f}, Temperature={:.01f}C'.format(x, y, DN, temperature)

image_path = sys.argv[1]

if not image_path:
    print("Failed to open image!\n")
    sys.exit(0)

image = Image.open(image_path).convert('L')

plt.imshow(image)
plt.gca().format_coord = Formatter(image)

plt.gray()
plt.show()
