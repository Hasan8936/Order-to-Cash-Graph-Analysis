"""
Graph construction and conversion module.
Builds an in-memory NetworkX graph from SQLite data.
"""
import sqlite3
import networkx as nx
from typing import Any, Dict, List, Tuple
from ..db.connection import get_db_path


# Define node types and their key attributes
NODE_TYPES = {
    "SalesOrder": {"source_table": "sales_order_headers", "key_field": "salesOrder", "color": "#1f77b4"},
    "SalesOrderItem": {"source_table": "sales_order_items", "key_fields": ["salesOrder", "salesOrderItem"], "color": "#aec7e8"},
    "Customer": {"source_table": "business_partners", "key_field": "customer", "color": "#9467bd"},
    "BillingDocument": {"source_table": "billing_document_headers", "key_field": "billingDocument", "color": "#ff7f0e"},
    "BillingItem": {"source_table": "billing_document_items", "key_fields": ["billingDocument", "billingDocumentItem"], "color": "#ffbb78"},
    "Delivery": {"source_table": "outbound_delivery_headers", "key_field": "deliveryDocument", "color": "#2ca02c"},
    "JournalEntry": {"source_table": "journal_entry_items_accounts_receivable", "key_fields": ["accountingDocument", "accountingDocumentItem"], "color": "#d62728"},
    "Payment": {"source_table": "payments_accounts_receivable", "key_fields": ["accountingDocument", "accountingDocumentItem"], "color": "#17becf"},
    "Product": {"source_table": "product_descriptions", "key_field": "product", "color": "#7f7f7f"},
    "Plant": {"source_table": "plants", "key_field": "plant", "color": "#bcbd22"},
}

# Define edges and their join conditions
RELATIONSHIPS = [
    # (from_type, to_type, edge_label, from_table, to_table, join_condition)
    ("Customer", "SalesOrder", "PLACED", "business_partners", "sales_order_headers", "bp.customer = soh.soldToParty"),
    ("SalesOrder", "SalesOrderItem", "HAS_ITEM", "sales_order_headers", "sales_order_items", "soh.salesOrder = soi.salesOrder"),
    ("SalesOrderItem", "Product", "REFERENCES_PRODUCT", "sales_order_items", "product_descriptions", "soi.material = pd.product"),
    ("SalesOrderItem", "Plant", "PRODUCED_AT", "sales_order_items", "plants", "soi.productionPlant = p.plant"),
    ("SalesOrder", "Delivery", "FULFILLED_BY", "sales_order_headers", "outbound_delivery_headers", "soh.salesOrder LIKE '%' || odh.deliveryDocument || '%'"),
    ("BillingDocument", "Customer", "BILLED_TO", "billing_document_headers", "business_partners", "bdh.soldToParty = bp.customer"),
    ("BillingDocument", "Delivery", "REFERENCES_DELIVERY", "billing_document_headers", "outbound_delivery_headers", "bdh.billingDocument LIKE '%' || odh.deliveryDocument || '%'"),
    ("BillingItem", "Delivery", "SHIPS_FROM", "billing_document_items", "outbound_delivery_headers", "bdi.referenceSdDocument = odh.deliveryDocument"),
    ("BillingDocument", "JournalEntry", "GENERATES", "billing_document_headers", "journal_entry_items_accounts_receivable", "bdh.accountingDocument = je.referenceDocument"),
    ("JournalEntry", "Payment", "CLEARED_BY", "journal_entry_items_accounts_receivable", "payments_accounts_receivable", "je.clearingAccountingDocument = par.accountingDocument"),
]


def build_graph(db_path: str = None) -> nx.DiGraph:
    """
    Build a directed graph from SQLite data.
    Returns a NetworkX DiGraph with nodes and edges.
    """
    if db_path is None:
        db_path = get_db_path()
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    G = nx.DiGraph()
    
    # Add nodes by type
    for node_type, config in NODE_TYPES.items():
        table = config["source_table"]
        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT 1000")
            rows = cursor.fetchall()
            
            for row in rows:
                if "key_field" in config:
                    key = row[config["key_field"]]
                    node_id = f"{node_type}:{key}"
                else:
                    key_fields = config["key_fields"]
                    key = "|".join(str(row[f]) for f in key_fields)
                    node_id = f"{node_type}:{key}"
                
                # Add node with metadata
                G.add_node(
                    node_id,
                    type=node_type,
                    label=_make_label(node_id, dict(row)),
                    color=config["color"],
                    metadata=dict(row)
                )
        except Exception as e:
            print(f"Error loading nodes for {node_type}: {e}")
            continue
    
    # Add edges - simplified for now (full join logic would be more complex)
    # This is a basic implementation that can be expanded
    for node_id in G.nodes():
        pass  # Edge logic to be implemented based on your relationship rules
    
    conn.close()
    return G


def graph_to_json(G: nx.DiGraph) -> Dict[str, Any]:
    """
    Convert NetworkX graph to force-graph compatible JSON format.
    """
    nodes = []
    links = []
    node_id_map = {}
    
    # Convert nodes
    for idx, (node_id, attrs) in enumerate(G.nodes(data=True)):
        node_id_map[node_id] = idx
        nodes.append({
            "id": idx,
            "label": attrs.get("label", node_id),
            "type": attrs.get("type", "Unknown"),
            "color": attrs.get("color", "#999"),
        })
    
    # Convert edges
    for source, target, attrs in G.edges(data=True):
        if source in node_id_map and target in node_id_map:
            links.append({
                "source": node_id_map[source],
                "target": node_id_map[target],
                "label": attrs.get("label", ""),
            })
    
    return {
        "nodes": nodes,
        "links": links,
    }


def _make_label(node_id: str, attrs: dict) -> str:
    """
    Create a human-readable label for a node.
    """
    node_type = node_id.split(":")[0]
    
    # Customize label based on node type
    if node_type == "Customer":
        return attrs.get("businessPartnerFullName", node_id)
    elif node_type == "SalesOrder":
        return f"Order {attrs.get('salesOrder', node_id)}"
    elif node_type == "BillingDocument":
        return f"Invoice {attrs.get('billingDocument', node_id)}"
    elif node_type == "Delivery":
        return f"Delivery {attrs.get('deliveryDocument', node_id)}"
    elif node_type == "Product":
        return attrs.get("productDescription", attrs.get("product", node_id))
    else:
        return node_id


if __name__ == "__main__":
    # Test graph building
    G = build_graph()
    print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    # Export to JSON
    graph_json = graph_to_json(G)
    print(f"Exported {len(graph_json['nodes'])} nodes and {len(graph_json['links'])} links")
