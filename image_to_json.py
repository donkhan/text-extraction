import boto3
import json
import sys


def get_triplet(block):
    return str(block.get('BlockType')), str(block.get('TextType')), str(block.get('Text'))


def get_block_of_content(blocks, i, text_type, end="?"):
    q = ""
    i = i + 1
    t = get_triplet(blocks[i])
    while t[1] == text_type:
        q = q + t[2] + " "
        if t[2].find(end) != -1:
            break
        i = i + 1
        t = get_triplet(blocks[i])
    return q, i-1


def get_printed_question(blocks, i):
    return get_block_of_content(blocks, i, "PRINTED", "?")


def get_handwritten_answer(blocks, i):
    return get_block_of_content(blocks, i, "HANDWRITING")


def process_text_detection(client, bucket, document):
    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}})
    blocks = response['Blocks']
    i = 0
    data_array = list()
    q_type = "number"

    while i < len(blocks):
        b = get_triplet(blocks[i])
        if b[0] == "WORD" and b[1] == 'PRINTED':
            if b[2] == "-":
                q_no = ""
                q, i = get_printed_question(blocks, i)
                if q.count("-") > 1:
                    continue
                a, i = get_handwritten_answer(blocks, i)
                data_array.append({
                    "question_no": q_no, "question": q, "answer": a
                })
                q_type = "hyper"
                continue

            if q_type == "number" and b[2][0:len(b[2])-1].isdigit():
                q_no = b[2][0:len(b[2])-1]
                q, i = get_printed_question(blocks, i)
                a, i = get_handwritten_answer(blocks, i)
                data_array.append({
                    "question_no": q_no, "question": q, "answer": a
                })
                print(q_no + " " + q + " " + a)
        i = i + 1
    print(str(data_array))
    return str(data_array)


def main():
    session = boto3.Session(profile_name='awskamil')
    client = session.client('textract', region_name='us-east-1')
    process_text_detection(client, 'kamilxbucket', sys.argv[1])


if __name__ == "__main__":
    main()


