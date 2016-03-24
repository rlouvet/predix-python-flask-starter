activate env1
pip freeze > requirements.txt
pip install --download vendor -r requirements.txt --no-use-wheel
set ERRORLEVEL=0