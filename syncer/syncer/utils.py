

URI_PATH_SEPARATOR = "/"


def build_uri(uri, *components):
    if uri.endswith(URI_PATH_SEPARATOR):
        uri = uri[:-1]

    for component in components:
        if component.startswith(URI_PATH_SEPARATOR):
            component = component[1:]

        uri = f"{uri}{URI_PATH_SEPARATOR}{component}"

    return uri
