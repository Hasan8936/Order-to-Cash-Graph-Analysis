/**
 * GraphCanvas component for visualizing the O2C graph.
 */
import { useRef } from "react";
import { ForceGraph2D } from "react-force-graph";
import { useGraphStore } from "../store/graphStore";
import NodePopup from "./NodePopup";
import "../styles/GraphCanvas.css";

interface NodeData {
  id: number;
  label: string;
  type: string;
  color: string;
  metadata?: Record<string, any>;
  x?: number;
  y?: number;
}

interface LinkData {
  source: number;
  target: number;
  label?: string;
}

function GraphCanvas() {
  const { nodes, links, selectedNodeId, setSelectedNodeId, highlightedNodes, error } =
    useGraphStore();
  const graphRef = useRef<any>(null);

  // Convert node IDs to indices for force-graph
  const nodeIndexMap = new Map(
    nodes.map((node, idx) => [node.id, idx])
  );

  const graphData = {
    nodes: nodes.map((node, idx) => ({
      id: idx,
      label: node.label,
      type: node.type,
      color: node.color,
      metadata: node.metadata,
      val: 3,
      highlighted: highlightedNodes.has(node.id),
    })),
    links: links.map((link) => ({
      source:
        typeof link.source === "string"
          ? nodeIndexMap.get(link.source) ?? 0
          : link.source,
      target:
        typeof link.target === "string"
          ? nodeIndexMap.get(link.target) ?? 0
          : link.target,
      label: link.label,
    })) as LinkData[],
  };

  const handleNodeClick = (node: NodeData) => {
    const nodeId = nodes[node.id]?.id;
    setSelectedNodeId(nodeId || null);
  };

  const handleNodeHover = (node: NodeData | null) => {
    if (graphRef.current && node) {
      graphRef.current.centerAt(node.x, node.y, 1000);
    }
  };

  if (error) {
    return (
      <div className="graph-canvas-container">
        <div className="graph-error">Error loading graph: {error}</div>
      </div>
    );
  }
  if (!nodes.length || !links.length) {
    return (
      <div className="graph-canvas-container">
        <div className="graph-empty">No graph data available.</div>
      </div>
    );
  }
  return (
    <div className="graph-canvas-container">
      <ForceGraph2D
        ref={graphRef}
        graphData={graphData}
        nodeCanvasObject={(node: any, ctx: any) => {
          const label = node.label;
          const size = node.highlighted ? 8 : 5;
          ctx.fillStyle = node.highlighted ? "#ff6b6b" : node.color;
          ctx.beginPath();
          ctx.arc(node.x, node.y, size, 0, 2 * Math.PI);
          ctx.fill();
          ctx.font = "12px Arial";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillStyle = "#000";
          ctx.fillText(label, node.x, node.y + size + 8);
        }}
        onNodeClick={handleNodeClick}
        onNodeHover={handleNodeHover}
        width={window.innerWidth * 0.6}
        height={window.innerHeight}
      />
      {selectedNodeId && (
        <NodePopup nodeId={selectedNodeId} onClose={() => setSelectedNodeId(null)} />
      )}
    </div>
  );
}

export default GraphCanvas;
