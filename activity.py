# -*- coding:utf-8 -*-
import os,sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import web
import pymongo
import code
from getclient import getClient
render=web.template.render('/var/www/AA/static')
con=pymongo.Connection('localhost',27017)
db=con.aapay
activities=db.activities
users=db.users

class currentActivity:
    def GET(self):
#	return "hello"
        cookie=web.cookies()
	ac=cookie[u'access_token']
	exp=cookie[u'expires_in']
	client=getClient(ac,exp)
        activityIn=[]
        activityORG=[]
        uid=int(cookie[u'uid'])
        user=users.find_one({'uid':uid})
        if user!=None:
            for ac in user[u'activities']:
                a_activity=activities.find_one({u'weibo_id':ac})
                if a_activity[u'ifend']==False and a_activity[u'ifclose']==False:
                    activityORG.append(a_activity)
        #name=cookie[u'screen_name']
	infor=client.users.show.get(uid=int(cookie[u'uid']))
	name=infor[u'screen_name']
	
        for ac in activities.find():
            if name in ac[u'peopleInvited']:
                if ac[u'ifend']==False and ac[u'ifclose']==False and (ac in  activityORG)==False:
                    activityIn.append(ac)
        return render.currentActivity(activityIn,activityORG)


class pastActivity:
    def GET(self):
        cookie=web.cookies()
        activityIn=[]
        activityORG=[]
        uid=int(cookie[u'uid'])
        user=users.find_one({'uid':uid})
        if user!=None:
            for ac in user[u'activities']:
                a_activity=activities.find_one({u'weibo_id':ac})
                if a_activity[u'ifend']==True:
                    activityORG.append(a_activity)
        #name=cookie[u'screen_name']
	ac=cookie[u'access_token']
	exp=cookie[u'expires_in']
	client=getClient(ac,exp)
	infor=client.users.show.get(uid=int(cookie[u'uid']))
	name=infor[u'screen_name']

        for ac in activities.find():
            if name in ac[u'peopleIn']:
                if ac[u'ifend']==True:
                    if (ac in activityORG)==False:
                        activityIn.append(ac)

        return render.pastActivity(activityIn,activityORG)

class startActivity:
    def POST(self):
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        ac=activities.find_one({u'weibo_id':weibo_id})
        ifbegin=True
        for people in ac[u'peopleInvited']:
            if (people in ac[u'peopleIn'])==False:
                ifbegin=False
                break
        if ifbegin:
            activities.update({u'weibo_id':weibo_id},{'$set':{u'ifbegin':True}})
            web.seeother("/currentActivity")
        else:
            web.seeother("/currentActivity")



class endActivity:
    def POST(self):
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        ac=activities.find_one({u'weibo_id':weibo_id})
        if ac[u'ifbegin']==True:
            activities.update({u'weibo_id':weibo_id},{"$set":{u'ifend':True}})
            web.seeother("/pastActivity")
        else:
            web.seeother("/currentActivity")

class attendActivity:
    def POST(self):
        cookie=web.cookies()
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        ac=activities.find_one({u'weibo_id':weibo_id})
        #name=cookies[u'screen_name']
	acc=cookie[u'access_token']
	exp=cookie[u'expires_in']
	client=getClient(acc,exp)
	infor=client.users.show.get(uid=int(cookie[u'uid']))
	name=infor[u'screen_name']

        if name in ac[u'peopleIn']:
            web.seeother("/currentActivity")
        else:
            peopleIn=ac[u'peopleIn']
            peopleIn.append(name)
            activities.update({u'weibo_id':weibo_id},{"$set":{u'peopleIn':peopleIn}})
            web.seeother("/currentActivity")


class refuseActivity:
    def POST(self):
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        activities.update({u'weibo_id':weibo_id},{"$set":{u'ifclose':True}})
        web.seeother("/currentActivity")

