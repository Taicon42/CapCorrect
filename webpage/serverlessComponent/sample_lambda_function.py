import json

def lambda_handler(event, context):
    # TODO implement
    
    
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': ''
    }
    
    
    
    detected_errors = [
        
        {'id': '1', 'timestamp':'00:00:00 - 00:04:20', 'err_text': 'So this is just an example of some text to show...',
             'sugguestions': 'adfweQ[EQpd', 'has_error': True
        },
        {'id': '2', 'timestamp':'00:06:50 - 00:07:20', 'err_text': 'AND YET ANOTHER EXMAMPWE',
             'sugguestions': 'hqerqerhqgrax', 'has_error': True
        },
        {'id': '3', 'timestamp':'00:08:00 - 00:09:20', 'err_text': 'WEEEEEEEEE',
             'sugguestions': 'eq2grwefe', 'has_error': True
        },
        {'id': '4', 'timestamp':'00:13:20 - 00:14:03 ', 'err_text': 'Nothing, this is a fine sentence.',
             'sugguestions': '', 'has_error': False
        }
    ]
    
    # response['body'] = json.dumps(event.get('fileText'))

    response['body'] = json.dumps(detected_errors)
    
    return response