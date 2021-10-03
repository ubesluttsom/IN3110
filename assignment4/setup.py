#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name='instapy',
    version='0.1.0',
    author='Martin Mihle Nygaard',
    author_email='martimn@ifi.uio.no',
    description='Image filters in different python implementations — IN3110 Assignment 4',
    url='https://github.uio.no/IN3110/IN3110-martimn/tree/master/assignment4',
    packages=['instapy', 'instapy.gray', 'instapy.sepia'],
    install_requires=['numba', 'numpy', 'opencv-python'],
    scripts=['bin/instapy']
    )
