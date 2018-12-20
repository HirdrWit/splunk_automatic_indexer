import json
import os
import sys 
import fnmatch

sys.dont_write_bytecode = True
info = "configuration/information.json"

def loadJson():
    with open(info) as f:
        data = json.load(f)
    return data

def dataToArray(data):
    myList = []
    for val in data:
        myList.append(val)
    return myList

def dataToArrayRemoveNewLine(data):
    myList = []
    for val in data:
        val = val.replace("\n","")
        val = val.replace("\t","")
        myList.append(val)
    return myList

def checkIfFirstLine(index,file):
    if(index == 0):
        file.write("\n")

def removeDuplicatesFromArray(data):
    newList = []
    for d in data:
        if d not in newList:
            newList.append(d)
    return newList

def createInputsAndPropsDirectory(data):
    index = data['Index']['index']
    dirName = "../../etc/" + index + "/" + index + "_inputs/default"
    try:
        os.makedirs(dirName)
        print("Directory " + dirName +  " :Created ")
    except:
        print("Directory was not created")
    dirName = "../../etc/" + index + "/" + index + "_props/default"
    try:
        os.makedirs(dirName)
        print("Directory " + dirName +  " :Created ")
    except:
        print("Directory was not created")
    
def createAndConfigureInputs(data):
    index = data['Index']['index']
    dirName = "../../etc/" + index + "/" + index + "_inputs/default/inputs.conf"
    sourcetype = dataToArray(data["Index"]["sourcetype"])
    log_location = dataToArray(data["Index"]["log_location"])
    
    file = open(dirName,"w+") 
    for x in range(0,len(sourcetype)):
        checkIfFirstLine(x,file)
        file.write("[monitor://"+log_location[x]["value"]+"]\n")
        file.write("\tblacklist = \. (gz|bz2|z|zip)$\n")
        file.write("\tindex = " + index + "\n")
        file.write("\tsourcetype = "+ sourcetype[x]["value"] + "\n")
        file.write("\n")
        print("Inputs " + str(log_location[x]) +  " :Done ")
    file.close()
    

def createAndConfigureProps(data):
    index = data['Index']['index']
    dirName = "../../etc/" + index + "/" + index + "_props/default/props.conf"
    sourcetype = dataToArray(data["Index"]["sourcetype"])
    sourcetype = removeDuplicatesFromArray(sourcetype)
    file = open(dirName,"w+") 
    for x in range(0,len(sourcetype)):
        checkIfFirstLine(x,file)
        file.write("["+ sourcetype[x]["value"] +"]\n")
        file.write("\tSHOULD_LINEMERGE=true\n")
        file.write("\tNO_BINARY_CHECK=true\n")
        file.write("\tBREAK_ONLY_BEFORE_DATE=true\n")
        file.write("\n")
        print("Props " + str(sourcetype[x]) +  " :Done ")
    file.close()

def whiteListProdServers(data):
    index = data['Index']['index']
    dirName = "../../etc/system/local/serverclass.conf.prod"
    servers = dataToArray(data["Index"]["hosts"]["prod"])
    file = open(dirName,"a") 
    file.write("\n")
    file.write("[serverClass:"+index+"]\n")
    for x in range(0,len(servers)):
        file.write("\twhitelist."+str(x)+" = "+ str(servers[x]["value"]) +"*\n")
    file.write("\t[serverClass:"+index+":app:outputs_prod]\n")   
    file.write("\t[serverClass:"+index+":app:"+index+"_inputs]\n")   
    file.write("\t[serverClass:"+index+":app:"+index+"_props]\n")   
    file.write("\n")  
    print("WhiteList Prod :Done ")
    file.close()

def whiteListDevServers(data):
    index = data['Index']['index']
    dirName = "../../etc/system/local/serverclass.conf.devtest"
    servers = dataToArray(data["Index"]["hosts"]["perf"])
    file = open(dirName,"a") 
    file.write("\n")
    file.write("[serverClass:"+index+"]\n")
    for x in range(0,len(servers)):
        file.write("\twhitelist."+str(x)+" = "+ servers[x]["value"] +"*\n")
    file.write("\t[serverClass:"+index+":app:outputs_devtest]\n")   
    file.write("\t[serverClass:"+index+":app:"+index+"_inputs]\n")   
    file.write("\t[serverClass:"+index+":app:"+index+"_props]\n")   
    file.write("\n")  
    print("WhiteList Perf :Done ") 
    file.close()

def addTo_Indexer_Base_Prod(data):
    index = data['Index']['index']
    dirName = "../../etc/common/indexer_base_prod/default/indexes.conf"
    verify = verifyIndexNotInIndexesConf(index,dirName)
    if(verify):
        file = open(dirName,"a")
        file.write("\n")
        file.write("["+index+"]\n")   
        file.write("\thomePath = $SPLUNK_DB/"+index+"/db\n")   
        file.write("\tcoldPath = $SPLUNK_DB/"+index+"/colddb\n")  
        file.write("\tthawedPath = $SPLUNK_DB/"+index+"/thaweddb\n")    
        file.write("\tfrozenTimePeriodInSecs = 2592000\n")    
        file.write("\t#(30 days)\n") 
        print("Add " + index +  "To Indexer_Base_Prod :Done ")
        file.close()
    else:
        print("Index already in prod indexes.conf")

