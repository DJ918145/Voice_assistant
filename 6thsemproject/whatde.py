import pywhatkit as kit
# Whatsapp msg decoder for sending message via whatsapp.
def wd(org):
    real = "jarvis send a message to that at am pm"
    reals = real.split()
    orgs = org.split()
    a=1
    time = ""
    for i in range(len(orgs)):
        if orgs[i]=='to':
            user = orgs[i+1]
            while a!=10:
                if orgs[i+1+a]!="that":
                    user = user +" "+ orgs[i+1+a]
                    a = a+1
                else:
                    a = 10
        if orgs[i]=="that":
            msg = orgs[i+1]
            a=1
            while a!=100:
                if orgs[i+1+a]!="at":
                        msg = msg +" "+ orgs[i+1+a]
                        a = a+1
                else:
                    if orgs[i+2+a][0].isnumeric():
                        a = 100
                    else:
                        msg = msg +" "+ orgs[i+1+a]
                        a = a+1
        if orgs[i][0].isnumeric():
            while i!=len(orgs):
                time = time + " " + orgs[i]
                i = i+1 
        
    return user, msg, time

def what(text):
    contact={
        "didi" : "+919664993441",
        "mama" : "+919313429989",
        "papa" : "+919974128265",
        "tisha" : "+917862881855",
        "dhruv" : "+917984918145"
    }
    # original = "jarvis send a message to didi that i am arrived at colloge at 15:10"
    user , msg, time = wd(text) 
    pop = contact.keys()
    num = ""
    for i in pop:
        if i == user:
            num = contact[user]
            break
    print(num)
    hh = time[1]+time[2]
    if time[4]!='0':
        mm = time[4]+time[5]
    else:
        mm = time[5]
    mm = int(mm)
    hh = int(hh)

    # Send a WhatsApp message
    kit.sendwhatmsg(num, msg , hh, mm)

if __name__ == "__main__":
    what()
