
import sys
import os
from flask import Flask

# Add the current directory to the path so we can import app
sys.path.append(os.getcwd())

try:
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    
    with app.test_client() as client:
        print("Attempting to fetch /modules/fertilizer-rec...")
        response = client.get('/modules/fertilizer-rec')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 500:
            print("Error 500 Reproduced!")
            # In debug mode, the response data might contain the stack trace
            print(response.data.decode('utf-8'))
        elif response.status_code == 200:
            print("Success! Template rendered correctly.")
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(response.data.decode('utf-8'))

except Exception as e:
    print(f"Exception occurred: {e}")
    import traceback
    traceback.print_exc()
