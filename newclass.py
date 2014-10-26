import web
from getclient import getClient
import pymongo


render=web.template.render('static')


class sendweibo:
    def POST(self):
        a=web.input()
        cookie=web.cookies()
        i=cookie[u'friendscount']
        namelist=[]
        for index in range(0,int(i)):
            try:
                name=a[str(index)]
                namelist.append(name)
            except:
                continue
        
        activityMoney=a['ActivityMoney']
        activityName=a['ActivityName']
        activityTime=a['ActivityTime']
        activityPosition=a['ActivityPosition']

        moneyforeach=0.0
        moneyforeach=float(activityMoney)/(len(namelist)+1)
        ac=cookie[u'access_token']
        exp=cookie[u'expires_in']
        uid=cookie[u'uid']
        client=getClient(ac,exp)
        status=u"\u6211\u9080\u8bf7\u4f60\u4eec\u53c2\u52a0\u4e00\u4e2a\u6d3b\u52a8:"+activityName+u",\u5730\u70b9:"+activityPosition+u",\u65f6\u95f4:"+activityTime+u",\u6bcf\u4e2a\u4eba\u9700\u0041\u0041\u7684\u91d1\u989d:"+str(moneyforeach)+"."+u"\u70b9\u51fb\u4e0b\u9762\u94fe\u63a5\u53c2\u52a0\u6d3b\u52a8\u54e6\uff1a: "+"http://123.57.11.233/AA "
        for name in namelist:
            status+=" @"+name
        result=client.statuses.update.post(status=status)
        namelist.append(str(cookie[u'screen_name']))
        con=pymongo.Connection("localhost",27017)
        db=con.aapay
        activities=db.activities
        activity={}
        activity[u'uid']=int(cookie[u'uid'])
        activity[u'name']=activityName
        activity[u'weibo_id']=str(result[u'id'])
        activity[u'ifend']=False
        activity[u'place']=activityPosition
        activity[u'money']=activityMoney
        activity[u'date']=activityTime
        activity[u'peopleInvited']=namelist
        peopleIn=[]
        peopleIn.append(str(cookie[u'screen_name']))
        activity[u'peopleIn']=peopleIn
        activity[u'ifclose']=False
        activity[u'ifbegin']=False
        activities.insert(activity)
        users=db.users
        userinfor=users.find_one({"uid":activity[u'uid']})
        if userinfor == None:
            user={}
            user[u'uid']=activity[u'uid']
            acs=[]
            acs.append(activity[u'weibo_id'])
            user[u'activities']=acs
            users.insert(user)
        else:
            acs=userinfor[u'activities']
            acs.append(activity[u'weibo_id'])
            users.update({"uid":activity[u'uid']},{"$set":{'activities':acs}})
        
        web.SeeOther("http://weibo.com")



        
