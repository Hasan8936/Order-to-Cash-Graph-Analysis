/**
 * Zustand store for graph and chat state.
 */
import { create } from "zustand";
import type { GraphState, GraphNode, GraphLink } from "../types";

interface Store extends GraphState {
  setNodes: (nodes: GraphNode[]) => void;
  setLinks: (links: GraphLink[]) => void;
  setSelectedNodeId: (id: string | null) => void;
  setHighlightedNodes: (ids: string[]) => void;
  addHighlightedNode: (id: string) => void;
  clearHighlightedNodes: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useGraphStore = create<Store>((set) => ({
  nodes: [],
  links: [],
  selectedNodeId: null,
  highlightedNodes: new Set<string>(),
  isLoading: false,
  error: null,

  setNodes: (nodes) => set({ nodes }),
  setLinks: (links) => set({ links }),
  setSelectedNodeId: (id) => set({ selectedNodeId: id }),
  setHighlightedNodes: (ids) => set({ highlightedNodes: new Set(ids) }),
  addHighlightedNode: (id) => set((state) => ({
    highlightedNodes: new Set([...state.highlightedNodes, id]),
  })),
  clearHighlightedNodes: () => set({ highlightedNodes: new Set<string>() }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
}));
