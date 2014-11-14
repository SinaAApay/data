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
class setFillMoney:
    def POST(self):
        webinput=web.input()
        fillMoney=webinput[u'fillMoney']
        weibo_id=webinput[u'weibo_id']
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
        hostname=''
        for people in peopleInvited:
            if count==0:
                count+=1
                hostname=people
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
        ifpay=True
        for people in ac[u'peopleInvited']:
            if people in ac[u'peopleIn']:
                ifpay=True
            else:
                ifpay=False
                break
        if ifpay:
            paymoney=float(ac[u'money'])/len(ac[u'peopleIn'])
            print paymoney
            print len(ac[u'peopleIn'])
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
        web.SeeOther("/currentActivity")
            

