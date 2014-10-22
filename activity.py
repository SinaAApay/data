import web
import pymongo
import code

render=web.template.render('static')
con=pymongo.Connection('localhost',27017)
db=con.aapay
activities=db.activities
users=db.users

class currentActivity:
    def GET(self):
        cookie=web.cookies()
        activityIn=[]
        activityORG=[]
        uid=int(cookie[u'uid'])
        user=users.find_one({'uid':uid})
        for ac in user[u'activities']:
            a_activity=activities.find_one({u'weibo_id':ac})
            if a_activity[u'ifend']==False and a_activity[u'ifclose']==False:
                activityORG.append(a_activity)
        name=cookie[u'screen_name']
        for ac in activities.find():
            if name in ac[u'peopleIn']:
                if ac[u'ifend']==False and ac[u'ifclose']==False:
                    activityIn.append(ac)

        return render.currentActivity(activityIn,activityORG)


class pastActivity:
    def GET(self):
        cookie=web.cookies()
        activityIn=[]
        activityORG=[]
        uid=int(cookie[u'uid'])
        user=users.find_one({'uid':uid})
        for ac in user[u'activities']:
            a_activity=activities.find_one({u'weibo_id':ac})
            if a_activity[u'ifend']==True:
                activityORG.append(a_activity)
        name=cookie[u'screen_name']
        for ac in activities.find():
            if name in ac[u'peopleIn']:
                if ac[u'ifend']==True:
                    activityIn.append(ac)

        return render.pastActivity(activityIn,activityORG)


