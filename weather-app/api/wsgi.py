# api/wsgi.py
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

def wsgi_handler(app, event, context):
    from werkzeug.wrappers import Request, Response
    from io import BytesIO
    
    # Convert Vercel event to WSGI environ
    environ = {
        'REQUEST_METHOD': event['httpMethod'],
        'PATH_INFO': event['path'],
        'QUERY_STRING': '&'.join([f"{k}={v}" for k, v in event.get('queryStringParameters', {}).items()]),
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(event.get('body', '').encode('utf-8')),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    if event.get('body'):
        environ['CONTENT_LENGTH'] = str(len(event['body']))
    
    # Handle response
    response = Response.from_app(app, environ)
    
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True),
        'isBase64Encoded': False
    }
