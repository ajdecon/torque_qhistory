#!/usr/bin/env python

from distutils.core import setup

setup(name="torque-qhistory",
      version="0.3.4.dg",
      description="Simple script to help view PBS/Torque accounting files",
      author="Adam DeConinck / Derek Gottlieb",
      author_email="ajdecon@ajdecon.org, derek.gottlieb@gmail.com",
      url="https://github.com/ajdecon/torque_qhistory",
      scripts=["qhistory"],
      data_files=[('/usr/share/man/man1',['man/qhistory.1'])],
      packages=["torque_accounting"],
      license="Apache 2.0")
