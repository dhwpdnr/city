import os, sys

port = sys.argv

if len(port) == 1:
    port = 8000
elif len(port) == 2:
    port = port[1]
else:
    print("\n [Error] 인자가 많습니다. 하나의 인자만 입력해주세요. \n")

os.system(f"python manage.py runserver 0.0.0.0:{port} --settings=config.settings.local")
