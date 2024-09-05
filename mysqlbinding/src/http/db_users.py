import json

def createuser(username, email):
    query = "INSERT INTO users(username,email) VALUES (?, ?)"
    params = [username, email]

    json_data = {
        "operation": "exec",
        "metadata": {
            "sql": query,
            "params": json.dumps(params)  # Convertimos los parámetros a un string JSON
        }
    }
    
    return json_data

def getusers():
    query = "SELECT * FROM users"

    json_data = {
        "operation": "query",
        "metadata": {
            "sql": query,
            "params": "[]"
        }
    }
    
    return json_data
def finduser(username):
    query = "SELECT * FROM users WHERE username=?"
    params = [username]

    json_data = {
        "operation": "query",
        "metadata": {
            "sql": query,
            "params": json.dumps(params)  # Convertimos los parámetros a un string JSON
        }
    }
    
    return json_data