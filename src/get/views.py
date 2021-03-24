import os

from flask import Blueprint, abort, send_file, request

from src.get.img_utils import deal_img
from src.settings import File_Types
from src.upload.views import UpLoad_Dir

get = Blueprint('get', __name__)


@get.route('/<file_type>/<path:file_name>',)
def get_file(file_type, file_name):
    if file_type not in File_Types or not file_name:
        return abort(404)
    file_path = os.path.join(UpLoad_Dir, file_type, file_name)
    if not os.path.exists(file_path):
        return abort(404)
    tmp_img_path = None
    if 'img' == file_type and 'imageView2' in str(request.query_string, 'utf-8'):
        if request.args:
            option_str = None
            for k in request.args.keys():
                if 'imageView2' in k:
                    option_str = k
                    break
            tmp_img_path = deal_img(option_str, file_path)
            if tmp_img_path:
                file_path = tmp_img_path
    rv = send_file(file_path, as_attachment=True, conditional=True)
    if file_type in ('img', 'video'):
        del rv.headers['Content-Disposition']
    if tmp_img_path and os.path.exists(tmp_img_path):   # Window上在返回前删除文件会报错，MAC OS和linux服务器上没问题
        os.remove(tmp_img_path)
    return rv
