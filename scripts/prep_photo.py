import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

img = Image.open(sys.argv[1]).convert("RGB")
cut = np.array(remove(img))
alpha = cut[:, :, 3] / 255.0
gray = cv2.cvtColor(cut[:, :, :3], cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
out = (gray * alpha + 255 * (1 - alpha)).astype(np.uint8)
cv2.imwrite("source-prepped.png", out)
print("done: source-prepped.png")
