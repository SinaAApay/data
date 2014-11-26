import web
import weibo


def getClient(access_token,expires_in):
    appkey='3541987275'
    appsecret='9e2cca6d2f735a7ebee4999ac6608231'
    redirecturl='http://0.0.0.0:8080/redirecturl'
    client=weibo.APIClient(app_key=appkey,app_secret=appsecret,redirect_uri=redirecturl)
    try:
        client.set_access_token(access_token,expires_in)
        return client
    except:
        web.seeother("https://api.weibo.com/oauth2/authorize?client_id=3541987275&redirect_uri=http://0.0.0.0:8080/redirecturl&response_type=code")
#in case accesstoken overtime

