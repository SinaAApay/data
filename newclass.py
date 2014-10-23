import web
from code import getClient
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
        status="I invite you all to a activity:"+activityName+",place:"+activityPosition+",time:"+activityTime+",money for each person:"+str(moneyforeach)+"."
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



        
