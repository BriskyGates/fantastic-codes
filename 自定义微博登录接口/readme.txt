1.资源注册配置（urls.py）：
api.add_resource(WeiboLoginResource, "/weibo/")

2.微博开放平台的回调url 要修改成 /weibo/


3.OAuth2.0<用户身份鉴权平台>做的工作大致是：开发者在微博开放平台对自己的应用进行注册，
    获取相关的App key 和 App secret 。
    然后在自己的python脚本中填写App key 和 App secret<获取用户身份认证>，
    脚本通过OAuth2.0验证后，就可以发微博，获取用户基本信息etc.

4.开发者调用Sina 开放接口中的许多功能需要授权才能使用，
    也就是获取OAuth2.0返回的AccessToken，然后才能调用相应的API
