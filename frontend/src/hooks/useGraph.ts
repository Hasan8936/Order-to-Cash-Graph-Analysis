/**
 * Custom hook for fetching and managing graph data.
 */
import { useCallback } from "react";
import axios from "axios";
import { useGraphStore } from "../store/graphStore";
import type { GraphData } from "../types";

// Normalize API base to avoid accidental double-slashes and provide a sensible
// browser fallback when `VITE_API_BASE` is not set in production.
const RAW_API_BASE = import.meta.env.VITE_API_BASE || "";
const API_BASE = (RAW_API_BASE.replace(/\/+$/g, "") || window.location.origin).replace(/\/+$/g, "");

export function useGraph() {
  const { setNodes, setLinks, setLoading, setError } = useGraphStore();

  const fetchGraph = useCallback(async () => {
    setLoading(true);
    try {
      const url = `${API_BASE}/api/graph`;
      console.log("Requesting graph from:", url);
      const response = await axios.get<{
        success: boolean;
        data: GraphData;
      }>(url, { timeout: 15000 });

      if (response.data.success) {
        const MAX_NODES = 1500;
        const MAX_LINKS = 3000;

        const nodes = response.data.data.nodes || [];
        const links = (response.data.data.links || []).filter(
          (link) => link.source != null && link.target != null
        );

        console.log("Fetched nodes:", nodes.length, "links:", links.length);

        if (nodes.length > MAX_NODES) {
          console.warn(`Graph has ${nodes.length} nodes - trimming to ${MAX_NODES}`);
        }

        const trimmedNodes = nodes.slice(0, MAX_NODES);
        const nodeIds = new Set(trimmedNodes.map((n) => n.id));
        const trimmedLinks = links
          .filter((link) => nodeIds.has(link.source) && nodeIds.has(link.target))
          .slice(0, MAX_LINKS);

        console.log("Setting nodes:", trimmedNodes.length, "links:", trimmedLinks.length);
        setNodes(trimmedNodes);
        setLinks(trimmedLinks);
      }
      setError(null);
    } catch (err: any) {
      // Surface HTTP details when available to help diagnose 404/500 issues
      const status = err?.response?.status;
      const statusText = err?.response?.statusText;
      const url = `${API_BASE}/api/graph`;
      const message = status
        ? `Request to ${url} failed with status ${status} ${statusText}`
        : err instanceof Error
        ? err.message
        : "Failed to fetch graph";

      setError(message);
      console.error("Error fetching graph:", {
        url,
        status,
        statusText,
        data: err?.response?.data,
        message: err?.message,
      });

      // If the first attempt used the configured API base and failed with
      // an origin-relative or double-slash path, try a safe fallback to the
      // current origin (useful when Vercel doesn't set VITE_API_BASE).
      try {
        if (RAW_API_BASE === "") {
          const fallbackUrl = `${window.location.origin}/api/graph`;
          console.warn("Retrying graph request with fallback URL:", fallbackUrl);
          const retryResp = await axios.get<{ success: boolean; data: GraphData }>(fallbackUrl, { timeout: 15000 });
          if (retryResp.data?.success) {
            setError(null);
            const nodes = retryResp.data.data.nodes || [];
            const links = (retryResp.data.data.links || []).filter((link) => link.source != null && link.target != null);
            const MAX_NODES = 1500;
            const MAX_LINKS = 3000;
            const trimmedNodes = nodes.slice(0, MAX_NODES);
            const nodeIds = new Set(trimmedNodes.map((n) => n.id));
            const trimmedLinks = links
              .filter((link) => nodeIds.has(link.source) && nodeIds.has(link.target))
              .slice(0, MAX_LINKS);
            setNodes(trimmedNodes);
            setLinks(trimmedLinks);
          }
        }
      } catch (retryErr) {
        console.error("Retry fetching graph failed:", retryErr);
      }
    } finally {
      setLoading(false);
    }
  }, [setNodes, setLinks, setLoading, setError]);

  const expandNode = useCallback(
    async (nodeId: string, depth: number = 1) => {
      try {
        const response = await axios.post<{
          success: boolean;
          expanded_nodes: string[];
        }>(`${API_BASE}/api/graph/expand`, null, {
          params: { node_id: nodeId, depth },
          timeout: 10000,
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
