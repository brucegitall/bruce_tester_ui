import sys;
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize  
setup(name = 'pyd',
      ext_modules = cythonize([
      Extension("b_load", [".//py//b_load.py"]),
	  Extension("b_Rlg2Dx_translate", [".//py//b_Rlg2Dx_translate.py"]),
      ]))


	  
