@echo off
cd ..
set PYTHONPATH=%CD%
cd integration_tests
echo PYTHONPATH=%PYTHONPATH%

for %%e in (*.py) do python32 %%e