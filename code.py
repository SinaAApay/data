import web
import urllib,urllib2
import weibo
import pachong

urls=(
        "/","index",
        "/url","askforusercode",
        "/redirecturl","userindex",
        "/beginActivity","designActivity",
        "/error","error"
    )

render=web.template.render('static')

app=web.application(urls,globals())

def getAccesstokenAndSoOn(code):
    #print code
    appkey='1063052666'
    appsecret='c7d48410f4c03b87d5319edf5d544fd6'
    redirecturl='http://0.0.0.0:8080/redirecturl'
    client=weibo.APIClient(app_key=appkey,app_secret=appsecret,redirect_uri=redirecturl)
    r=client.request_access_token(str(code[u'code']))
    web.setcookie('uid',r.uid)
    web.setcookie('access_token',r.access_token)
    web.setcookie('expires_in',r.expires_in)
    client.set_access_token(r.access_token,r.expires_in)
    userinfor={}
    userinfor[u'uid']=r.uid
    userinfor[u'client']=client
    return userinfor

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

    
class error:
    def GET(self):
        return "Sorry,some errors happened,please email us weiyanjie@gmail.com"

class index:
    def GET(self):
        return render.index();
 
class askforusercode:
    def GET(self):
        web.seeother("https://api.weibo.com/oauth2/authorize?client_id=1063052666&redirect_uri=http://0.0.0.0:8080/redirecturl&response_type=code")

class userindex:
    def GET(self):
        code=web.input(code="")
        userinfor=getAccesstokenAndSoOn(code)
        infor=userinfor[u'client'].users.show.get(uid=int(userinfor[u'uid']))
        return render.userindex(infor)

class designActivity:
    def GET(self):
        if web.cookies()!=None:
            cookies=web.cookies()
            p=pachong.pachong()
            friends=[]
            i=2
            try:
                friends=p.getBiFriendsName(uid=int(cookies.uid),i=1)
                while len(p.getBiFriendsName(uid=int(cookies.uid),i=i))>90:
                    friends+=p.getBiFriendsName(uid=int(cookies.uid),i=i)
                    i+=1
            except:
                web.SeeOther("/error")

            return render.designActivity(friends)
        else:
            web.seeother("https://api.weibo.com/oauth2/authorize?client_id=1063052666&redirect_uri=http://0.0.0.0:8080/redirecturl&response_type=code")



if __name__=="__main__":
    app.run()
