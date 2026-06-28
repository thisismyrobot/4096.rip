import os

import generate

import numpy as np


def update_library():
    for i in range(4**6):
        code = np.base_repr(i, base=4).zfill(6)
        profile = generate.KeyProfile(code=''.join([str(int(d) + 1) for d in code]))
        profile.cut_to_stl(os.path.join('library', f'{profile.code}.stl'))


if __name__ == '__main__':
    update_library()
