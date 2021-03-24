from flask import Response

from src.core import json_utils

Response_Success_Code = 2000
Response_Not_Allow_Method = {'status': 2001, 'message': '请求方法不允许'}
Response_Parameters_Error = {'status': 2002}  # 参数不正确
Response_Option_Error = {'status': 2003}  # 操作失败
Response_Query_Error = {'status': 2004, 'message': '该数据不存在'}
Response_Auth_Error = {'status': 2005}
Response_Pay_Error = {'status': 2006}
Response_Login_Error = {'status': 2007, 'message': '请先登录'}  # 没有登录


def response_suc(d=True, is_all=False):
    if not isinstance(d, dict):
        d = json_utils.to_dict(d, is_all=is_all)
    return response(status=Response_Success_Code, data=d, is_all=is_all)


def response(*args, **kwargs):
    ctx = dict()
    is_all = False
    if len(args) > 0 and isinstance(args[0], dict):
        ctx = args[0]
    else:
        for key, value in kwargs.items():
            if 'is_all' == key:
                is_all = value
            elif value is not None:
                ctx.setdefault(key, value)
    # ctx = {'status': 2000,'data',[]}
    return Response(json_utils.dict_to_str(ctx, is_all=is_all), mimetype='application/json')


def response_parameters_err(str='参数不正确'):
    ctx = Response_Parameters_Error.copy()
    ctx.setdefault('message', str)
    return response(ctx)


def response_option_err(str='操作失败'):
    ctx = Response_Option_Error.copy()
    ctx.setdefault('message', str)
    return response(ctx)


def response_pay_err(str='获取支付信息失败'):
    ctx = Response_Pay_Error.copy()
    ctx.setdefault('message', str)
    return response(ctx)


def response_auth_err(str='没有该权限'):
    ctx = Response_Auth_Error.copy()
    ctx.setdefault('message', str)
    return response(ctx)
