"""
High quality quantization for Pillow images.

Pillow uses Euclidean distance for color matching during quantization, which yields poor results
when using RGB due to the nonlinearity of color perception. YCbCr is a better fit for Euclidean
distance, but Pillow does not natively support quantization of such images.

This module improves the quantization by converting the images to YCbCr, and then tricking
Pillow into thinking it's an RGB image so quantization works.
"""

__version__ = '0.1.0'

from PIL import Image
from typing import List, Tuple, Union

def quantize(
	image: Image,
	palette: bytes,
	colorspace: str = 'YCbCr',
	dither: Union[int, Image.Dither] = Image.Dither.FLOYDSTEINBERG
) -> Image:
	"""
	Quantizes an image using a specified color palette.

	Args:
		img (Image): The input image to be quantized.
		palette (bytes): A byte string representing the RGB color palette.
		colorspace (str, optional): The color space to use for conversion. Can be any of the
		    colorspaces supported by Pillow. Defaults to 'YCbCr'.
		dither (Union[int, Image.Dither], optional): The dithering method to apply.
			Defaults to Floyd-Steinberg.

	Returns:
		Image: The quantized image with the applied palette.
	"""

	# Convert all colors in palette from RGB to intermediate color space by drawing it in a RGB
	# picture and then converting it.
	int_pal_pixels = Image.frombytes('RGB', (len(palette) // 3, 1), palette)
	int_pal_pixels = int_pal_pixels.convert(colorspace)

	# We need to convert it to a fake RGB picture, or else funny things happen when calling the
	# tobytes() method down below.
	int_pal_pixels = Image.merge('RGB', int_pal_pixels.split())

	# Create the image containing the palette
	int_pal = Image.new('P', (1, 1))
	int_pal.putpalette(int_pal_pixels.tobytes())

	# Convert image to intermediate color space, but pretend it's RGB so dithering works
	result = Image.merge('RGB', image.convert(colorspace).split())

	# Quantize, with dithering if enabled
	result = result.quantize(dither=dither, palette=int_pal)

	# Swap palette with real RGB one
	result.putpalette(palette)

	return result

def cover(image: Image, size: Tuple[int, int]) -> Image:
	"""
	Utility method to resize and crop an image to cover the specified dimensions.

	Args:
		image (Image): The input image to be resized and cropped.
		size (Tuple[int, int]): The target size (width, height) for the output image.

	Returns:
		Image: The resized and cropped image.
	"""

	ratio = max(size[0] / image.width, size[1] / image.height)
	if ratio != 1:
		image = image.resize((round(image.width * ratio), round(image.height * ratio)))
		crop_start = (
			round((image.width - size[0]) / 2),
			round((image.height - size[1]) / 2),
		)
		image = image.crop((
			crop_start[0],
			crop_start[1],
			crop_start[0] + size[0],
			crop_start[1] + size[1],
		))
	return image
