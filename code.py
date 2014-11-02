# -*- coding:utf-8 -*-
import os,sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import web
import urllib,urllib2
import weibo
import pachong
import newclass
import activity
from getclient import getClient
urls=(
        "/","index",
        "/url","askforusercode",
        "/redirecturl","getCodeSetCookie",
        "/beginActivity","designActivity",
        "/error","error",
        "/sendBeginWeibo","newclass.sendweibo",
        "/currentActivity","activity.currentActivity",
        "/pastActivity","activity.pastActivity",
        "/userindex","userindex",
        "/startActivity","activity.startActivity",
        "/endActivity","activity.endActivity",
        "/attendActivity","activity.attendActivity",
        "/refuseActivity","activity.refuseActivity",
        "/us","us",
        "/deletePastActivity","activity.deletePastActivity"

    )

render=web.template.render('/home/rw/workplace/aapay/data/static')

app=web.application(urls,globals())
application=app.wsgifunc()
def getAccesstokenAndSoOn(code):
    #print code
    appkey='3541987275'
    appsecret='9e2cca6d2f735a7ebee4999ac6608231'
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

class us:
    def GET(self):
        return render.us()



class error:
    def GET(self):
        return "Sorry,some errors happened,please email us weiyanjie@gmail.com"

class index:
    def GET(self):
        return render.index();
 
class askforusercode:
    def GET(self):
        web.seeother("https://api.weibo.com/oauth2/authorize?client_id=3541987275&redirect_uri=http://0.0.0.0:8080/redirecturl&response_type=code")


class getCodeSetCookie:
    def GET(self):
        code=web.input(code="")
        if len(code[u'code'])>1:
            userinfor=getAccesstokenAndSoOn(code)
            infor=userinfor[u'client'].users.show.get(uid=int(userinfor[u'uid']))
            web.setcookie('screen_name',infor[u'screen_name'])
        
        web.seeother("/userindex")

class userindex:
    def GET(self):
        cookies=web.cookies()
        ac=cookies[u'access_token']
        expires_in=cookies[u'expires_in']
        client=getClient(ac,expires_in)
        infor=client.users.show.get(uid=int(cookies[u'uid']))
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

            web.setcookie("friendscount",len(friends))
            return render.designActivity(friends)
        else:
            web.seeother("https://api.weibo.com/oauth2/authorize?client_id=3541987275&redirect_uri=http://0.0.0.0:8080/redirecturl&response_type=code")


if __name__=="__main__":
    app.run()
