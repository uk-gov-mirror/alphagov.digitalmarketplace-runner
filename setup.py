#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

with open('requirements.txt') as reqfile:
      requirements = reqfile.read().split()

setup(name='dmrunner',
      version='1.0.0',
      description='A small utility for running and managing core Digital Marketplace apps.',
      author='Samuel Williams',
      author_email='Samuel.Williams@digital.cabinet-office.gov.uk',
      packages=['dmrunner'],
      install_requires=requirements
  )
