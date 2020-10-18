import json

import requests
from flask import Blueprint, render_template, session, jsonify,request
from flask_restful import Resource


# weibo_blue = Blueprint('weibo', __name__)


# @weibo_blue.route('/weibo_login/')
# def weibo_login():
#     return render_template('login_weibo.html')


# 登录完微博后,跳到这个视图函数中处理
# 获得参数: code--->access_token--->uid--->
# @weibo_blue.route('/weibo_auth/', method=['GET'])
class WeiboLoginResource(Resource):
    def get(self):
        code=request.args.get('code')
        print('--------')
        print(code)
        weibo_access_url = 'https://api.weibo.com/oauth2/access_token'
        params = {
            'client_id': '2217088527',
            'client_secret': '471878a0a07ccc5f8585c41217c58d1d',
            'grant_type': 'authorization_code',
            'code': request.args.get('code'),  # 获得code
            'redirect_uri': 'http://127.0.0.1:5000/weibo/'
        }
        resp = requests.post(weibo_access_url, data=params)
        json_data = resp.json()
        print(json_data)

        access_token = json_data.get('access_token')  # 获得access_token

        get_userid_url = f'https://api.weibo.com/2/account/get_uid.json?access_token={access_token}'
        uid = requests.get(get_userid_url).json().get('uid')  # 获得uid

        user_url = "https://api.weibo.com/2/users/show.json"
        info_url = user_url + f"?access_token={access_token}&uid={uid}"

        info_str = requests.get(info_url).text

        info_dict = json.loads(info_str)
        print(info_dict)

        uname = info_dict['screen_name']
        session['uname'] = uname  # 设置登录成功标志
        return jsonify({
            'uname': uname,
            'msg': '微博登录成功',
            'status': 'WEIBO_LOGIN_OK'
        })


if __name__ == '__main__':
    print('提交新代码')