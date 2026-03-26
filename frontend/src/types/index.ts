/**
 * TypeScript interfaces for the O2C graph system.
 */

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  color: string;
  metadata?: Record<string, any>;
  x?: number;
  y?: number;
}

export interface GraphLink {
  source: string;
  target: string;
  label?: string;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

export interface Message {
  role: "user" | "assistant";
  content: string;
  sql?: string;
}

export interface ChatRequest {
  message: string;
  history?: Message[];
}

export interface ChatResponse {
  answer: string;
  sql?: string;
  sql_success: boolean;
  highlighted_nodes: Array<number | string>;
  error?: string;
}

export interface GraphState {
  nodes: GraphNode[];
  links: GraphLink[];
  selectedNodeId: string | number | null;
  highlightedNodes: Set<string | number>;
  isLoading: boolean;
  error: string | null;
}
