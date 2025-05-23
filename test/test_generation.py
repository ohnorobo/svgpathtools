# Note: This file was taken mostly as is from the svg.path module (v 2.0)
#------------------------------------------------------------------------------
from __future__ import division, absolute_import, print_function
import unittest
import re
from typing import Optional

import numpy as np

from svgpathtools import parse_path


_space_or_comma_pattern = re.compile(r'[,\s]+')


def _assert_d_strings_are_almost_equal(d1: str, d2: str, test_case=unittest.TestCase, msg: Optional[str] = None) -> bool:
    """Slight differences are expected on different platforms, check each part is approx. as expected."""

    parts1 = _space_or_comma_pattern.split(d1)
    parts2 = _space_or_comma_pattern.split(d2)
    test_case.assertEqual(len(parts1), len(parts2), msg=msg)
    for p1, p2 in zip(parts1, parts2):
        if p1.isalpha():
            test_case.assertEqual(p1, p2, msg=msg)
        else:
            test_case.assertTrue(np.isclose(float(p1), float(p2)), msg=msg)



class TestGeneration(unittest.TestCase):

    def test_path_parsing(self):
        """Examples from the SVG spec"""
        paths = [
            'M 100,100 L 300,100 L 200,300 Z',
            'M 0,0 L 50,20 M 100,100 L 300,100 L 200,300 Z',
            'M 100,100 L 200,200',
            'M 100,200 L 200,100 L -100,-200',
            'M 100,200 C 100,100 250,100 250,200 S 400,300 400,200',
            'M 100,200 C 100,100 400,100 400,200',
            'M 100,500 C 25,400 475,400 400,500',
            'M 100,800 C 175,700 325,700 400,800',
            'M 600,200 C 675,100 975,100 900,200',
            'M 600,500 C 600,350 900,650 900,500',
            'M 600,800 C 625,700 725,700 750,800 S 875,900 900,800',
            'M 200,300 Q 400,50 600,300 T 1000,300',
            'M -3.4E+38,3.4E+38 L -3.4E-38,3.4E-38',
            'M 0,0 L 50,20 M 50,20 L 200,100 Z',
            'M 600,350 L 650,325 A 25,25 -30 0,1 700,300 L 750,275',
        ]
        float_paths = [
            'M 100.0,100.0 L 300.0,100.0 L 200.0,300.0 L 100.0,100.0',
            'M 0.0,0.0 L 50.0,20.0 M 100.0,100.0 L 300.0,100.0 L 200.0,300.0 L 100.0,100.0',
            'M 100.0,100.0 L 200.0,200.0',
            'M 100.0,200.0 L 200.0,100.0 L -100.0,-200.0',
            'M 100.0,200.0 C 100.0,100.0 250.0,100.0 250.0,200.0 C 250.0,300.0 400.0,300.0 400.0,200.0',
            'M 100.0,200.0 C 100.0,100.0 400.0,100.0 400.0,200.0',
            'M 100.0,500.0 C 25.0,400.0 475.0,400.0 400.0,500.0',
            'M 100.0,800.0 C 175.0,700.0 325.0,700.0 400.0,800.0',
            'M 600.0,200.0 C 675.0,100.0 975.0,100.0 900.0,200.0',
            'M 600.0,500.0 C 600.0,350.0 900.0,650.0 900.0,500.0',
            'M 600.0,800.0 C 625.0,700.0 725.0,700.0 750.0,800.0 C 775.0,900.0 875.0,900.0 900.0,800.0',
            'M 200.0,300.0 Q 400.0,50.0 600.0,300.0 Q 800.0,550.0 1000.0,300.0',
            'M -3.4e+38,3.4e+38 L -3.4e-38,3.4e-38',
            'M 0.0,0.0 L 50.0,20.0 L 200.0,100.0 L 50.0,20.0',
            'M 600.0,350.0 L 650.0,325.0 A 27.9508497187,27.9508497187 -30.0 0,1 700.0,300.0 L 750.0,275.0'
        ]

        for path, expected in zip(paths, float_paths):
            parsed_path = parse_path(path)
            res = parsed_path.d()
            msg = ('\npath =\n {}\nexpected =\n {}\nparse_path(path).d() =\n {}'
                   ''.format(path, expected, res))
            _assert_d_strings_are_almost_equal(res, expected, self, msg)


    def test_normalizing(self):
        # Relative paths will be made absolute, subpaths merged if they can,
        # and syntax will change.
        path = 'M0 0L3.4E2-10L100.0,100M100,100l100,-100'
        ps = 'M 0,0 L 340,-10 L 100,100 L 200,0'
        psf = 'M 0.0,0.0 L 340.0,-10.0 L 100.0,100.0 L 200.0,0.0'
        self.assertTrue(parse_path(path).d() in (ps, psf))


if __name__ == '__main__':
    unittest.main()
