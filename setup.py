#!/usr/bin/env python

from distutils.core import setup

setup(name="torque-qhistory",
      version="0.1",
      description="Simple script to help view PBS/Torque accounting files",
      author="Adam DeConinck",
      author_email="ajdecon@ajdecon.org",
      url="https://github.com/ajdecon/torque_qhistory",
      scripts=["qhistory"],
      packages=["torque_accounting"],
      license="Apache 2.0")
