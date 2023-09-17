# text-extraction

This repository is a demonstration of lambda function which AWS-textract to extract the images which is present in a known s3 repository.

Sample input images are present in input folder and corresponding json output is present in the output folder

i.e) s1.jpg  is extracted and stored in s1.json and s3.jpg is extracted and stored in s3.json

This lambda function can be easily extended to listen for s3 bucket created/update/delete notifications, extract the text content and store it in either s3 bucket or to another web service.
