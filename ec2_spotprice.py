import boto3
import boto3, json
import pprint
import urllib.request, json
import csv
from operator import itemgetter

client=boto3.client('ec2',region_name='ap-south-1')

instance_name=[input("Enter the instance name:")]


prices=client.describe_spot_price_history(InstanceTypes=instance_name,MaxResults=3,ProductDescriptions=['Linux/UNIX (Amazon VPC)'])


dic=prices['SpotPriceHistory']
# print(dic)


az_to_price_dict={}
with open('price.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['Instancename','Availabilityzone','Spotprice','LowestPrice'])
    for elements in dic:
        instaname=elements['InstanceType']
        az=elements['AvailabilityZone']
        
        spotprice=elements['SpotPrice']   
        
        az_to_price_dict[az]=spotprice

        print(az_to_price_dict)

        lowestprice_az=( min(az_to_price_dict.items(), key=itemgetter(1)))

        thewriter.writerow([instaname,az,spotprice,lowestprice_az])
        # print(spotprice)

        

        
    # print(az_to_price_dict)

    # lowestprice_az=( min(az_to_price_dict.items(), key=itemgetter(1)))
    
# # print(lowprice)

print("Lowest price of ec2 spot instance" + str(instance_name) + ':' + str(lowestprice_az))

