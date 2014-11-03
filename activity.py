# -*- coding:utf-8 -*-
import os,sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import web
import pymongo
import code
from getclient import getClient
render=web.template.render('/home/rw/workplace/aapay/data/static')
con=pymongo.Connection('localhost',27017)
db=con.aapay
activities=db.activities
users=db.users
def refreshInformations(informations,string):
    if len(informations)<5:
        informations.append(string)
    else:
        del informations[0]
        informations.insert(4,string)
    return informations



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
        ac=cookie[u'access_token']
	exp=cookie[u'expires_in']
	client=getClient(ac,exp)
	infor=client.users.show.get(uid=int(cookie[u'uid']))
	name=infor[u'screen_name']

        if user!=None:
            for ac in user[u'activities']:
                a_activity=activities.find_one({u'weibo_id':ac})
                if a_activity[u'ifend']==True:
                    if name in a_activity[u'peopleIn']:
                        activityORG.append(a_activity)
        #name=cookie[u'screen_name']
	
        for ac in activities.find():
            if name in ac[u'peopleIn']:
                if ac[u'ifend']==True:
                    if (ac in activityORG)==False:
                        if name in ac[u'peopleIn']:
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
            string=name+u"\u53c2\u52a0\u4e86\u6d3b\u52a8\u003a"+":"+ac[u'name']
            user=users.find_one({u"uid":ac[u'uid']})
            informations=user[u'informations']
            informations=refreshInformations(informations,string)
            users.update({u"uid":ac[u"uid"]},{"$set":{u"informations":informations}})
            activities.update({u'weibo_id':weibo_id},{"$set":{u'peopleIn':peopleIn}})
            web.seeother("http://alipay.com")
            #web.seeother("/currentActivity")


class refuseActivity:
    def POST(self):
        cookie=web.cookies()
        webinput=web.input()
        acc=cookie[u'access_token']
	exp=cookie[u'expires_in']
	client=getClient(acc,exp)
	infor=client.users.show.get(uid=int(cookie[u'uid']))
	name=infor[u'screen_name']
        weibo_id=webinput[u'weibo_id']
        ac=activities.find_one({u'weibo_id':weibo_id})
        user=users.find_one({u"uid":ac[u'uid']})
        string=name+u"\u62d2\u7edd\u53c2\u52a0\u6d3b\u52a8\uff1a"+ac[u'name']+u"\uff0c\u6d3b\u52a8\u5df2\u7ecf\u5173\u95ed"+"."
        informations=user[u'informations']
        informations=refreshInformations(informations,string)
        users.update({u"uid":ac[u"uid"]},{"$set":{u"informations":informations}})

        activities.update({u'weibo_id':weibo_id},{"$set":{u'ifclose':True}})
        web.seeother("/currentActivity")


class deletePastActivity:
    def POST(self):
        cookie=web.cookies()
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        uid=int(cookie[u'uid'])
        ac=cookie[u'access_token']
	exp=cookie[u'expires_in']
	client=getClient(ac,exp)
	infor=client.users.show.get(uid=int(cookie[u'uid']))
	name=infor[u'screen_name']
        a=activities.find_one({u"weibo_id":weibo_id})
        peopleIn=a[u'peopleIn']
        if name in peopleIn:
            peopleIn.remove(name)
        if len(peopleIn)==0:
            activities.remove({u'weibo_id':weibo_id})
            user=users.find_one({u'uid':a[u'uid']})
            acids=user[u'activities']
            acids.remove(weibo_id)
            users.update({u'uid':a[u'uid']},{"$set":{u'activities':acids}})
        else:
            activities.update({u'weibo_id':weibo_id},{"$set":{u'peopleIn':peopleIn}})
        web.seeother("/pastActivity")



