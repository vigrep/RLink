"""
注：改文件只在调试环境下使用Flask自带的服务器时起作用，部署到服务器上时，采用uwsgi托管，该文件失效
"""
from app import app

app.run(debug = True)

