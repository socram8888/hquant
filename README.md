# hquant

High quality quantization for [Pillow](https://python-pillow.org/) images.

Pillow uses Euclidean distance for color matching during quantization, which yields poor results
when using RGB due to the nonlinearity of color perception. YCbCr is a better fit for Euclidean
distance, but Pillow does not natively support quantization of such images.

This module improves the quantization by converting the images to YCbCr, and then tricking
Pillow into thinking it's an RGB image so quantization works.

## Samples

The following samples dither the original image to the classic 16 colors supported in all terminals,
using RGB (as Pillow quantize method would normally use), CIELAB and YCbCr.

| Original                                                                                              | RGB                                                                                                   | CIELAB                                                                                                   | YCbCr                                                                                                     |
| ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| ![Original Lena](https://github.com/socram8888/hquant/blob/master/samples/lena_orig.png?raw=true)     | ![Lena using RGB](https://github.com/socram8888/hquant/blob/master/samples/lena_rgb.png?raw=true)     | ![Lena using CIELAB](https://github.com/socram8888/hquant/blob/master/samples/lena_lab.png?raw=true)     | ![Lena using YCbCr](https://github.com/socram8888/hquant/blob/master/samples/lena_ycbcr.png?raw=true)     |
| ![Original Kobold](https://github.com/socram8888/hquant/blob/master/samples/kobold_orig.png?raw=true) | ![Kobold using RGB](https://github.com/socram8888/hquant/blob/master/samples/kobold_rgb.png?raw=true) | ![Kobold using CIELAB](https://github.com/socram8888/hquant/blob/master/samples/kobold_lab.png?raw=true) | ![Kobold using YCbCr](https://github.com/socram8888/hquant/blob/master/samples/kobold_ycbcr.png?raw=true) |

## Usage example

```python
from PIL import Image
import hquant

terminal_palette = bytes([
	# Primary 3-bit (8 colors). Unique representation!
	0x00, 0x00, 0x00,
	0x80, 0x00, 0x00,
	0x00, 0x80, 0x00,
	0x80, 0x80, 0x00,
	0x00, 0x00, 0x80,
	0x80, 0x00, 0x80,
	0x00, 0x80, 0x80,
	0xc0, 0xc0, 0xc0,

	# Equivalent "bright" versions of original 8 colors.
	0x80, 0x80, 0x80,
	0xff, 0x00, 0x00,
	0x00, 0xff, 0x00,
	0xff, 0xff, 0x00,
	0x00, 0x00, 0xff,
	0xff, 0x00, 0xff,
	0x00, 0xff, 0xff,
	0xff, 0xff, 0xff,
])

original = Image.open('lena.png')
dithered = hquant.quantize(original, terminal_palette)
dithered.save('dithered.png')
```
