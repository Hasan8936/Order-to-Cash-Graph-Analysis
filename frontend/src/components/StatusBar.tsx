/**
 * StatusBar component for displaying connection and loading status.
 */
import "../styles/StatusBar.css";

interface StatusBarProps {
  isLoading?: boolean;
  error?: string | null;
}

function StatusBar({ isLoading = false, error = null }: StatusBarProps) {
  return (
    <div className="status-bar">
      <div className="status-content">
        <span className={`status-indicator ${error ? "error" : "connected"}`}>
          ●
        </span>
        <span className="status-text">
          {error ? `Error: ${error}` : isLoading ? "Loading..." : "Connected"}
        </span>
      </div>
    </div>
  );
}

export default StatusBar;
