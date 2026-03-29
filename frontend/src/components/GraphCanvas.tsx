import { useEffect, useRef } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { useGraph } from "../hooks/useGraph";
import { useGraphStore } from "../store/graphStore";
import "../styles/GraphCanvas.css";

function GraphCanvas() {
  const { fetchGraph, expandNode } = useGraph();
  const { nodes, links, isLoading, error, setSelectedNodeId } = useGraphStore();
  const fgRef = useRef<any>();

  useEffect(() => {
    fetchGraph();
  }, [fetchGraph]);

  // Prefer showing explicit errors to avoid the UI getting stuck on "Loading"
  if (error) {
    return <div className="graph-canvas-container">Error loading graph: {error}</div>;
  }

  // Only show loading while an active request is in-flight. If loading
  // is false but we still have no nodes, show a helpful message so the
  // user isn't left with a perpetual "Loading" state.
  if (isLoading) return <div className="graph-canvas-container">Loading graph data...</div>;
  if (!isLoading && nodes.length === 0)
    return <div className="graph-canvas-container">No graph data available (check backend/API and env vars).</div>;

  // Map store nodes/links to force-graph expected shape
  const graphData = {
    nodes: nodes.map((n: any) => ({ id: String(n.id), name: n.label || String(n.id), color: n.color })),
    links: links.map((l: any) => ({ source: String(l.source), target: String(l.target), label: l.label }))
  };

  return (
    <div className="graph-canvas-container" role="region" aria-label="Graph canvas">
      <div className="graph-summary">
        <strong>Nodes:</strong> {nodes.length} &nbsp; <strong>Links:</strong> {links.length}
      </div>

      <ForceGraph2D
        ref={fgRef}
        graphData={graphData}
        nodeAutoColorBy={"color"}
        nodeLabel={(node: any) => node.name}
        nodeCanvasObject={(node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
          const label = node.name;
          const fontSize = 12 / globalScale;
          ctx.fillStyle = node.color || "#1f77b4";
          ctx.beginPath();
          ctx.arc(node.x, node.y, 5, 0, 2 * Math.PI, false);
          ctx.fill();
          ctx.font = `${fontSize}px Sans-Serif`;
          ctx.fillStyle = "#222";
          ctx.fillText(label, node.x + 8, node.y + fontSize / 2);
        }}
        onNodeClick={(node: any) => {
          setSelectedNodeId(node.id);
          expandNode(String(node.id), 1).catch(() => {});
        }}
        linkDirectionalArrowLength={3}
        linkDirectionalParticles={0}
        width={800}
        height={600}
      />

      <div className="graph-footer">Drag to explore. Click a node to expand.</div>
    </div>
  );
}

export default GraphCanvas;

