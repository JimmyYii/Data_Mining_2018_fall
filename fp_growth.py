#FP_growth

import time
#variables:
#name of the node, a count
#nodelink used to link similar items
#parent vaiable used to refer to the parent of the node in the tree
#node contains an empty dictionary for the children in the node
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      #needs to be updated
        self.children = {} 
#increase the count variable with a given amount    
    def inc(self, numOccur):
        self.count += numOccur
#display tree in text. Useful for debugging        
    def disp(self, ind=1):
        print ('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)

# Pre-process of data
def load_process():
    import numpy as np
    data = np.loadtxt("ntrans_10000_nitems_30_tlen_20.txt", dtype='int') #Change filename here for different datasets

    all_dat = []
    tran_dat = []
    temp = 1  # Initial
    for trans in data:
        if not trans[0] == temp:
            all_dat.append(tran_dat)
            tran_dat = []
        tran_dat.append(trans[2])
        temp = trans[0]
    all_dat.append(tran_dat)  # Final set of data
    #print(all_dat)
    return all_dat,len(all_dat)

def loadSimpDat():
    simpDat = [['a','b','c'], #Example from PDF
               ['b','d'],
               ['b','e'],
               ['a','b','d'],
               ['a','e'],
               ['b','e'],
               ['a','e'],
               ['a','b','e','c'],
               ['a','b','e']]
    return simpDat,len(simpDat)

def createInitSet(dataSet): #ASK
    retDict = {} #Form for createTree()
    for trans in dataSet:
        if not frozenset(trans) in retDict:
            retDict[frozenset(trans)] = 1 #The double transaction will be missing!!        
        else:
            retDict[frozenset(trans)] += 1
    #print(retDict)
    return retDict

def createTree(dataSet, minSup): #create FP-tree from dataset but don't mine
    headerTable = {}
    #go over dataSet twice
    for trans in dataSet: #first pass counts frequency of occurance
        for item in trans:
        	headerTable[item] = headerTable.get(item, 0) + dataSet[trans] #dataSet[trans] = 1
        	# If 1st found -> 'a': 1, if found again -> value + 1
    for k in list(headerTable):  #remove items not meeting minSup
        if headerTable[k] < minSup:	#dict[] -> take the value of key
        	del(headerTable[k])
    freqItemSet = set(headerTable.keys()) #make it { , , , }
    #print('freqItemSet: ',freqItemSet)
    if len(freqItemSet) == 0: return None, None  #if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link
    #print('headerTable: ',headerTable)
    retTree = treeNode('Null Set', 1, None) #create tree
    #print(dataSet.items())
    for tranSet, count in dataSet.items():  #go through dataset 2nd time
        localD = {}
        for item in tranSet:  #put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
                # print(localD)
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            #print(orderedItems,count)
            updateTree(orderedItems, retTree, headerTable, count)#populate tree with ordered freq itemset
    return retTree, headerTable #return tree and header table

def updateTree(items, inTree, headerTable, count): # ASK!
    #print(items)
    # inTree.disp()
    if items[0] in inTree.children:#check if orderedItems[0] in retTree.children
    	inTree.children[items[0]].inc(count) #increase count
    else:   #add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: #update header table 
            #print('111')
            # print(headerTable[items[0]][1])
            headerTable[items[0]][1] = inTree.children[items[0]]
            #print(headerTable[items[0]][1])
        else:
            #print('222')
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]]) #what this do?
    # inTree.disp()
    #print(items)
    if len(items) > 1: #call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count) #items[1::]?ASK

# ASK!
def updateHeader(nodeToTest, targetNode):   #this version does not use recursion
    while (nodeToTest.nodeLink != None):    #Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode): #treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def showPath(myHeaderTab):
    sort_item = sorted(myHeaderTab.items(), key=lambda x: x[1][0],reverse=True)
    del sort_item[0]
    # print(sort_item)
    for item in sort_item:
        item_path={}
        item_path = findPrefixPath(item[0], myHeaderTab[item[0]][1])
        # print(item[0],'--->',item_path)
        # for path in item_path.items():
        #     print(path[0],path[1])

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    """mineTree(To construct conditional FP-growth)
    Args:
        inTree       myFPtree
        headerTable  {All element +(value, treeNode)} that satisfy minSup 
        minSup       
        preFix       Previous record of newFreqSet，will not update without myHead
        freqItemList
    """
    # Sort by value to get keys of frequent itemsets
    # list collection of keys of minimum support
    # print(headerTable)
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]
    # print('-----', sorted(headerTable.items(), key=lambda p: p[1][0]))
    # print('bigL=', bigL)
    # Key of Mmst frequent itemsets. Find correspinding frequent itemsets ascendingly
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        # print('newFreqSet=', newFreqSet, preFix)

        freqItemList.append(newFreqSet)
        # print('freqItemList=', freqItemList)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        # print('condPattBases=', basePat, condPattBases)

        # Construct FP-tree
        myCondTree, myHead = createTree(condPattBases, minSup)
        # print('myHead=', myHead)
        # Mine conditional FP-tree, if myHead not empty -> satisfy minSup {所有的元素+(value, treeNode)}
        if myHead is not None:
            # myCondTree.disp(1)
            # print('\n\n\n')
            # Pass myHead to find frequent itemset
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
        # print('\n\n\n')
#--------------------------------------------------------

# rootNode = treeNode('pyramid',9,None)
# rootNode.children['eye'] = treeNode('eye',13,None)
# rootNode.disp()

minSup = 0.6
tranData, numTran = load_process()
# tranData, numTran = loadSimpDat()
minSup_mul = minSup*numTran
# minSup_mul = 2
# print(minSup_mul)
# print('Dataset:\n',tranData)
print('------------------------------------------------------')
initSet = createInitSet(tranData)
# print(initSet)

start_time = time.time()
#The FP-tree
myFPtree, myHeaderTab = createTree(initSet, minSup_mul)
#myFPtree.disp()
# showPath(myHeaderTab)
freqItemList = []
mineTree(myFPtree, myHeaderTab, minSup_mul, set([]), freqItemList)
end_time = time.time()
print('By FP-Growth:\nFrequent itemsets:\n',freqItemList,'\nNumber of frequent itemsets =', len(freqItemList))
print('Elapsed time: ',end_time - start_time,'s\n')