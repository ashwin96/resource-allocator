import sys
# creating a dictionary with the processor count for each server type
cpuCount={
	'large'  :1,
	'xlarge' :2,
	'2xlarge':4,
	'4xlarge':8,
	'8xlarge':16,
	'10xlarge':32
}
maxDiff = sys.maxsize
# Assuming the non-specified information in case of CPU count or 
# price ( case 1 and 2 ) is represented as -1
def get_costs(instances,hours,cpus,price):
	if cpus == -1:
		return allocateCPU(instances,hours,cpus,price,0)
	elif price == -1:
		return allocateCPU(instances,hours,cpus,price,1)
	else:
		return allocateCPU(instances,hours,cpus,price,2)
# Representing three cases of the problem as states
def allocateCPU(instances,hours,cpus,price,state):
	result = []
	for instance in instances:
		instanceSet = sorted(instances[instance],key=instances[instance].get,reverse=True);
		finalList = []
		global maxDiff
		maxDiff = sys.maxsize
		if validParams(hours,cpus,price):
			CostCalculator(instances[instance],instanceSet,hours,cpus,price,[],finalList,0,state)
		server_list,total_cost = getListData(instances[instance],finalList,hours);
		instanceDict = {
			"region":instance,
			"total_cost":str("$"+str(round(total_cost,2))),
			"servers": server_list
		}
		result.append(instanceDict)
	result.sort(key=lambda x:x['total_cost'])
	return result
# case 1 : Getting the first combination which sums to the CPU count. Since the list is sorted in descending order we get the first combination as optimal allocation
# case 2 : For maximum allocation for a given price without a CPU count, we find the combination which sum close to the given amount
# case 3 : With both CPU count and maximum budget mentioned we combine the strategy for the first two cases and if the allocation is not possible within the amount, we return a empty server list 
def CostCalculator(instance,instanceSet,hours,cpus,price,li,finalList,start,state):
	if state == 1:
		if cpus == 0:
			if len(finalList)==0:
				finalList.append(li[:])
			return
		if cpus < 0:
			return
	elif state == 0:
		if price >= 0:
			global maxDiff
			if maxDiff > price - 0: #checking if the previous difference greater than the current
				if len(finalList)>0:
					finalList.pop()
				maxDiff = price - 0 
				finalList.append(li[:])
		if price < 0:
			return
	else:
		if cpus == 0 and price >= 0:
			if len(finalList)==0:
				finalList.append(li[:])
				myNewList = [] # Assigning servers for the remaining amount after allocating the minimum CPUs
				CostCalculator(instance,instanceSet,hours,cpus,price,[],myNewList,0,0)
				for i in myNewList:
					finalList.append(i)
		if cpus < 0 or price < 0:
			return 
	for i in range(start,len(instance)):
		if len(finalList)>0 and state != 0:
			break;
		li.append(instanceSet[i])
		if state == 0:
			CostCalculator(instance,instanceSet,hours,cpus,price-hours*instance.get(instanceSet[i]),li,finalList,i,state)
		elif state == 1:
			CostCalculator(instance,instanceSet,hours,cpus-cpuCount.get(instanceSet[i]),price,li,finalList,i,state)
		else:
			CostCalculator(instance,instanceSet,hours,cpus-cpuCount.get(instanceSet[i]),price-hours*instance.get(instanceSet[i]),li,finalList,i,state)
		li.pop()

def validParams(hours,cpus,price):
	return hours > 0 and cpus != 0 and cpus >= -1 and price >= -1 and price != 0

def getListData(instance,finalList,hours):
	ServerDict = {}
	serverList = []
	total_cost = 0;
	for mylist in finalList:
		for element in mylist:
			if element in ServerDict:
				ServerDict[element] += 1
			else:
				ServerDict[element] = 1
			total_cost += instance.get(element)
	for key,value in ServerDict.items():
		serverList.append(tuple([key,value]))
	return serverList,total_cost*hours







