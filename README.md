torque_qhistory
=================

`qhistory` is a basic script to make it easier to view PBS Torque accounting logs.
It also installs a new python module "torque_accounting" which encapsulates the actual 
parsing logic. The easiest way to understand it is to read the code (it's very simple.)

## To build and install as an RPM ##
1. `python setup.py bdist_rpm`
2. `sudo yum localinstall dist/torque-qhistory-0.1-1.noarch.rpm`
