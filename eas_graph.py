import streamlit as st
import requests
from pyvis.network import Network
import tempfile
import pandas as pd
import g4f
from streamlit.components.v1 import html


def chat_bot(prompt):
    response = g4f.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model=g4f.models.default,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    return response


@st.cache_resource
def generate_summary(df):
    csv_data_str = df.to_string(index=False)
    prompt = f"Here EAS protocol transactions data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and there connections in points"
    st.write(chat_bot(prompt))


def fetch_data(order_by, take):
    query = f"""
    query MyQuery {{
      timestamps(take: {take}, orderBy: {{ {order_by}: desc }}) {{
        from
        id
        timestamp
        tree
        txid
      }}
      aggregateAttestation(take: {take}, orderBy: {{ time: desc }}) {{
        _count {{
          attester
          expirationTime
          id
          ipfsHash
          isOffchain
          recipient
          refUID
          revocable
          revocationTime
          revoked
          schemaId
          time
          timeCreated
          txid
        }}
      }}
    }}
    """
    url = "https://optimism.easscan.org/graphql"
    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
        data = response.json()['data']
        return data
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

def create_network_graph(data):
    df_timestamps = pd.DataFrame(data['timestamps'])
    df_aggregate = pd.DataFrame(data['aggregateAttestation']['_count'].items())

    nodes = []
    edges = []

    for _, row in df_timestamps.iterrows():
        from_address = row['from']
        txid = row['txid']
        timestamp = row['timestamp']
        id = row['id']

        nodes.extend([
            {'id': f"From: {from_address}", 'label': f"From: {from_address}", 'title': f"Timestamp: {timestamp}"},
            {'id': f"TxID: {txid}", 'label': f"TxID: {txid}", 'title': f"ID: {id}"}
        ])

        edges.append({'source': f"From: {from_address}", 'target': f"TxID: {txid}"})

    for _, row in df_aggregate.iterrows():
        nodes.append({'id': row[0], 'label': row[0], 'title': f"Count: {row[1]}"})

    graph = Network(height="800px", width="100%", notebook=True)

    for node in nodes:
        graph.add_node(node['id'], label=node['label'], title=node['title'])

    for edge in edges:
        graph.add_edge(edge['source'], edge['target'])

    search_filter_script = """
    <script>
    function searchNodes() {
        var input = document.getElementById('searchInput').value;
        var nodes = network.body.data.nodes;
        nodes.forEach(function(node) {
            if (node.label.includes(input)) {
                network.selectNodes([node.id]);
                network.focus(node.id, {scale: 1.5});
            }
        });
    }
    </script>
    """

    search_input_html = """
    <div>
      <input type="text" id="searchInput" placeholder="Search for a wallet address...">
      <button onclick="searchNodes()">Search</button>
    </div>
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        graph.show(tmpfile.name)
        tmpfile.seek(0)
        html_content = tmpfile.read().decode("utf-8")

    html_content = search_filter_script + search_input_html + html_content

    return html_content

def fetch_offchain_revocations(order_by, take):
    query = f"""
    query MyQuery {{
      offchainRevocations(take: {take}, orderBy: {{ {order_by}: desc }}) {{
        uid
        txid
        timestamp
        id
        from
      }}
    }}
    """
    url = "https://optimism.easscan.org/graphql"
    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
        data = response.json()['data']['offchainRevocations']
        return data
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

def create_offchain_revocations_network_graph(revocations):
    df = pd.DataFrame(revocations)

    nodes = []
    edges = []

    for _, revocation in df.iterrows():
        uid = revocation['uid']
        from_address = revocation['from']
        txid = revocation['txid']
        timestamp = revocation['timestamp']

        nodes.extend([
            {'id': f"UID: {uid}", 'label': f"UID: {uid}", 'title': f"TXID: {txid}"},
            {'id': f"From: {from_address}", 'label': f"From: {from_address}", 'title': f"Timestamp: {timestamp}"}
        ])

        edges.append({'source': f"From: {from_address}", 'target': f"UID: {uid}"})

    graph = Network(height="800px", width="100%", notebook=True)

    for node in nodes:
        graph.add_node(node['id'], label=node['label'], title=node['title'])

    for edge in edges:
        graph.add_edge(edge['source'], edge['target'])

    search_filter_script = """
    <script>
    function searchNodes() {
        var input = document.getElementById('searchInput').value;
        var nodes = network.body.data.nodes;
        nodes.forEach(function(node) {
            if (node.label.includes(input)) {
                network.selectNodes([node.id]);
                network.focus(node.id, {scale: 1.5});
            }
        });
    }
    </script>
    """

    search_input_html = """
    <div>
      <input type="text" id="searchInput" placeholder="Search for a wallet address...">
      <button onclick="searchNodes()">Search</button>
    </div>
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        graph.show(tmpfile.name)
        tmpfile.seek(0)
        html_content = tmpfile.read().decode("utf-8")

    html_content = search_filter_script + search_input_html + html_content

    return html_content





