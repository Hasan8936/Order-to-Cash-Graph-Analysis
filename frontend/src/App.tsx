/**
 * Main App component.
 */
import React, { useEffect } from "react";
import "./App.css";
import GraphCanvas from "./components/GraphCanvas";
import ChatPanel from "./components/ChatPanel";
import StatusBar from "./components/StatusBar";
import { useGraph } from "./hooks/useGraph";
import { useGraphStore } from "./store/graphStore";

function App() {
  const { fetchGraph } = useGraph();
  const { isLoading, error } = useGraphStore();

  useEffect(() => {
    console.log("App useEffect, calling fetchGraph");
    fetchGraph();
  }, [fetchGraph]);

  const { nodes, links } = useGraphStore();

  console.log("App render", { nodes: nodes.length, links: links.length, isLoading, error });

  return (
    <div className="app">
      <div className="app-container">
        <div className="graph-section">
          <GraphCanvas />
        </div>
        <div className="chat-section">
          <ChatPanel />
        </div>
      </div>
      <StatusBar isLoading={isLoading} error={error} />
      <div className="debug-panel">
        <p>Graph nodes: {nodes.length}</p>
        <p>Graph links: {links.length}</p>
      </div>
    </div>
  );
}

export default App;
