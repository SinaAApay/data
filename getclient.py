import web
import weibo


def getClient(access_token,expires_in):
    appkey='1063052666'
    appsecret='c7d48410f4c03b87d5319edf5d544fd6'
    redirecturl='http://0.0.0.0:8080/redirecturl'
    client=weibo.APIClient(app_key=appkey,app_secret=appsecret,redirect_uri=redirecturl)
    try:
        client.set_access_token(access_token,expires_in)
        return client
    except:
        web.seeother("https://api.weibo.com/oauth2/authorize?client_id=1063052666&redirect_uri=http://0.0.0.0:8080/redirecturl&response_type=code")
#in case accesstoken overtime

