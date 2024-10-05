import re
import json
import os

vault_dir = '/'
graph_data = {"nodes": [], "edges": []}
node_id = 1
node_map = {}

# Traverse the vault and extract nodes and edges
for root, dirs, files in os.walk(vault_dir):
    for file in files:
        if file.endswith('.md'):
            note_name = os.path.splitext(file)[0]
            file_path = os.path.join(root, file)

            # Add the note as a node
            graph_data["nodes"].append({"id": node_id, "label": note_name})
            node_map[note_name] = node_id
            current_node_id = node_id
            node_id += 1

            # Read file content and find [[links]]
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                links = re.findall(r'\[\[([^\]]+)\]\]', content)

                # Add edges for each link found
                for link in links:
                    link_name = link.strip()
                    if link_name in node_map:
                        link_node_id = node_map[link_name]
                        graph_data["edges"].append({"from": current_node_id, "to": link_node_id})

# Save graph data as JSON for use in visualization
with open('graph_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(graph_data, json_file)