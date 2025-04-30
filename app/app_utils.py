from flask import jsonify, Response
import json

def json_response(data, status_code=200):
    """
    Create a JSON response with proper Content-Type header.
    
    Args:
        data: The data to convert to JSON
        status_code: HTTP status code (default: 200)
        
    Returns:
        Response object with JSON data and headers
    """
    # Convert data to JSON string
    json_str = json.dumps(data)
    
    # Create response with proper headers
    response = Response(
        json_str,
        status=status_code,
        mimetype='application/json'
    )
    
    # Set Content-Type header explicitly
    response.headers['Content-Type'] = 'application/json'
    
    return response 