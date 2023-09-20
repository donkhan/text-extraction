import boto3
import json
import sys


def get_triplet(block):
    return str(block.get('BlockType')), str(block.get('TextType')), str(block.get('Text'))


def get_block_of_content(blocks, i, text_type):
    content = ""
    i = i + 1
    t = get_triplet(blocks[i])
    while t[1] == text_type:
        content = content + t[2] + " "
        i = i + 1
        t = get_triplet(blocks[i])
    return content, i-1


def get_block_answer(blocks):
    i = 0
    s = ""
    while i < len(blocks):
        t = get_triplet(blocks[i])
        if t[1] == "HANDWRITING":
            s = s + " " + t[2]
        i = i + 1
    return s


def get_printed_question(blocks, i):
    return get_block_of_content(blocks, i, "PRINTED")


def get_handwritten_answer(blocks, i):
    return get_block_of_content(blocks, i, "HANDWRITING")


def process_text_detection(f_name):
    blocks = boto3.client('textract', region_name='us-east-1').detect_document_text(
        Document={'S3Object': {'Bucket': "kamilxbucket", 'Name': f_name}})['Blocks']
    i = 0
    data_array = list()
    while i < len(blocks):
        b = get_triplet(blocks[i])
        if b[0] == "WORD" and b[1] == 'PRINTED':
            if b[2] == "-":
                q_no = ""
                q, i = get_printed_question(blocks, i)
                a, i = get_handwritten_answer(blocks, i)
                data_array.append({
                    "question_no": q_no, "question": q, "answer": a
                })
                continue

            if b[2][0:len(b[2])-1].isdigit():
                q_no = b[2][0:len(b[2])-1]
                q, i = get_printed_question(blocks, i)
                a, i = get_handwritten_answer(blocks, i)
                data_array.append({
                    "question_no": q_no, "question": q, "answer": a
                })

        i = i + 1
    print(str(data_array))
    return str(data_array)


def main():
    process_text_detection(sys.argv[1])


if __name__ == "__main__":
    main()


