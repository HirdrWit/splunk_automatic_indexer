#Creator: Rob Hird
#Date: Nov 2018
#Description: Automate adding indexes
#How to run: 
#  1. Must run from : /splunk/splunk_indexer_automation
#  2. Updated /splunk/splunk_indexer_automation/configuration/information.json with  
#  3. (Best to run from python3.) If you have multiple python instances, run --> python3 add_index.py
from modules import addIndexModule 
import json
import sys 
sys.dont_write_bytecode = True
def addNewIndex(data):
    addIndexModule.createInputsAndPropsDirectory(data)
    addIndexModule.createAndConfigureInputs(data)
    addIndexModule.createAndConfigureProps(data)
    addIndexModule.whiteListProdServers(data)
    addIndexModule.whiteListDevServers(data)
    addIndexModule.addTo_Indexer_Base_Devtest(data)
    addIndexModule.addTo_Indexer_Base_Prod(data)
    addIndexModule.addIndexToBuild(data)
    addIndexModule.create_sh_File(data)

def addToExistingIndex(data): #Needs work
    addIndexModule.addToInputs(data)
    addIndexModule.addToProps(data)
    addIndexModule.addToExistingWhiteList(data,"prod")
    addIndexModule.addToExistingWhiteList(data,"devtest")

def main():
    data = addIndexModule.loadJson()
    if(data['Index']['Type'] == 'New'):
        addNewIndex(data)
    elif(data['Index']['Type'] == 'Add'): 
        addToExistingIndex(data)   
    else:
        print("Incorrect Index Type")

if __name__ == '__main__':
    main()