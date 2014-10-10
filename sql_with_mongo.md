design the database for aapay

sqlname:aapay
collections:users
{
    {
    "uid":int//user's uid
    "activities"
    [
        "weibo_id"://huodong id

    ]
    }

    {
    "uid:
    ......
    }
    ......
    
}

collections:activitys:
{
    {
        "uid":int//who begin the activity
        "weibo_id":int  //begin the game through this weibo
        "name"str://activity_name
        "peoples":[str]//who invited to this activity
        "palce":str//where it happens
        "ifend":bool//if it end
        "money":str//the monkey
        "date":str


    }

}
