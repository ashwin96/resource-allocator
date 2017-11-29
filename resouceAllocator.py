# creating a dictionary with the processor count for each server type
cpuCount{
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
		return allocateCPU(instances,hours,price)
	elif price == -1:
		return allocateCPU(instances,hours,cpus)
	else
		return allocateCPU(instances,hours,cpus,price)



