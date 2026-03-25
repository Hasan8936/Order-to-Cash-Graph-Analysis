"""
Pydantic models for graph nodes and edges.
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class NodeMetadata(BaseModel):
    """Metadata for a graph node."""
    type: str
    label: str
    color: str
    x: Optional[float] = None
    y: Optional[float] = None


class Node(BaseModel):
    """A node in the force graph."""
    id: str
    label: str
    type: str
    color: str
    metadata: Optional[Dict[str, Any]] = None


class Link(BaseModel):
    """An edge/link in the force graph."""
    source: str
    target: str
    label: Optional[str] = None


class GraphData(BaseModel):
    """Complete graph data structure."""
    nodes: List[Node]
    links: List[Link]


class NodeDetail(BaseModel):
    """Detailed information about a single node."""
    id: str
    type: str
    label: str
    properties: Dict[str, Any]
    connections: int
