from flask import Flask, jsonify, request

app = Flask(__name__)

VAULT_TOKEN = "vault_root_token"
PROJECT_NAME = "vaulty"

OPTIONS = {
    "list": "list workspaces user is part of",
    "<workspace>/list": "list of secrets stored for workspace",
    "<workspace>/read/<secret_name>": "get secret",
    "<workspace>/create/<secret_name>": "create secret",
    "<workspace>/update/<secret_name>": "update secret",
    "<workspace>/delete/<secret_name>": "delete secret",
}

# vault operations
import hvac

VAULT_HOST = 'https://127.0.0.1:1234'
VAULT_TOKEN = 'vault_root_token' 
client = hvac.Client(
    url= VAULT_HOST,
    token=VAULT_TOKEN,
    #cert=(client_cert_path, client_key_path),
    #verify=server_cert_path,
)

import string

ALLOWED_CHARS = {i:i for i in string.ascii_letters}

def remove_all_non_ascii_letters(s):
    return ''.join(ALLOWED_CHARS.get(i, '') for i in s)


def create_path(namespace, workspace, name=''):
    return '/'.join(namespace, workspace, name)


def clean_input(f):
    def inner(workspace, name, *args, **kwargs):
        cleaned_workspace = remove_all_non_ascii_letters(workspace)
        cleaned_name = remove_all_non_ascii_letters(name)
        return f(cleaned_workspace, cleaned_name, *args, **kwargs)
    return inner


@clean_input
def vault_list(workspace, name):
    path = create_path(PROJECT_NAME, cleaned_workspace)
    return client.secrets.kv.v1.list_secrets(path=path)


@clean_input
def vault_read(workspace, name):
    return 


@clean_input
def vault_create(workspace, name, secret):
    path = create_path(PROJECT_NAME, cleaned_workspace, cleaned_name)

    client.secrets.kv.v1.create_or_update_secret(
        path=path,
        secret={"secret": secret},
    )

    return


@clean_input
def vault_update(workspace, name, secret):
    vault_create(workspace, name, secret)
    return 


@clean_input
def vault_delete(workspace, name):
    path = create_path(PROJECT_NAME, cleaned_workspace, cleaned_name)

    client.secrets.kv.v1.delete_secret(path=path)
    return


# util functions
def get_secret(request):
    # TODO handle both form and json
    return request.get_json()["secret"]


def decode(jwt):
    return {"usergroups": ["admin", "apple"]}


def get_userdata(request):
    jwt = request.headers.get("X-Auth")
    return decode(jwt)


def get_workspaces(userdata):
    groups = userdate["groups"]
    groups.append("personal")
    return groups


@app.route("/")
def index():
    return jsonify(OPTIONS)


# get all workspaces for user


@app.route("/workspaces/")
def list_workspaces():
    userdata = get_userdata(request)
    workspaces = get_workspaces(userdata)
    return jsonify({"workspaces": workspaces})



# rest handlers

@app.route("/<workspace>/list/")
def list(workspace, name):
    userdata = get_userdata(request)
    workspaces = get_workspaces(userdata)
    if workspace not in workspaces:
        raise

    items = vault_list(workspace)
    return jsonify(items)


@app.route("/<workspace>/create/<name>")
def create(workspace, name):
    userdata = get_userdata(request)
    workspaces = get_workspaces(userdata)
    if workspace not in workspaces:
        raise

    secret = get_secret(request)
    success = vault_create(workspace, name, secret)
    return jsonify({"message": "f{success}"})


@app.route("/<workspace>/read/<name>")
def read(workspace, name):
    userdata = get_userdata(request)
    workspaces = get_workspaces(userdata)
    if workspace not in workspaces:
        raise

    secret = vault_read(workspace, name)
    return jsonify({"secret": secret})


@app.route("/<workspace>/update/<name>")
def update(workspace, name):
    userdata = get_userdata(request)
    workspaces = get_workspaces(userdata)
    if workspace not in workspaces:
        raise

    secret = get_secret(request)
    success = vault_update(workspace, name, secret)
    return jsonify({"message": "f{success}"})


@app.route("/<workspace>/delete/<name>")
def delete(workspace, name):
    userdata = get_userdata(request)
    workspaces = get_workspaces(userdata)
    if workspace not in workspaces:
        raise

    success = vault_delete(workspace, name)
    return jsonify({"message": "f{success}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
