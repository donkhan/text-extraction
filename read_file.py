import boto3

def read_file_from_s3(bucket_name, file_name):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    print(obj)
    data = obj['Body'].read().decode('utf-8','ignore')
    return data


data = read_file_from_s3("kamilimagebucket","i1.jpeg")

#print(len(data))
