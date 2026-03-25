"""
Graph API endpoints.
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from ..graph.builder import build_graph, graph_to_json

router = APIRouter()

# Global graph (built once at startup)
_graph_cache = None


def get_graph():
    """Get or build the graph."""
    global _graph_cache
    if _graph_cache is None:
        _graph_cache = build_graph()
    return _graph_cache


@router.get("/api/graph")
async def get_graph_data():
    """Get full graph as JSON for visualization."""
    try:
        G = get_graph()
        graph_json = graph_to_json(G)
        return {
            "success": True,
            "data": graph_json,
            "node_count": len(graph_json["nodes"]),
            "link_count": len(graph_json["links"])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building graph: {str(e)}")


@router.get("/api/node/{node_id}")
async def get_node_detail(node_id: str):
    """Get detailed information about a specific node."""
    try:
        G = get_graph()
        
        if node_id not in G.nodes:
            raise HTTPException(status_code=404, detail="Node not found")
        
        node_data = G.nodes[node_id]
        
        # Find connected nodes
        connections = list(G.successors(node_id)) + list(G.predecessors(node_id))
        
        return {
            "success": True,
            "node": {
                "id": node_id,
                "type": node_data.get("type"),
                "label": node_data.get("label"),
                "metadata": node_data.get("metadata"),
                "connections": len(set(connections))
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching node: {str(e)}")


@router.post("/api/graph/expand")
async def expand_node(node_id: str, depth: int = 1):
    """Expand a node to show connected nodes up to depth."""
    try:
        G = get_graph()
        
        if node_id not in G.nodes:
            raise HTTPException(status_code=404, detail="Node not found")
        
        # Get neighbors at specified depth
        visited = set()
        to_visit = [(node_id, 0)]
        
        while to_visit:
            current, current_depth = to_visit.pop(0)
            if current in visited or current_depth > depth:
                continue
            
            visited.add(current)
            
            if current_depth < depth:
                for neighbor in G.successors(current) | G.predecessors(current):
                    if neighbor not in visited:
                        to_visit.append((neighbor, current_depth + 1))
        
        return {
            "success": True,
            "expanded_nodes": list(visited),
            "node_count": len(visited)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error expanding node: {str(e)}")
