
def get_document_entry_for_path(graph_json: dict, path_components: list):
    last_path_component = path_components[-1]
    parent_doc = graph_json
    result = None
    for path_component in path_components:
        if not path_component in parent_doc:
            return None, parent_doc

        result = parent_doc[path_component]
        if path_component == last_path_component:
            return result, parent_doc

        parent_doc = result


