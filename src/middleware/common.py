import json

from flask import request, g

from src.core import logger, response_utils
from src.settings import redis


def get_user(token):
    if token:
        try:
            user_byte = redis.get(token)
            if user_byte:
                user_info = json.loads(user_byte)
                logger.info(user_info)
                principal = user_info.get('principal')
                return principal
        except Exception as e:
            logger.info(e)


def process_request():
    """
    上传时候鉴权处理
    """
    return None
    # print(request.headers)
    # token = request.headers.get('Accesstoken')
    # if token is None:
    #     token = request.headers.get('X-Apihitgou-Accesstoken')
    #     if token is None:
    #         token = request.cookies.get('accessToken')
    # logger.info('accessToken:%s', token)
    # user = get_user(token)
    # if user:
    #     g.user = user
    #     return None
    # else:
    #     return response_utils.response(response_utils.Response_Login_Error)
