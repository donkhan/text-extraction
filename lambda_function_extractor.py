from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities import parameters
import boto3
import io
import json
app = APIGatewayRestResolver()
tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="PowertoolsSample")

@app.get("/get-text")
@tracer.capture_method
def get_text():
    f_name = app.current_event["queryStringParameters"]['file-name']
    metrics.add_metric(name="TextConversionInvocations", unit=MetricUnit.Count, value=1)
    d = process_text_detection(f_name)
    return d

def get_triplet(block):
    return str(block.get('BlockType')), str(block.get('TextType')), str(block.get('Text'))

def get_block_of_content(blocks, i, text_type):
    q = ""
    i = i + 1
    t = get_triplet(blocks[i])
    while t[1] == text_type:
        q = q + t[2] + " "
        i = i + 1
        t = get_triplet(blocks[i])
    return q, i-1

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
            if b[2][0:len(b[2])-1].isdigit():
                q_no = b[2][0:len(b[2])-1]
                q, i = get_printed_question(blocks, i)
                a, i = get_handwritten_answer(blocks, i)
                data_array.append({
                    "question_no" : q_no,"question" : q,"answer" : a })
        i = i + 1
    return data_array

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    logger.info(event)
    return app.resolve(event, context)
