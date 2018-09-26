# pillow-pile
A proxy to enable hierarchical documents in CouchDB

**IMPORTANT:** this Project requires **Python 3.6 or higher**

# Development
#### Setup a Virtualenv  
    python -m venv venv
#### Install Dev dependencies  
    pip install tornado

#### Running locally  
1. Start your couchdb server locally (prefered way is docker)
2. Run the Pillow Pile Proxy Server
```bash
.\venv\Scripts\activate #on windows
python .\pillowpile\main.py --couchdb_url="http://localhost:32769" --debug 
```

# REST API
## Databases  

To create a database:  
**PUT (NO BODY)** http://localhost:8080/my-database  

To delete a database:  
**DELETE (NO BODY)** http://localhost:8080/my-database  

## Documents
To access a document:  
**GET** http://localhost:8080/my-database/my/document/path  

To create or update a document:  
**PUT (JSON)** http://localhost:8080/my-database/my/document/path  

To delete a document:  
**DELETE (NO BODY)** http://localhost:8080/my-database/my/document/path

## Index
**GET** http://localhost:8080/my-database/index