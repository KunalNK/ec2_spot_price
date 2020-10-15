import boto3
import boto3, json
import pprint
import urllib.request, json
import csv
from operator import itemgetter

client=boto3.client('ec2',region_name='ap-south-1')

###################### STEP-1 ###########################################
# Create a function to get the Avaialability zone & Spotprice details

def getaz_spot(instance_name):

    prices=client.describe_spot_price_history(InstanceTypes=instance_name,MaxResults=3,ProductDescriptions=['Linux/UNIX (Amazon VPC)'])

    dic=prices['SpotPriceHistory']
    # print(dic)

    az_spot_data={}
    for elements in dic:
        spot_price=elements['SpotPrice']    #stores the spotprice of instance
        az=elements['AvailabilityZone']     #stores availability zone details
        if not az in az_spot_data.keys():
            az_spot_data[az] = spot_price
    
    # pprint.pprint(prices['SpotPriceHistory'])
    # print(az_spot_data)
    
    return(az_spot_data)

########################## STEP-2 #########################################
# Create a function to get input from user for instance type  

def user_input():
    instance_name=[input("Enter the spot instance:")]
    instance_name1=instance_name[0]
    print(instance_name)
    return instance_name,instance_name1
    
instance_name, instance_name1=user_input()

az_spot_data = getaz_spot(instance_name)
print(az_spot_data)

############################ STEP-3 ########################################
#Create a function to get cheapest az and its price

def get_lowaz_price(az_spot_data):
    lowestprice_az=( min(az_spot_data.items(), key=itemgetter(1)))
    return lowestprice_az

lowest_az, price = get_lowaz_price(az_spot_data)

print("Cheapest AZ:", lowest_az)
print("Lowest price:", price)

##########################  STEP-4 ############################################
# Creation of spot ec2 instance

def create_spot_instance(instance_name, lowest_az):
    response = client.request_spot_instances(
        DryRun=False,
        SpotPrice= price,
        # ClientToken='string1',
        InstanceCount=1,
        Type='one-time',
        LaunchSpecification={
            'ImageId': 'ami-0e306788ff2473ccb',
            'KeyName': 'spotec2',
            'SecurityGroups': ['mysg'],
            'InstanceType': instance_name1,
            'Placement': {
                'AvailabilityZone': lowest_az,
            },
            'SecurityGroupIds': [
                'mysg',
            ]
        }
    )
    # print(response)
    return response

create_spot_instance(instance_name, lowest_az)
#####################################################################
