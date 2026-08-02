import argparse
from fileinput import filename
import math
import os
import re
import sys

import shapely.geometry
import trimesh.creation


DEFAULT_EXPORT_TO = '.'


class KeyProfile:
    __DEFAULTS = {
        'blade_height': 5.3,
        'blade_thickness': 1.0,
        'blade_length': 29.5,
        'blade_lift': 0.5,
        'tip_angle': 42.5,
        'pin_1_inset': 5.5,
        'pin_spacing': 19/5.0,
        'depth_1': 0.5,
        'depth_step': 1.0,
        'v_angle': 90.0,
        'bow_height': 5.3 + 5.0,
        'bow_depth': 10.0,
    }
    __CODE_REGEX = re.compile(r'^[1-4]{6}$')

    @classmethod
    def from_parsed_args(cls, args):
        config = dict([(arg, getattr(args, arg) or cls.__DEFAULTS[arg])
                       for arg
                       in cls.__DEFAULTS.keys()])
        return cls(code=args.code, **config)

    @property
    def code(self):
        return self._code

    def __init__(self, code, **kwargs):
        code = str(code)
        if not self.__CODE_REGEX.match(code):
            raise ValueError(f'Invalid code: {code}. Must be 6-digits between 1 and 4.')

        for (key, default) in self.__DEFAULTS.items():
            if key not in kwargs:
                kwargs[key] = default

        for (key, value) in kwargs.items():
            try:
                float(kwargs[key])
            except ValueError:
                raise ValueError(f'Invalid value for {key}: {value}. Must be a number.')

        self._code = code
        self._config = {**kwargs}

    def _blank_polygon(self):
        c = self._config
        tip_angle_rad = math.radians(c['tip_angle'])

        return shapely.geometry.Polygon([
             # Tip point and taper, top.
            (0, c['blade_lift']),
            (c['blade_height'] * math.tan(tip_angle_rad-math.pi), c['blade_height']),
            (c['blade_length'], c['blade_height']),
            
            # Bow.
            (c['blade_length'], c['bow_height']),
            (c['blade_length'] + c['bow_depth'], c['bow_height']),
            (c['blade_length'] + c['bow_depth'], c['blade_lift']),

            # Bottom of blade.
            (c['blade_length'], c['blade_lift']),
        ])

    def _cut(self):
        c = self._config
        key_polygon = self._blank_polygon()
        for (i, depth) in enumerate(self.code):
            depth = int(depth)
            cutting_blade_polygon = shapely.geometry.Polygon([
                # Cutting tip
                (0, 0),
                (c['blade_height'] * math.tan(math.radians(c['v_angle']/2.0)-math.pi), c['blade_height']),
                (-c['blade_height'] * math.tan(math.radians(c['v_angle']/2.0)-math.pi), c['blade_height'])
            ])
            cutting_blade_polygon = shapely.affinity.translate(
                cutting_blade_polygon,
                xoff=(c['blade_length'] - c['pin_1_inset']) - c['pin_spacing'] * i,
                yoff=c['blade_height'] - (c['depth_1'] + c['depth_step'] * (depth - 1))
            )
            key_polygon = key_polygon.difference(cutting_blade_polygon)
 
        return trimesh.creation.extrude_polygon(key_polygon, height=c['blade_thickness'])

    def cut_to_stl(self, path):
        self._cut().export(path, file_type='stl_ascii')


def main(key_profile, destination):
    directory = os.path.abspath(destination)
    if not os.path.exists(directory):
        sys.stderr.write(f'Destination directory does not exist: {directory}\n')
        sys.exit(1)

    safe_path = os.path.join(directory, f'{key_profile.code}.stl')
    key_profile.cut_to_stl(safe_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate BiLock profiles.')
    parser.add_argument('code', type=str, help='The code for the BiLock profile, shoulder-to-tip.')
    parser.add_argument('destination', type=str, nargs='?', default=DEFAULT_EXPORT_TO, help='Destination path for the generated file.')

    # These are good defaults based on measuring a real BiLock key, but they might change a little as I test more.
    parser.add_argument('--blade_height', type=float, help='Height of the blade.')
    parser.add_argument('--tip_angle', type=float, help='Angle of the tip of the blade (from vertical).')
    parser.add_argument('--blade_thickness', type=float, help='Thickness of the blade.')
    parser.add_argument('--blade_length', type=float, help='Length of the blade.')
    parser.add_argument('--blade_lift', type=float, help='Lift of the bottom of the blade to fit the blade under-curve.')
    parser.add_argument('--pin_1_inset', type=float, help='Position of the first pin from shoulder.')
    parser.add_argument('--pin_spacing', type=float, help='Space between pins.')
    parser.add_argument('--depth_1', type=float, help='Depth of a 1 cut.')
    parser.add_argument('--depth_step', type=float, help='Step between pin depths.')
    parser.add_argument('--v_angle', type=float, help='Cut shape.')
    parser.add_argument('--bow_height', type=float, help='Height of the bow.')
    parser.add_argument('--bow_depth', type=float, help='Depth of the bow.')

    args = parser.parse_args()
    profile = KeyProfile.from_parsed_args(args)
    main(profile, args.destination)
