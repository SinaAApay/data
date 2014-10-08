import web
import urllib,urllib2
import weibo


urls=(
        "/","index",
        "/url","askforusercode",
        "/redirecturl","userindex"
    )

render=web.template.render('static')

app=web.application(urls,globals())

def getAccesstokenAndSoOn(code):
    print code
    appkey='1063052666'
    appsecret='c7d48410f4c03b87d5319edf5d544fd6'
    redirecturl='http://0.0.0.0:8080/redirecturl'
    client=weibo.APIClient(app_key=appkey,app_secret=appsecret,redirect_uri=redirecturl)
    r=client.request_access_token(str(code[u'code']))
    client.set_access_token(r.access_token,r.expires_in)
    userinfor={}
    userinfor[u'uid']=r.uid
    userinfor[u'client']=client
    return userinfor

    
    

class index:
    def GET(self):
        return render.index();

class askforusercode():
    def GET(self):
        web.seeother("https://api.weibo.com/oauth2/authorize?client_id=1063052666&redirect_uri=http://0.0.0.0:8080/redirecturl&response_type=code")

class userindex():
    def GET(self):
        code=web.input(code="")
        userinfor=getAccesstokenAndSoOn(code)
        infor=userinfor[u'client'].users.show.get(uid=int(userinfor[u'uid']))
        return render.userindex(infor)
        



if __name__=="__main__":
    app.run()
