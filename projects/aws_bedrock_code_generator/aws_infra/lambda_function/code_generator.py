import boto3
import botocore.config
import json
from datetime import datetime


def generate_code(message:str,language:str) ->str:

    prompt_text = f"""Human: Act as a programmer/developer and write {language} code for the following instructions: {message}.
    Assistant:
    """
    body = {
        "inputText": prompt_text,
        "textGenerationConfig": {
            "maxTokenCount": 2048,
            "temperature": 0.1,
            "topP": 0.9,
            "stopSequences": []
        }
    }

    try:
        bedrock = boto3.client("bedrock-runtime",region_name="us-east-1",config = botocore.config.Config(read_timeout=300, retries = {'max_attempts':3}))
        response = bedrock.invoke_model(body=json.dumps(body), modelId="amazon.titan-text-premier-v1:0", contentType="application/json", accept="application/json")
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.loads(response_content)
        code = response_data["results"][0]["outputText"].strip()
        return code

    except Exception as e:
        print(f"Error generating the code: {e}")
        return ""

def save_code_to_s3_bucket(code, s3_bucket, s3_key):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = code)
        print("Code saved to s3")
    except Exception as e:
        print("Error when saving the code to s3")

def lambda_handler(event, context):
    # Handle API Gateway events (with 'body') and direct invokes (no 'body')
    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    message = body.get("message", "")
    language = body.get("language", "python")

    print(message, language)
    generated_code = generate_code(message, language)

    if generated_code:
        current_time = datetime.now().strftime("%H%M%S")
        s3_key = f"code-output/{current_time}.py"
        s3_bucket = "code-generator-aws-bedrock"
        save_code_to_s3_bucket(generated_code, s3_bucket, s3_key)
    else:
        print("No code was generated")

    return {
        "statusCode": 200,
        "body": json.dumps("Code generation Complete")
    }
