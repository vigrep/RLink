"""
正式服务器部署时，uwsgi配置文件中app参数应该指定的文件
"""
from app import create_app

app = create_app('production')
