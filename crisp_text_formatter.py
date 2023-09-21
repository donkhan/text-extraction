#Detects text in a document stored in an S3 bucket. Display polygon box around text and angled text 
import boto3
import io
from PIL import Image, ImageDraw


def process_text_detection(s3_connection, client, bucket, document):
    s3_object = s3_connection.Object(bucket,document)
    s3_response = s3_object.get()
    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}})

    blocks=response['Blocks']
    print ('Detected Document Text')
   
    for block in blocks:
            print('Type: ' + block['BlockType'])
            if block['BlockType'] != 'PAGE':
                print('Detected: ' + block['Text'])
    return len(blocks)


def main():
    session = boto3.Session(profile_name='awskamil')
    s3_connection = session.resource('s3')
    client = session.client('textract', region_name='us-east-1')
    bucket = 'kamilxbucket'
    document = 'i1.jpeg'
    block_count=process_text_detection(s3_connection,client,bucket,document)
    print("Blocks detected: " + str(block_count))


if __name__ == "__main__":
    main()


