import re
import json
import os

vault_dir = '/'
graph_data = {"nodes": [], "edges": []}
node_id = 1
node_map = {}
node_connections = {}  # Keep track of connections

# Traverse the vault and extract nodes and edges
for root, dirs, files in os.walk(vault_dir):
    for file in files:
        if file.endswith('.md'):
            note_name = os.path.splitext(file)[0]
            file_path = os.path.join(root, file)

            # Add the note as a potential node (but don't add it to the graph yet)
            if note_name not in node_map:
                node_map[note_name] = node_id
                node_connections[note_name] = 0  # Initialize connection count
                current_node_id = node_id
                node_id += 1
            else:
                current_node_id = node_map[note_name]

            # Read file content and find [[links]]
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                links = re.findall(r'\[\[([^\]]+)\]\]', content)

                # Add edges for each link found
                for link in links:
                    link_name = link.strip()
                    if link_name not in node_map:
                        link_node_id = node_id
                        node_map[link_name] = node_id
                        node_connections[link_name] = 0  # Initialize connection count
                        node_id += 1
                    else:
                        link_node_id = node_map[link_name]

                    # Create edge between current note and linked note
                    graph_data["edges"].append({"from": current_node_id, "to": link_node_id})
                    
                    # Increment connection count for both nodes
                    node_connections[note_name] += 1
                    node_connections[link_name] += 1

# Now add only connected nodes to the final graph data
for note_name, note_id in node_map.items():
    if node_connections[note_name] > 0:
        graph_data["nodes"].append({"id": note_id, "label": note_name})

# Save graph data as JSON for use in visualization
with open('graph_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(graph_data, json_file)