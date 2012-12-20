torque_qhistory
=================

`qhistory` is a basic script to make it easier to view PBS Torque accounting logs.
It also installs a new python module "torque_accounting" which encapsulates the actual 
parsing logic. The easiest way to understand it is to read the code (it's very simple.)

## To build and install as an RPM ##
0. To build the man pages into the RPM, add the following line to ~/.rpmmacros:
    `%__os_install_post %{nil}`
1. `python setup.py bdist_rpm`
2. `sudo yum localinstall dist/torque-qhistory-0.1-1.noarch.rpm`

You can also just run qhistory directly from a git checkout. Make sure you have 
Python argparse on your system (added to standard library in Python 2.7, but 
EL 6 is still on 2.6 so you need to install separately).
