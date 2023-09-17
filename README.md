# text-extraction

This repository is a demonstration of lambda function which uses AWS-textract to extract the text content from images which are present in a known s3 repository and create json responses.

Sample input images are present in input folder and corresponding json output is present in the output folder

i.e) s1.jpg  is extracted and stored in s1.json and s3.jpg is extracted and stored in s3.json

This lambda function can be easily extended to listen for s3 bucket created/update/delete notifications, extract the text content and store it in either s3 bucket or to another web service.

The sample jpg files are already stored in s3 bucket named kamilxbucket. Right now it is hardcoded in the code to be read from. 

For Testing you can execute curl -XGET "https://tvzdzzak83.execute-api.us-east-1.amazonaws.com/dev/get-text?file-name=s1.jpg" and see the json output in terse. You can use https://jsonformatter.org/#google_vignette to format the json.  You can note that file-name is a parameter. As of now you can pass either s1.jpg or s3.jpg and input parameter and get different outputs.

