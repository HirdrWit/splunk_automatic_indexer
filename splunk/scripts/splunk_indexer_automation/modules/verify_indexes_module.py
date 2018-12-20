import sys 
sys.dont_write_bytecode = True
def test():
    print("hello")
    
def run(env):
    #get path
    path = getPath(env)
    #load environment, read file
    lines = readFile(path)
    #verify file
    verifyIndexes(lines,env)
    
def getPath(env):
    if(env == "perf"):
        return "splunk/etc/common/indexer_base_devtest/default/indexes.conf"
    elif(env == "prod"):
        return "splunk/etc/common/indexer_base_prod/default/indexes.conf"
    else:
        print("ERROR : ENV variable passed wrong")
        return ""

def readFile(path):
    f = open(path, "r")
    contents = f.readlines()
    f.close()
    return contents

def verifyIndexes(lines,env):
    if(env == "perf"):
        verifyPerf(lines)
    # else:
    #     verifyProd(lines)

def verifyPerf(lines):
    start = False
    newIndex = False
    homepath = True
    coldpath = True
    thawedpath = True
    emptyLine = ""
    index = ""

    for line in lines:
        if("#---------- End Splunk Internal Indexes ----------" in line):
            start = True
        if(start):
            if(line == emptyLine):
                break
            elif("[" in line):
                print(homepath)
                if(homepath == True and coldpath == True and thawedpath == True):
                    print("ok")
                else:
                    print("ERROR: " + index)
                index = cleanIndex(line)
                newIndex = True
                homepath = False
                coldpath = False
                thawedpath = False
            elif(newIndex):
                print(line)
                if("homePath" in line):
                    homepath = True
                if("coldPath" in line):
                    coldpath = True  
                if("thawedPath" in line):
                    thawedpath = True  


                
def cleanIndex(index):
    temp = index.replace(']','')
    index = temp.replace('[','')
    return index             