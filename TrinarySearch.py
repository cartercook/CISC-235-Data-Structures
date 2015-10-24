#By Carter Cook - "I confirm that this submission is my own work and is consistent with the Queen's regulations on Academic Integrity."
#----------IMPORTS AND FUNCTION DECLARATIONS----------#
import random
import time
import csv #for exporting data to a spreadsheet

def bin_search(A,first,last,target):
    # returns index of target in A, if present
    # returns -1 if target is not present in A
    if first > last:
        return -1
    else:
        mid = (first+last)/2
        if A[mid] == target:
            return mid
        elif A[mid] > target:
            return bin_search(A,first,mid-1,target)
        else:
            return bin_search(A,mid+1,last,target)

def trin_search(A,first,last,target):
    # returns index of target in A, if present
    # returns -1 if target is not present in A
    if first > last:
        return -1
    else:
        one_third = first + (last-first)/3
        two_thirds = first + 2*(last-first)/3
        if A[one_third] == target:
            return one_third
        elif A[one_third] > target:
            # search the left-hand third
            return trin_search(A,first,one_third-1,target)
        elif A[two_thirds] == target:
            return two_thirds
        elif A[two_thirds] > target:
            # search the middle third
            return trin_search(A,one_third+1,two_thirds-1,target)
        else:
            # search the right-hand third
            return trin_search(A,two_thirds+1,last,target)

#----------OPEN SPREADSHEET FOR WRITING----------#
myFile = open("TrinarySearchResults.csv", 'wb')
wr = csv.writer(myFile, quoting=csv.QUOTE_ALL)

#----------BEGIN EXPERIMENT----------#
for experiment in [1,2]:
    t_bin = []
    t_trin = []
    sizes = [250,1000,4000,16000,64000] #various list lengths to test.
    search_values = [10,5,2] #values in the list near positions len(list)/10, len(list)/5, etc.
    for sizeIndex in range(len(sizes)):
        size = sizes[sizeIndex]
        
        #create and sort a list of random ints for testing
        testList = random.sample(range(size*10), size) #randomly pick size out of size*10 possibilities
        testList.sort()

        searchVals = []
        if experiment == 1: #experiment 1: search for values in the list
            searchVals.append(testList[0]) #smallest value
            for val in search_values:
                searchVals.append(testList[int(size/val)]) #put a series of values already in testList into searchVals
        else: #experiment 2: search for values absent from the list
            searchVals.append(-1) #furthest value
            for i in range(len(search_values)):
                searchVals.append(int((size*10)/search_values[i])) #put an arbitrary series of in searchVals
                if searchVals[i] in testList:
                    testList.remove(searchVals[i]) #remove any matches from testList

        #list of lists of zeros that will eventually hold time values for each search.
        #e.g:
        #[[0,0,0,0],
        # [0,0,0,0],
        # [0,0,0,0],
        # [0,0,0,0]]
        t_bin.append([0]*len(searchVals))
        t_trin.append([0]*len(searchVals))

        #----------TEST----------#
        for i in range(len(searchVals)):
            for j in range(100):
                t0 = 0.0 #placeholder for initial time before the function is run
                
                #run the search and clock its process time
                t0 = time.clock()
                bin_search(testList, 0, len(testList), searchVals[i])
                t_bin[sizeIndex][i] = t_bin[sizeIndex][i] + float(time.clock()) - t0 #append the difference between inital and current time to t_bin
                
                t0 = time.clock()
                trin_search(testList, 0, len(testList), searchVals[i])
                t_trin[sizeIndex][i] = t_bin[sizeIndex][i] + float(time.clock()) - t0

    #----------WRITE TO CSV AND CLOSE----------#
    wr.writerow(["EXPERIMENT "+str(experiment)])
    wr.writerow(["","BINARY SEARCH:"])
    wr.writerow(["","","SIZE","SIZE/INF","SIZE/10","SIZE/5","SIZE/2"])
    wr.writerow(["","SEARCH VALUES", ""]+searchVals)
    for i in range(len(t_bin)):
        wr.writerow(["","", sizes[i]]+t_bin[i])
    wr.writerows([""]*14)
    wr.writerow(["","TRINARY SEARCH:"])
    wr.writerow(["","","SIZE","SIZE/INF","SIZE/10","SIZE/5","SIZE/2"])
    wr.writerow(["","SEARCH VALUES", ""]+searchVals)
    for i in range(len(t_trin)):
        wr.writerow(["","", sizes[i]]+t_trin[i])
    wr.writerows([""]*14)
myFile.close()
