def get_document_entry_for_path(graph_json: dict, path_components: list):
    last_path_component = path_components[-1]
    parent_doc = graph_json
    result = None

    path_components_index = 0
    for path_component in path_components:
        if not path_component in parent_doc:
            return None, dict(parent_doc), path_components[path_components_index:]

        result = parent_doc[path_component]
        if path_component == last_path_component:
            return dict(result), dict(parent_doc), None

        path_components_index += 1
        parent_doc = result

def create_doc_node_in_graph(graph_json: dict, path_components: list, new_doc_uuid: str):
    new_graph_node = graph_json

    for path_component in path_components:
        if not path_component in new_graph_node:
            new_graph_node[path_component] = dict()

        new_graph_node = new_graph_node[path_component]

    new_graph_node['id'] = new_doc_uuid

def delete_doc_node_from_graph(graph_json: dict, path_components: list) -> bool:
    doc_ref, parent_doc, _ = get_document_entry_for_path(graph_json, path_components)
    if not doc_ref:
        return False

    if len(doc_ref.keys()) > 1:
        doc_ref.pop('id', None) # if the node to delete is parent of other nodes, only remove his couch document id
    else:
        # otherwise drop the entire node by removing it from the parent
        node_name_in_parent = path_components[-1]
        parent_doc.pop(node_name_in_parent, None)


    return True
