/**
 * GraphCanvas component for visualizing the O2C graph.
 */
import { useEffect, useRef, useState } from "react";
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

function GraphCanvas() {
  const { nodes, links, selectedNodeId, setSelectedNodeId, highlightedNodes, error } =
    useGraphStore();
  const containerRef = useRef<HTMLDivElement>(null);
  const graphRef = useRef<any>(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  useEffect(() => {
    const updateDimensions = () => {
      const container = containerRef.current;
      if (container) {
        setDimensions({ width: container.clientWidth, height: container.clientHeight });
      }
    };

    updateDimensions();
    const resizeObserver = new ResizeObserver(() => updateDimensions());
    if (containerRef.current) resizeObserver.observe(containerRef.current);

    window.addEventListener("resize", updateDimensions);
    return () => {
      window.removeEventListener("resize", updateDimensions);
      resizeObserver.disconnect();
    };
  }, []);

  console.log("GraphCanvas render", { nodes: nodes.length, links: links.length, error });

  const graphData = {
    nodes: nodes.map((node) => ({
      ...node,
      highlighted: highlightedNodes.has(node.id),
      val: 3,
    })),
    links: links.map((link) => ({
      source: link.source,
      target: link.target,
      label: link.label,
    })),
  };

  console.log("graphData", graphData);

  const handleNodeClick = (node: NodeData) => {
    setSelectedNodeId(node.id);
  };

  const handleNodeHover = (node: NodeData | null) => {
    if (graphRef.current && node && node.x != null && node.y != null) {
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
    <div className="graph-canvas-container" ref={containerRef}>
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
        width={dimensions.width}
        height={dimensions.height}
      />
      {selectedNodeId !== null && (
        <NodePopup nodeId={selectedNodeId} onClose={() => setSelectedNodeId(null)} />
      )}
    </div>
  );
}

export default GraphCanvas;
