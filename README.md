# text-extraction

This repository is a demonstration of lambda function which uses AWS-textract to extract the text content from images which are present in a known s3 repository and create json responses.

Sample input images are present in input folder and corresponding json output is present in the output folder.

i.e) s1.jpg  is extracted and stored in s1.json and s3.jpg is extracted and stored in s3.json.

This lambda function can be easily extended to listen for s3 bucket create/update/delete notifications, extract the text content and store it in either s3 bucket or transfer to another web service.

The sample jpg files are already stored in s3 bucket named kamilxbucket. Right now it is hardcoded in the code to be read from. 

For Testing you can execute curl -XGET "https://tvzdzzak83.execute-api.us-east-1.amazonaws.com/dev/get-text?file-name=s1.jpg" and see the json output in terse. You can use https://jsonformatter.org/#google_vignette to format the json.  You can note that file-name is a parameter. As of now you can pass either s1.jpg or s3.jpg as input parameter and get different outputs.

Example:
You can see the input image and corresponding text extract.

![alt text](https://github.com/donkhan/text-extraction/blob/main/input/s1.jpg?raw=true)


```json
[
  {
    "question_no": "1",
    "question": "Name: ",
    "answer": "Cindy Rella "
  },
  {
    "question_no": "2",
    "question": "What would you like me to call you? ",
    "answer": "Cinderella "
  },
  {
    "question_no": "3",
    "question": "Phone number: ",
    "answer": "867-5309 "
  },
  {
    "question_no": "4",
    "question": "Address: ",
    "answer": "732 Fairy God Mother drive "
  },
  {
    "question_no": "5",
    "question": "If I can't get you by phone is it ok for me to stop by this address? ",
    "answer": "yes "
  },
  {
    "question_no": "6",
    "question": "Emergency contact person/relationship ",
    "answer": "Gus / pet 123-456-7891 "
  },
  {
    "question_no": "7",
    "question": "Support person contact/relationship and phone number: ",
    "answer": "Fairy - God mother - 1111 472- "
  },
  {
    "question_no": "8",
    "question": "If I am trying to get in touch with you and someone else answers the phone, would it be OK to introduce myself as a ",
    "answer": "Yes "
  }
]
```

