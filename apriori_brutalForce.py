# Data Mining, Project_1, N16064103, Jimmy Liu

# Pre-process of data
import time
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

    # all_dat = [['a','b','c'], #Example from PDF
    #            ['b','d'],
    #            ['b','e'],
    #            ['a','b','d'],
    #            ['a','e'],
    #            ['b','e'],
    #            ['a','e'],
    #            ['a','b','e','c'],
    #            ['a','b','e']]
    return all_dat, len(all_dat)

# Brutal force
def BF_gen_next_lv(Lk, k):
    # print('there')
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            # print(i,lenLk)
            if not (Lk[i] | Lk[j]) in retList and len(Lk[i] | Lk[j]) == k: #Avoid double & over length
                retList.append(Lk[i] | Lk[j])
    # print('here')
    return retList

def brutal_force(dataSet, minSupport):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))
    L = [C1]
    k = 2
    while(len(L[k - 2]) > 0):
        Ck = BF_gen_next_lv(L[k - 2], k)
        L.append(Ck)
        k += 1
    # Scan database
    ssCnt = {}
    for tid in D:
    	for i in range(len(L)-2):
    		for can in L[i]:
    			if can.issubset(tid):
    				if not can in ssCnt: ssCnt[can]=1	# Count
    				else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)	#Insert into list
        supportData[key] = support
    return retList, supportData

# Apriori Algorithm
#   Concept
#       Create a list of candidate itemsets of length k
#       Scan the dataset to see if each itemset is frequent
#       Keep frequent itemsets to create itemsets of length k+1"""

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:    # if C1 not yet has [item] 
                C1.append([item])   # Add [item] to C1
                
    C1.sort()   # [1,2,3,4,5]
    return list(map(frozenset, C1)) # use frozen set so we can use it as a key in a dict

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:   # [{1,3,4},{2,3,5},...]
        for can in Ck:  # [1,2,...]
            if can.issubset(tid):
                if not can in ssCnt: ssCnt[can]=1   # Count
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)   #Insert into list
            supportData[key] = support #Show only those > minSupport
        #supportData[key] = support    #Show all
    return retList, supportData

def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk) # L = [5,2,3,1], len(L) = 4
    for i in range(lenLk):  #0~4
        for j in range(i+1, lenLk): # 1~4 2~4 3~4 4
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]  # 0th element = [], 1 -> 2 all the same
            # print(Lk[i],Lk[j])
            # print(i,j,L1,L2)
            L1.sort(); L2.sort()    # Must do!
            if L1==L2:  # if first k-2 elements are equal!
                retList.append(Lk[i] | Lk[j]) #set union
                # print(retList)
    return retList

def apriori(dataSet, minSupport):
    C1 = createC1(dataSet)  #e.g. [1,2,3,4,5]
    D = list(map(set, dataSet)) # [{1, 3, 4}, {2, 3, 5}, {1, 2, 3, 5}, {2, 5}] Make it in setform
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]    # L1 = [5,2,3,1]
    k = 2
    while (len(L[k-2]) > 0):    # 4 > 0
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport) #scan DB to get Lk, L2 = [{2,3},{3,5},{2,5},{1,3}]
        supportData.update(supK)
        L.append(Lk)
        k += 1  # Check L2
    return L, supportData

# Fail...
# FP-Growth
# def FPG(dataSet, minSupport=0.5):
# 	C1 = createC1(dataSet)
# 	D = list(map(set, dataSet))
# 	L1, supportData = scanD(D, C1, minSupport)
# 	#Get descending item
# 	supportData_sorted = sorted(supportData.items(), key=lambda x: x[1],reverse=True)
# 	for itm in supportData_sorted:
# 		for tran in D:

# 	return L1, sup_dat_sorted
#------------------------------------------------------------------------------------
start_time = time.time()
tranData, numTran = load_process()
end_time = time.time()
# print('Dataset:\n',tranData,'\n')
# print('Elapsed time: ',end_time - start_time,'s\n')
print('------------------------------------------------------')
minSup = 0.6
# print(minSup)
# start_time = time.time()
# freqItemSet_BF,supportData_BF = brutal_force(tranData,minSup)
# end_time = time.time()
# print('By Brutal force:\nFrequent itemsets:\n',freqItemSet_BF,'\nNumber of frequent itemsets =',len(freqItemSet_BF))
# print('Elapsed time: ',end_time - start_time,'s\n')
# print('------------------------------------------------------')
start_time = time.time()
freqItemSet_AP,supportData_AP = apriori(tranData,minSup)
end_time = time.time()
# For counting frequent itemsets from Apriori
length_fqItem = 0
for itemset in freqItemSet_AP:
    for item in itemset:
        length_fqItem += 1

print('By Apriori algorithm:\nFrequent itemsets:\n',freqItemSet_AP,'\nNumber of frequent itemsets =',length_fqItem)
print('Elapsed time: ',end_time - start_time,'s\n')
# a,b = FPG(yoyo)
# print(b)