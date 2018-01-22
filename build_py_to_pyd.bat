SET VS90COMNTOOLS=%VS100COMNTOOLS%
python setup.pyx build_ext --inplace
pause
set des_path=pyd
md %des_path%
copy .\*.pyd .\%des_path%
pause
del .\*.pyc
del .\*.c
del .\*.pyd
rd /s /q .\build
cd .\py
del .\*.pyc
del .\*.c
del .\*.pyd
cd ..\
pause