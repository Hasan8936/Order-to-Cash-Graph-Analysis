/**
 * Custom hook for fetching and managing graph data.
 */
import { useEffect, useCallback } from "react";
import axios from "axios";
import { useGraphStore } from "../store/graphStore";
import type { GraphData } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export function useGraph() {
  const { setNodes, setLinks, setLoading, setError } = useGraphStore();

  const fetchGraph = useCallback(async () => {
    setLoading(true);
    try {
      const response = await axios.get<{
        success: boolean;
        data: GraphData;
      }>(`${API_BASE}/api/graph`);

      if (response.data.success) {
        const MAX_NODES = 1500;
        const MAX_LINKS = 3000;

        const nodes = response.data.data.nodes || [];
        const links = (response.data.data.links || []).filter(
          (link) => link.source != null && link.target != null
        );

        if (nodes.length > MAX_NODES) {
          console.warn(`Graph has ${nodes.length} nodes - trimming to ${MAX_NODES}`);
        }

        const trimmedNodes = nodes.slice(0, MAX_NODES);
        const nodeIds = new Set(trimmedNodes.map((n) => n.id));
        const trimmedLinks = links
          .filter((link) => nodeIds.has(link.source as any) && nodeIds.has(link.target as any))
          .slice(0, MAX_LINKS);

        setNodes(trimmedNodes);
        setLinks(trimmedLinks);
      }
      setError(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to fetch graph";
      setError(message);
      console.error("Error fetching graph:", err);
    } finally {
      setLoading(false);
    }
  }, [setNodes, setLinks, setLoading, setError]);

  useEffect(() => {
    fetchGraph();
  }, [fetchGraph]);

  const expandNode = useCallback(
    async (nodeId: string, depth: number = 1) => {
      try {
        const response = await axios.post<{
          success: boolean;
          expanded_nodes: string[];
        }>(`${API_BASE}/api/graph/expand`, null, {
          params: { node_id: nodeId, depth },
        });

        if (response.data.success) {
          // Optionally highlight expanded nodes
          console.log("Expanded nodes:", response.data.expanded_nodes);
        }
      } catch (err) {
        console.error("Error expanding node:", err);
      }
    },
    []
  );

  return { fetchGraph, expandNode };
}