def addTo_Indexer_Base_Devtest(data):
    index = data['Index']['index']
    dirName = "../../etc/common/indexer_base_devtest/default/indexes.conf"
    verify = verifyIndexNotInIndexesConf(index,dirName)
    if(verify):
        file = open(dirName,"a")
        file.write("\n")
        file.write("["+index+"]\n")   
        file.write("\thomePath = $SPLUNK_DB/"+index+"/db\n")   
        file.write("\tcoldPath = $SPLUNK_DB/"+index+"/colddb\n")  
        file.write("\tthawedPath = $SPLUNK_DB/"+index+"/thaweddb\n")    
        file.write("\tfrozenTimePeriodInSecs = 1209600\n")
        file.write("\t#(14 days)\n") 
        print("Add " + index +  "To Indexer_Base_DevTest :Done ")
        file.close()
    else:
        print("Index already in prod indexes.conf")

def verifyIndexNotInIndexesConf(index, path):
    file = open(path, "r")
    for line in file:
        if(index in line):
            return False
    file.close()
    return True

def addIndexToBuild(data):
    index = " " + data['Index']['index']
    addLine = 100000
    f = open("../../build.sh", "r")
    contents = f.readlines()
    f.close()

    mylist = dataToArrayRemoveNewLine(contents)
    alphaFound = False
    done = False

    for line in range(0,len(mylist)):
        if(alphaFound == True and done == False):
            if(index<mylist[line]):
                addLine = line
                done = True
                print("Add " +  index +  " Build.sh :Done ") 

        elif(alphaFound == False):
            if(mylist[line] == "modules=\""):
                alphaFound = True

    
    contents.insert(addLine, index+"\n")
    f = open("../../build.sh", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()
    if(done == False):
        print("Add " +  index +  " Build.sh :FAILED ")  

def create_sh_File(data):
    index = data['Index']['index']
    dirName = "../../"+index+".sh"
    file = open(dirName,"w+") 
    file.write(index+"_sh_common=\"" + index + "_props\"")
    print("Create " + index + ".sh :Done ")
    file.close()

def addToInputs(data):
    index = data['Index']['index']
    dirName = data['Index']['existing_inputs']
    sourcetype = dataToArray(data["Index"]["sourcetype"])
    log_location = dataToArray(data["Index"]["log_location"])
    
    file = open(dirName,"a") 
    for x in range(0,len(sourcetype)):
        checkIfFirstLine(x,file)
        file.write("[monitor://"+log_location[x]["value"]+"*]\n")
        file.write("\tblacklist = \. (gz|bz2|z|zip)$\n")
        file.write("\tindex = " + index + "\n")
        file.write("\tsourcetype = "+ sourcetype[x]["value"] + "\n")
        file.write("\n")
        print("Inputs " + str(log_location[x]) +  " :Done ")
    file.close()

def addToProps(data):
    index = data['Index']['index']
    dirName = data['Index']['existing_props']
    
    sourcetype = dataToArray(data["Index"]["sourcetype"])
    sourcetype = removeDuplicatesFromArray(sourcetype)
    file = open(dirName,"a") 
    for x in range(0,len(sourcetype)):
        checkIfFirstLine(x,file)
        file.write("["+ sourcetype[x]["value"] +"]\n")
        file.write("\tSHOULD_LINEMERGE=true\n")
        file.write("\tNO_BINARY_CHECK=true\n")
        file.write("\tBREAK_ONLY_BEFORE_DATE=true\n")
        file.write("\n")
        print("Props " + str(sourcetype[x]) +  " :Done ")
    file.close()

def addToExistingWhiteList(data,env):#needs work
    index = data['Index']['index']
    index = "[serverClass:" + index +"]"
    dirName = "../../etc/system/local/serverclass.conf."+env
    env = devenv(env)
    servers = dataToArray(data["Index"]["hosts"][env])
    
    f = open(dirName, "r")
    contents = f.readlines()
    f.close()

    mylist = dataToArrayRemoveNewLine(contents)
    indexFound = False
    done = False
    addLine = 100000
    count = 0

    for line in range(0,len(mylist)):
        if(indexFound == True and done == False):
            if("whitelist." in mylist[line][:10]): 
                count+=1
                
            else:
                addLine = line
                done = True

        elif(indexFound == False):
            if(index in mylist[line]):
                indexFound = True

    f = open(dirName, "w+")
    for server in servers:
        # text = input("\twhitelist."+str(count)+" = "+server['value']+"*\n")
        contents.insert(addLine, "test")
        contents = "".join(contents)
        f.write(contents)
        count+=1
    f.close()
    print("Added " +  env +  " whitelist")  



def addIndexToBuild(data):
    index = " " + data['Index']['index']
    addLine = 100000
    f = open("../../build.sh", "r")
    contents = f.readlines()
    f.close()

    mylist = dataToArrayRemoveNewLine(contents)
    alphaFound = False
    done = False

    for line in range(0,len(mylist)):
        if(alphaFound == True and done == False):
            if(index<mylist[line]):
                addLine = line
                done = True
                print("Add " +  index +  " Build.sh :Done ") 

        elif(alphaFound == False):
            if(mylist[line] == "modules=\""):
                alphaFound = True

    
    contents.insert(addLine, index+"\n")
    f = open("../../build.sh", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()
    if(done == False):
        print("Add " +  index +  " Build.sh :FAILED ")  





def devenv(env):
    if env == "devtest":
        return "perf"
    else:
        return env