def fetch_schema_names(order_by, take):
    # Constructing the query with the user-selected orderBy metric
    query = f"""
    query MyQuery {{
      schemaNames(take: {take}, orderBy: {{ {order_by}: desc }}) {{
        time
        schemaId
        name
        isCreator
        id
        attesterAddress
      }}
    }}
    """
    
    # Updated URL for the GraphQL endpoint
    url = "https://optimism.easscan.org/graphql"
    response = requests.post(url, json={'query': query})
    
    if response.status_code == 200:
        data = response.json()['data']['schemaNames']
        return data
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

def create_schema_names_network_graph(schema_names):
    # Filters for the graph
    df = pd.DataFrame(schema_names)

    nodes = []
    edges = []

    for _, schema in df.iterrows():
        schema_id = schema['schemaId']
        attester_address = schema['attesterAddress']
        name = schema['name']
        time = schema['time']

        nodes.extend([
            {'id': f"Schema ID: {schema_id}", 'label': f"Schema ID: {schema_id}", 'title': f"Name: {name}"},
            {'id': f"Attester Address: {attester_address}", 'label': f"Attester Address: {attester_address}", 'title': f"Time: {time}"}
        ])

        edges.extend([
            {'source': f"Schema ID: {schema_id}", 'target': f"Attester Address: {attester_address}"}
        ])

    graph = Network(height="800px", width="100%", notebook=True)

    for node in nodes:
        graph.add_node(node['id'], label=node['label'], title=node['title'])

    for edge in edges:
        graph.add_edge(edge['source'], edge['target'])

    search_filter_script = """
    <script>
    function searchNodes() {
        var input = document.getElementById('searchInput').value;
        var nodes = network.body.data.nodes;
        nodes.forEach(function(node) {
            if (node.label.includes(input)) {
                network.selectNodes([node.id]);
                network.focus(node.id, {scale: 1.5});
            }
        });
    }
    </script>
    """

    search_input_html = """
    <div>
      <input type="text" id="searchInput" placeholder="Search for a wallet address...">
      <button onclick="searchNodes()">Search</button>
    </div>
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        graph.show(tmpfile.name)
        tmpfile.seek(0)
        html_content = tmpfile.read().decode("utf-8")

    html_content = search_filter_script + search_input_html + html_content

    return html_content


def fetch_attestations(order_by, take):
    # Constructing the query with the user-selected orderBy metric
    query = f"""
    query MyQuery {{
      attestations(take: {take}, orderBy: {{ {order_by}: desc }}) {{
        attester
        expirationTime
        id
        ipfsHash
        recipient
        txid
        timeCreated
        time
        isOffchain
        revocable
        revocationTime
        revoked
        refUID
      }}
    }}
    """
    
    # Updated URL for the GraphQL endpoint
    url = "https://optimism.easscan.org/graphql"
    response = requests.post(url, json={'query': query})
    
    if response.status_code == 200:
        data = response.json()['data']['attestations']
        return data
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

def create_attestations_network_graph(attestations):
    # Filters for the graph
    st.subheader("Filter Options for Graph")
    df = pd.DataFrame(attestations)
    
    selected_attester = st.selectbox("Filter by Attester", ["All"] + df['attester'].unique().tolist())
    selected_recipient = st.selectbox("Filter by Recipient", ["All"] + df['recipient'].unique().tolist())
    
    # Apply filters
    if selected_attester != "All":
        df = df[df['attester'] == selected_attester]
    if selected_recipient != "All":
        df = df[df['recipient'] == selected_recipient]
    
    # Extracting data for nodes and edges based on filtered DataFrame
    nodes = []
    edges = []
    
    for _, attestation in df.iterrows():
        attester = attestation['attester']
        recipient = attestation['recipient']
        txid = attestation['txid']
        time_created = attestation['timeCreated']
        ipfs_hash = attestation['ipfsHash']
        
        # Adding nodes
        nodes.extend([
            {'id': f"Attester: {attester}", 'label': f"Attester: {attester}", 'title': f"TxID: {txid}"},
            {'id': f"Recipient: {recipient}", 'label': f"Recipient: {recipient}", 'title': f"Time Created: {time_created}"},
            {'id': f"IPFS Hash: {ipfs_hash}", 'label': f"IPFS Hash: {ipfs_hash}", 'title': ''}
        ])
        
        # Adding edges
        edges.extend([
            {'source': f"Attester: {attester}", 'target': f"Recipient: {recipient}"},
            {'source': f"Attester: {attester}", 'target': f"IPFS Hash: {ipfs_hash}"}
        ])
    
    # Creating the network graph
    graph = Network(height="800px", width="100%", notebook=True)
    
    for node in nodes:
        graph.add_node(node['id'], label=node['label'], title=node['title'])
    
    for edge in edges:
        graph.add_edge(edge['source'], edge['target'])

    # Using a temporary file to display the graph
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        graph.show(tmpfile.name)
        tmpfile.seek(0)
        html_content = tmpfile.read().decode("utf-8")

    return html_content



    
def eas_graph():
    option = st.radio(
        "Select Choice",
        ("attestations",'schemaNames','offchainRevocations','Timestamps'),
        index=0,
        horizontal=True
    )

    if option == 'attestations':
            # Initialize session state variables
            if 'data' not in st.session_state:
                st.session_state['data'] = None
            if 'order_by' not in st.session_state:
                st.session_state['order_by'] = 'timeCreated'
            if 'take' not in st.session_state:
                st.session_state['take'] = 10

            # User input for the orderBy metric
            order_by_options = [
                "attester", "expirationTime", "id", "ipfsHash", "recipient", 
                "txid", "timeCreated", "time", "isOffchain", 
                "revocable", "revocationTime", "revoked", "refUID"
            ]
            st.session_state['order_by'] = st.selectbox("Order By", order_by_options, index=order_by_options.index(st.session_state['order_by']))

            # Input for number of records to fetch
            st.session_state['take'] = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=st.session_state['take'])

            # Fetch data button
            if st.button('Fetch Data'):
                st.session_state['data'] = fetch_attestations(st.session_state['order_by'], st.session_state['take'])

            # Only proceed if data is available
            if st.session_state['data']:
                st.dataframe(pd.DataFrame(st.session_state['data']))
                st.markdown("##")
                graph_html = create_attestations_network_graph(st.session_state['data'])
                if graph_html:
                    st.components.v1.html(graph_html, height=900)

                generate_summary(pd.DataFrame(st.session_state['data']))
            
    elif option == 'schemaNames':

        order_by_options = ["time", "schemaId", "name", "isCreator", "id", "attesterAddress"]
        order_by = st.selectbox("Order By", order_by_options, index=0)

        take = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)

        if st.button('Fetch Data'):
            data = fetch_schema_names(order_by, take)

            if data:
                st.dataframe(pd.DataFrame(data))
                st.markdown("##")
                graph_html = create_schema_names_network_graph(data)
                if graph_html:
                    st.components.v1.html(graph_html, height=900)

                st.markdown("##")
                generate_summary(pd.DataFrame(data))
    
    elif option == 'offchainRevocations':
        order_by_options = ["timestamp", "uid", "txid", "id", "from"]
        order_by = st.selectbox("Order By", order_by_options, index=0)

        take = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)

        if st.button('Fetch Data'):
            data = fetch_offchain_revocations(order_by, take)

            if data:
                st.dataframe(pd.DataFrame(data))
                graph_html = create_offchain_revocations_network_graph(data)
                if graph_html:
                    st.components.v1.html(graph_html, height=900)

                st.markdown("##")
                generate_summary(pd.DataFrame(data))

    elif option == 'Timestamps':
        order_by_options = ["timestamp", "time"]
        order_by = st.selectbox("Order By", order_by_options, index=0)

        take = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)

        if st.button('Fetch Data'):
            data = fetch_data(order_by, take)

            if data:
                st.dataframe(pd.DataFrame(data['timestamps']))
                st.dataframe(pd.DataFrame(data['aggregateAttestation']['_count'].items(), columns=['Metric', 'Count']), width=1200)
                graph_html = create_network_graph(data)
                if graph_html:
                    st.components.v1.html(graph_html, height=900)
