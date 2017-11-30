# creating a dictionary with the processor count for each server type
cpuCount={
	'large'  :1,
	'xlarge' :2,
	'2xlarge':4,
	'4xlarge':8,
	'8xlarge':16,
	'10xlarge':32
}
# Assuming the non-specified information in case of CPU count or 
# price ( case 1 and 2 ) is represented as -1
def get_costs(instances,hours,cpus,price):
	if cpus == -1:
		return allocateCPU(instances,hours,cpus,price,0)
	elif price == -1:
		return allocateCPU(instances,hours,cpus,price,1)
	else:
		return allocateCPU(instances,hours,cpus,price,2)

def allocateCPU(instances,hours,cpus,price,state):
	result = []
	for instance in instances:
		instanceSet = sorted(instances[instance],key=instances[instance].get,reverse=True);
		finalList = []
		CostCalculator(instances[instance],instanceSet,hours,cpus,price,[],finalList,0,state)
		server_list,total_cost = getListData(instances[instance],finalList,hours);
		instanceDict = {
			"region":instance,
			"total_cost":str("$"+str(total_cost)),
			"servers": server_list
		}
		result.append(instanceDict)
	result.sort(key=lambda x:x['total_cost'])
	return result

def CostCalculator(instance,instanceSet,hours,cpus,price,li,finalList,start,state):
	if state in [0,1]:
		variable =  price if state == 0 else cpus
		if variable == 0:
			if len(finalList)==0:
				finalList.append(li[:])
			return
		if variable < 0:
			return
	else:
		if cpus == 0 and price >= 0:
			if len(finalList)==0:
				finalList.append(li[:])
		if cpus < 0 or price < 0:
			return 
	for i in range(start,len(instance)):
		if len(finalList)>0:
			break;
		li.append(instanceSet[i])
		if state == 0:
			CostCalculator(instance,instanceSet,hours,cpus,price-hours*instance.get(instanceSet[i]),li,finalList,i,state)
		elif state == 1:
			CostCalculator(instance,instanceSet,hours,cpus-cpuCount.get(instanceSet[i]),price,li,finalList,i,state)
		else:
			CostCalculator(instance,instanceSet,hours,cpus-cpuCount.get(instanceSet[i]),price-hours*instance.get(instanceSet[i]),li,finalList,i,state)
		li.pop()

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







