import boto3
import boto3, json
import pprint
import urllib.request, json
import csv
from operator import itemgetter

client=boto3.client('ec2',region_name='ap-south-1')
instance_name=[input("Enter the spot instance:")]
instance_name1=instance_name[0]
print(instance_name1)

prices=client.describe_spot_price_history(InstanceTypes=instance_name,MaxResults=5,ProductDescriptions=['Linux/UNIX (Amazon VPC)'])
# mydata = json.dumps(prices.read())
# pprint.pprint(prices['SpotPriceHistory'][:10]) 

dic=prices['SpotPriceHistory']
print(dic)

# az=(dic[1]['AvailabilityZone'])
# spotprice=(dic[1]['SpotPrice'])
# instaname=(dic[1]['InstanceType'])

# print(az)
# print(spotprice)
# print(instaname)

az_to_price_dict={}
with open('price.csv', 'w', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['Instancename','Availabilityzone','Spotprice'])
    for elements in dic:
        instaname=elements['InstanceType']
        az=elements['AvailabilityZone']
        spotprice=elements['SpotPrice']   
        # print({az:spotprice})
        az_to_price_dict[az]=spotprice


        
        
        # print(spotprice)

        # mydic=dict(zip(az,spotprice))
        # print(mydic)

        # thewriter.writerow([instaname,az,spotprice])
print(az_to_price_dict)

lowestprice_az=( min(az_to_price_dict.items(), key=itemgetter(1)))
myaz=lowestprice_az[0]
azprice=lowestprice_az[1]
print(myaz)
print(azprice)
# print(lowprice)

print("Lowest price of spot instance"+ str(instance_name) + ':' + str(myaz) + '=' + str(azprice))


# Creation of spot ec2 instance

client = boto3.client('ec2')
response = client.request_spot_instances(
    DryRun=False,
    SpotPrice=azprice,
    ClientToken='string',
    InstanceCount=1,
    Type='one-time',
    LaunchSpecification={
        'ImageId': 'ami-0e306788ff2473ccb',
        'KeyName': 'spotec2',
        'SecurityGroups': ['mysg'],
        'InstanceType': instance_name1,
        'Placement': {
            'AvailabilityZone': myaz,
        },

        'SecurityGroupIds': [
            'mysg',
        ]
    }
)



