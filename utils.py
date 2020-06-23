
def extract_data(request):
    """Return JSON decoded or form data from request.

    Args:
    request (flask.request): flask request object

    Returns:
    dict: JSON decoded or form data
    """
    payload = request.get_json()
    if payload is None:
        payload = request.form.to_dict()
    return payload
