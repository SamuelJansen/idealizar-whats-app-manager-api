from io import BytesIO
import base64
from PIL import Image

from python_helper import Constant as c
from python_framework import Service, ServiceMethod

from dto import QRCodeDto

@Service()
class ImageService :

    @ServiceMethod(requestClass=[str, str])
    def save(self, imageAsBase64, pathWithNameAndExtension) :
        image = Image.open(BytesIO(self.helper.base64.decode(imageAsBase64)))
        image.save(pathWithNameAndExtension)
        return image
