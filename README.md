# vaulty
API around Vault


Using hvac library, for now that is good enough.
Orignal idea was to use requests library.
https://hvac.readthedocs.io/en/stable/usage/secrets_engines/kv_v1.html

### TO be added
* handling jwt token, you can use a examople of from observer-api.
* unit tests
* refactor of code, create into seperate files.
* freezing secrets, so they are stored for all-time


## use cases 
### use case 1.
get all the workspaces available for the user.
1. handle jwt token
2. get all the groups in the jwt token.
3. return all the groups of jwt token.

### use case 2. 
list all the secrets under workspace.
1. handle parameter "workspace"
2. check if workspace is part of jwt groups
3. get all the names of the secrets under workspace
4. return the names

### use case 3
get a secret
1. handle input "workspace" and "secret_name"
2. check if workspace is part of jwt groups
3. get secret based on "workspace" and "secret_name"
4. return secret

### use case 4
create a secret
1. handle input "workspace" and "secret_name"
2. check if workspace is part of jwt groups
3. handle input from http post request, eiher http_form or json.
4. get secret from input under "secret".
5. store secret based on "workspace" and "secret_name"

### use case 5
update a secret
1. handle input "workspace" and "secret_name"
2. check if workspace is part of jwt groups
3. handle input from http post request, eiher http_form or json.
4. get secret from input under "secret".
5. store secret based on "workspace" and "secret_name"


### use case 6
delete a secret
1. handle input "workspace" and "secret_name"
2. check if workspace is part of jwt groups
3. remove secret under  "secret_name"



# Start project
```
python3.7 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python app.py
```
