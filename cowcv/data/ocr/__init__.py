
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import hashlib
import io
import pathlib
import pickle

from PIL import Image

OCR_DATA_DIR = pathlib.Path(__file__).resolve().parent


def save_roi(img, bb):
    with io.BytesIO() as bio:
        Image.fromarray(img).save(bio, format='png')
        bio.seek(0)
        img_md5 = hashlib.md5(bio.read())
        bio.seek(0)

        png_file = OCR_DATA_DIR.joinpath(
                        img_md5.hexdigest() + '.png')
        if not png_file.exists():
            with open(str(png_file), mode='wb') as f:
                f.write(bio.read())

        pkl_file = OCR_DATA_DIR.joinpath(
                        img_md5.hexdigest() + '.pkl')
        if not pkl_file.exists():
            with open(str(pkl_file), mode='wb') as f:
                pickle.dump(bb, f)


#def ocr_img_iter():
#    glob.glob()
