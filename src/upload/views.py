import datetime
import os

from PIL import Image
from flask import Blueprint, request, g

from src.core import response_utils
from src.middleware.common import process_request
from src.settings import BASE_DIR, BASE_URL, File_Types

upload = Blueprint('upload', __name__)

upload.before_request(process_request)

UpLoad_Dir = os.path.join(BASE_DIR, 'upload')

for f_type in File_Types:
    path = os.path.join(UpLoad_Dir, f_type)
    if not os.path.exists(path):
        os.makedirs(path)


def time_str():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')


def date_str():
    return datetime.datetime.now().strftime('%Y%m%d')


def get_file_name(user_id, filename):
    name = user_id + time_str()
    if '.' in filename:
        name = name + '.' + filename.rsplit('.', 1)[1].lower()
    return name


def get_img_size(file_path):
    w = None
    h = None
    if os.path.exists(file_path):
        try:
            im = Image.open(file_path)
            if im:
                w, h = im.size
        except IOError:
            pass
    return w, h


@upload.route('/<file_type>', methods=['POST'])
def upload_file(file_type):
    if file_type not in File_Types:
        return response_utils.response_parameters_err("文件类型不正确")
    if 'files' not in request.files:
        return response_utils.response_parameters_err("没提交文件内容")
    # user_id = str(g.user['id'])
    user_id = 1  # 加了鉴权后可以添加获取上传者信息
    date_dir = date_str()
    file_dir = os.path.join(UpLoad_Dir, file_type, date_dir)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    paths = []
    base_path = BASE_URL + 'get/' + file_type + '/'
    for f in request.files.getlist('files'):
        file_name = get_file_name(user_id, f.filename)
        file_path = os.path.join(file_dir, file_name)
        f.save(file_path)
        url = base_path + date_dir + '/' + file_name
        if 'img' == file_type:
            w, h = get_img_size(file_path)
            if w and h:
                url = url + '?_htwh=%s&_htht=%s' % (w, h)
        paths.append(url)
    return response_utils.response_suc(paths)


def upload_qr():
    if 'files' not in request.files:
        return response_utils.response_parameters_err("没提交文件内容")
    from src.settings import WHITE_HOSTS
    if request.remote_addr not in WHITE_HOSTS:
        return response_utils.response_auth_err()
    file_type = 'img'
    qr_dir = 'qr'
    file_dir = os.path.join(UpLoad_Dir, file_type, qr_dir)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    paths = []
    base_path = BASE_URL + 'get/' + file_type + '/' + qr_dir
    for f in request.files.getlist('files'):
        file_path = os.path.join(file_dir, f.filename)
        if not os.path.exists(file_path):
            f.save(file_path)
        url = base_path + '/' + f.filename
        w, h = get_img_size(file_path)
        if w and h:
            url = url + '?_htwh=%s&_htht=%s' % (w, h)
        paths.append(url)
    return response_utils.response_suc(paths)
