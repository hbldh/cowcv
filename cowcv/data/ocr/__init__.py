
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

    with open(str(OCR_DATA_DIR.joinpath(str(img_md5) + '.png'))) as f:
        f.write(bio.read())
    with open(str(OCR_DATA_DIR.joinpath(str(img_md5) + '.pkl'))) as f:
        pickle.dump(f, bb)
