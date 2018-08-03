import base64
from PIL import Image
from skimage import io
from io import BytesIO
import numpy as np
from skimage.transform import resize, rescale



def image_decoder(base64_string):
	pimg = Image.open(BytesIO(base64.b64decode(base64_string)))
	pimg = np.array(pimg)
	return pimg
	
def resize_image(image):
	image = resize(image,(150,150))
	image = image.astype(np.float32)
	image = [image]
	image = np.array(image)
	image = image.transpose(0,3,1,2)
	return image
