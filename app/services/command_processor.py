from ..services import generate_rang_response, generate_hello_response

def process_command(message):
    if message == "/rang":
        return generate_rang_response()
    elif message == "/hello":
        return generate_hello_response()
    
    return None
