import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    
    
    try:
        
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        object = s3.get_object(Bucket=bucket, Key=key)
        print('object')
        print(object)
        
        content = object['Body'].read().decode("utf-8")
        print('content')
        print(content)
        content = content.split("\n")
        print('contentsplit')
        print(content)
        print('parse')
        content = parse_content(content)
        print('total')
        total_id = sum_id(content)
        
        return total_id 
   
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

def parse_content(content):
    print('!!!!!')
    for i in content:
        print (i.split(";")[0], i.split(";")[1], i.split(";")[2], i.split(";")[3])
        print (i.split(";")[0])
    return  [{"id":i.split(";")[0], "email":i.split(";")[1], "name":i.split(";")[2], "surname":i.split(";")[3]} for i in content] #{"id":i.split(";")[0], "email":i.split(";")[1], "name":i.split(";")[2], "surname":i.split(";")[3]}
    
def sum_id(items):
    sum = 0
    for i in items:
          sum = sum + int(i["id"])
    print('sum')
    print(sum)
    return sum
    
def upload_data(bucket, filename, content):
    binary_data = str.encode(str(content))
    s3.put_object(Body=binary_data, Bucket=bucket, Key=filename)


