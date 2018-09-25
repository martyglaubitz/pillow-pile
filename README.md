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
           