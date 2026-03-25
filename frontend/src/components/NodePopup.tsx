/**
 * NodePopup component for displaying detailed node information.
 */
import { useEffect, useState } from "react";
import { useGraphStore } from "../store/graphStore";
import "../styles/NodePopup.css";

interface NodePopupProps {
  nodeId: string;
  onClose: () => void;
}

interface NodeDetail {
  id: string;
  type: string;
  label: string;
  properties: Record<string, any>;
  connections: number;
}

function NodePopup({ nodeId, onClose }: NodePopupProps) {
  const [nodeDetail, setNodeDetail] = useState<NodeDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { nodes } = useGraphStore();

  useEffect(() => {
    // Fallback: Try to get node details from the graph store if API is missing
    const node = nodes.find((n) => n.id === nodeId);
    if (node) {
      setNodeDetail({
        id: node.id,
        type: node.type,
        label: node.label,
        properties: node.metadata || {},
        connections: 0,
      });
      setError(null);
    } else {
      setError("Node details not available.");
    }
    setLoading(false);
  }, [nodeId, nodes]);

  return (
    <div className="node-popup-overlay" onClick={onClose}>
      <div className="node-popup" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>
          ×
        </button>

        {loading ? (
          <div className="loading">Loading node details...</div>
        ) : error ? (
          <div className="error">{error}</div>
        ) : nodeDetail ? (
          <>
            <div className="popup-header">
              <h3>{nodeDetail.label}</h3>
              <span className="node-type">{nodeDetail.type}</span>
            </div>

            <div className="popup-content">
              <div className="connections">
                <strong>Connections:</strong> {nodeDetail.connections}
              </div>

              <div className="properties">
                <h4>Properties:</h4>
                <table>
                  <tbody>
                    {Object.entries(nodeDetail.properties).map(([key, value]) => (
                      <tr key={key}>
                        <td className="property-key">{key}</td>
                        <td className="property-value">
                          {typeof value === "object"
                            ? JSON.stringify(value)
                            : String(value)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
}

export default NodePopup;
