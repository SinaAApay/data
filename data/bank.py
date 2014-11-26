# -*- coding:utf-8 -*-
import os,sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
import web
import pymongo
from getclient import getClient
from newclass import getClientName
render=web.template.render('static')
con=pymongo.Connection('localhost',27017)
db=con.aapay
activities=db.activities
users=db.users
bank=db.bank

def refreshInformations(informations,string):
    if len(informations)<5:
        informations.append(string)
    else:
        del informations[0]
        informations.insert(4,string)
    return informations

class fillmoney:
    def POST(self):
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        ac=activities.find_one({u'weibo_id':weibo_id})
        cookies=web.cookies()
        myuid=cookies[u'uid']
        act=cookies[u'access_token']
        exp=cookies[u'expires_in']
        client=getClient(act,exp)
        myname=getClientName(client,int(myuid))
        hostuid=ac[u'uid']
        hostname=ac[u'peoplePay'][0]
        if myname in ac['peoplePay']:
            return "Already payed,take it easy"
        else:
            paymoney=float(ac[u'fillmoney'])
            myacount=bank.find_one({u'name':myname})
            money=myacount[u'money']-paymoney
            bank.update({u'name':myname},{"$set":{u'money':money}})
            hostacount=bank.find_one({u'name':hostname})
            money=hostacount[u'money']+paymoney
            bank.update({u'name':hostname},{"$set":{u'money':money}})
            host=users.find_one({u'uid':hostuid})
            string=myname+u'\u652f\u4ed8\u4e86\u6d3b\u52a8\uff1a'+ac[u'name']
            informations=refreshInformations(host[u'informations'],string)
            users.update({u'uid':hostuid},{"$set":{u'informations':informations}})
            peoplepay=ac[u'peoplePay']
            peoplepay.append(myname)
            activities.update({u'weibo_id':weibo_id},{"$set":{u'peoplePay':peoplepay}})
            ifpayend=False
            for people in ac[u'peopleIn']:
                if people in peoplepay:
                    ifpayend=True
                else:
                    ifpayend=False
                    break
            if ifpayend:
                activities.update({u'weibo_id':weibo_id},{"$set":{u'fillmoney':0.0}})
            web.seeother("/pastActivity")

class setFillMoney:
    def POST(self):
        webinput=web.input()
        fillMoney=webinput[u'fillMoney']
        weibo_id=webinput[u'weibo_id']
        print fillMoney
        print weibo_id
        ac=activities.find_one({u'weibo_id':weibo_id})
        peoplePay=[]
        peoplePay.append(ac[u'peoplePay'][0])
        activities.update({u'weibo_id':weibo_id},{'$set':{u'fillmoney':fillMoney}})
        activities.update({u'weibo_id':weibo_id},{'$set':{u'peoplePay':peoplePay}})
        cookies=web.cookies()
        act=cookies[u'access_token']
        exp=cookies[u'expires_in']
        client=getClient(act,exp)
        uid=cookies[u'uid']
        status=u"\u6d3b\u52a8\u003a"+ac[u'name']+u'\u0020\u9700\u8981\u8865\u6b3e\uff0c\u6bcf\u4eba\uff1a'+fillMoney+u'.'+u'\u8bf7\u70b9\u51fb\u94fe\u63a5\u8865\u6b3e'+u'\u94fe\u63a5\uff1a'+u'http://123.57.11.233'
        for people in ac[u'peopleInvited']:
            status+=" @"+people
        client.statuses.update.post(status=status)
        web.seeother("http://weibo.com")

class startFill:
    def POST(self):
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        return render.fillingMoney(weibo_id)
class refund:
    def POST(self):
        #we should add an information after refund
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        refundMoney=float(webinput[u'refundMoney'])
        ac=activities.find_one({u"weibo_id":weibo_id})
        peopleInvited=ac[u'peopleInvited']
        count=0
        hostname=ac[u'peoplePay'][0]
        for people in peopleInvited:
            if people==hostname:
                continue
            else:
                peopleacount=bank.find_one({u"name":people})
                money=peopleacount[u'money']+refundMoney
                bank.update({u'name':people},{"$set":{u'money':money}})
                hostacount=bank.find_one({u"name":hostname})
                money=hostacount[u'money']-refundMoney
                bank.update({u'name':hostname},{"$set":{u'money':money}})
        web.seeother("/userindex")
         
class beginRefund:
    def POST(self):
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        return render.refund(weibo_id)

        
class payonline:
    def POST(self):
        webinput=web.input()
        weibo_id=webinput[u'weibo_id']
        ac=activities.find_one({u'weibo_id':weibo_id})
        hostname=ac[u'peoplePay'][0]
        hostuid=ac[u'uid']
        ifpay=True
        for people in ac[u'peopleInvited']:
            if people in ac[u'peopleIn']:
                ifpay=True
            else:
                ifpay=False
                break
        cookies=web.cookies()
        acc=cookies[u'access_token']
        exp=cookies[u'expires_in']
        uid=cookies[u'uid']
        client=getClient(acc,exp)
        myname=getClientName(client,int(uid))
        if myname in ac['peoplePay']:
            ifpay=False
            

        if ifpay:
            paymoney=float(ac[u'money'])/len(ac[u'peopleIn'])
            hostacount=bank.find_one({u'name':hostname})
            hostmoney=hostacount[u'money']
            hostmoney+=paymoney
            bank.update({u"name":hostname},{"$set":{u"money":hostmoney}})
            cookies=web.cookies()
            acc=cookies[u'access_token']
            exp=cookies[u'expires_in']
            uid=cookies[u'uid']
            client=getClient(acc,exp)
            myname=getClientName(client,int(uid))
            myacount=bank.find_one({u'name':myname})
            mymoney=myacount[u'money']
            mymoney-=paymoney
            bank.update({u"name":myname},{"$set":{u"money":mymoney}})
            peoplePay=ac[u'peoplePay']
            peoplePay.append(myname)
            activities.update({u"weibo_id":weibo_id},{"$set":{u"peoplePay":peoplePay}})
            string=myname+u"\u652f\u4ed8\u4e86\u6d3b\u52d5"+u":"+ac[u'name']
            user=users.find_one({u'uid':hostuid})
            informations=refreshInformations(user[u'informations'],string)
            users.update({u'uid':hostuid},{"$set":{u'informations':informations}})
        web.SeeOther("/currentActivity")
            

