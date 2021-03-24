import os
from PIL import Image
from src.upload.views import UpLoad_Dir

Mode_Dict = {
    '.jpeg': 'RGB',
    '.jpg': 'RGB',
    '.png': 'RGBA',
    '.webp': 'RGB'
}


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


Temp_Dir = os.path.join(UpLoad_Dir, 'temp')
if not os.path.exists(Temp_Dir):
    os.makedirs(Temp_Dir)
else:
    del_file(Temp_Dir)


def deal_im(im, mode, w, h, fmt, ext):
    im = resize_img(im, mode, w, h)
    img_mode = im.mode
    if fmt:
        target_mode = Mode_Dict.get('.' + fmt)
        if target_mode:
            ext = '.' + fmt
    if ext:
        ext = ext.lower()
    target_mode = Mode_Dict.get(ext)
    if target_mode and target_mode != img_mode:
        im = im.convert(target_mode)
    return im, ext


def get_filename_and_ext(file_path):
    name = ''
    ext = ''
    if file_path:
        file_name = os.path.split(file_path)[1]
        name, ext = os.path.splitext(file_name)
    return name, ext


def deal_normal_img(file_path, im, mode, w, h, fmt):
    name, ext = get_filename_and_ext(file_path)
    im, ext = deal_im(im, mode, w, h, fmt, ext)
    temp_path = os.path.join(Temp_Dir, name + ext)
    im.save(temp_path)
    return temp_path


def deal_gif_img(file_path, im, mode, w, h, fmt):
    if fmt and 'gif' != fmt:
        return deal_normal_img(file_path, im, mode, w, h, fmt)
    else:
        loop = im.info['loop']
        durations = []
        img_list = []
        # imgs = [f.copy() for f in ImageSequence.Iterator(im)]
        if im.n_frames == 0:
            return None
        file_name = os.path.split(file_path)[1]
        name, ext = os.path.splitext(file_name)
        try:
            im.seek(0)
            while True:
                durations.append(im.info['duration'])
                frame, ext = deal_im(im.copy(), mode, w, h, fmt, ext)
                img_list.append(frame)
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        temp_path = os.path.join(Temp_Dir, name + ext)
        img_list[0].save(temp_path, 'gif', save_all=True, append_images=img_list[1:], disposal=2, loop=loop,
                         duration=durations, optimize=False)
        return temp_path


def deal_img(option_str, file_path):
    temp_file = None
    if option_str and os.path.exists(file_path):
        try:
            mode, w, h, fmt = deal_option(option_str)
            im = Image.open(file_path)
            if 'GIF' == im.format:
                temp_file = deal_gif_img(file_path, im, mode, w, h, fmt)
            else:
                temp_file = deal_normal_img(file_path, im, mode, w, h, fmt)
        except Exception as e:
            print(e)
            pass
    return temp_file


def change_w_h(w, h):
    return h, w


def get_mode_0_size(iw, ih, w, h):
    if w > 0 or h > 0:
        if w == 0:
            w = iw
        if h == 0:
            h = ih
        scale = scale_x = iw / w
        scale_y = ih / h
        if scale_x < scale_y:
            scale = scale_y
        if scale > 1:
            return round(iw / scale), round(ih / scale)
    return None, None


def get_img_mode_0(im, w, h):
    iw, ih = im.size
    if iw < ih:
        w, h = change_w_h(w, h)
    rw, rh = get_mode_0_size(iw, ih, w, h)
    if rw and rh:
        im = im.resize((rw, rh), Image.ANTIALIAS)
    return im


def get_mode_1_size(iw, ih, w, h):
    scale_i = iw / ih
    scale = w / h
    if scale_i < scale:
        return iw, round(iw / scale)
    elif scale_i > scale:
        return round(ih * scale), ih
    return None, None


def get_img_mode_1(im, w, h):
    if w > 0 or h > 0:
        need_resize = False
        if w == 0:
            w = h
            need_resize = True
        if h == 0:
            h = w
            need_resize = True
        iw, ih = im.size
        rw, rh = get_mode_1_size(iw, ih, w, h)
        if rw and rh:
            x0 = round((iw - rw) / 2)
            y0 = round((ih - rh) / 2)
            x1 = x0 + rw
            y1 = y0 + rh
            im = im.crop((x0, y0, x1, y1))
            if x1 != iw or y1 != ih:
                need_resize = True
        if need_resize:
            im = im.resize((w, h), Image.ANTIALIAS)
    return im


def get_img_mode_2(im, w, h):
    iw, ih = im.size
    rw, rh = get_mode_0_size(iw, ih, w, h)
    if rw and rh:
        im = im.resize((rw, rh), Image.ANTIALIAS)
    return im


def get_mode_3_size(iw, ih, w, h):
    if w > 0 or h > 0:
        if w == 0:
            w = iw
        if h == 0:
            h = ih
        scale = scale_x = iw / w
        scale_y = ih / h
        if scale_x > scale_y:
            scale = scale_y
        if scale > 1:
            return round(iw / scale), round(ih / scale)
    return None, None


def get_img_mode_3(im, w, h):
    iw, ih = im.size
    rw, rh = get_mode_3_size(iw, ih, w, h)
    if rw and rh:
        im = im.resize((rw, rh), Image.ANTIALIAS)
    return im


def get_img_mode_4(im, w, h):
    iw, ih = im.size
    if iw < ih:
        w, h = change_w_h(w, h)
    rw, rh = get_mode_3_size(iw, ih, w, h)
    if rw and rh:
        im = im.resize((rw, rh), Image.ANTIALIAS)
    return im


def get_img_mode_5(im, w, h):
    if w > 0 or h > 0:
        if w == 0:
            w = h
        if h == 0:
            h = w
        iw, ih = im.size
        if iw < ih:
            w, h = change_w_h(w, h)
        rw, rh = get_mode_1_size(iw, ih, w, h)
        if rw and rh:
            x0 = round((iw - rw) / 2)
            y0 = round((ih - rh) / 2)
            x1 = x0 + rw
            y1 = y0 + rh
            im = im.crop((x0, y0, x1, y1))
            if x1 != iw or y1 != ih:
                im = im.resize((w, h), Image.ANTIALIAS)
    return im


def resize_img(im, mode, w, h):
    if 0 == mode:
        im = get_img_mode_0(im, w, h)
    elif 1 == mode:
        im = get_img_mode_1(im, w, h)
    elif 2 == mode:
        im = get_img_mode_2(im, w, h)
    elif 3 == mode:
        im = get_img_mode_3(im, w, h)
    elif 4 == mode:
        im = get_img_mode_4(im, w, h)
    elif 5 == mode:
        im = get_img_mode_5(im, w, h)
    return im


def deal_option(option_str):
    mode = '0'
    w = 0
    h = 0
    fmt = None
    if option_str:
        options = option_str.split('/')
        length = len(options)
        for i in range(0, length):
            if 'imageView2' == options[i] and i + 1 < length:
                mode = int(options[i + 1])
            elif 'w' == options[i] and i + 1 < length:
                w = int(options[i + 1])
            elif 'h' == options[i] and i + 1 < length:
                h = int(options[i + 1])
            elif 'format' == options[i] and i + 1 < length:
                fmt = options[i + 1]
                if fmt:
                    fmt = fmt.lower()
    return mode, w, h, fmt
