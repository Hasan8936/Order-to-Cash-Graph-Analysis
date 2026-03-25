# Graph-Based Order-to-Cash Query System

A sophisticated web application that visualizes Order-to-Cash (O2C) business processes as an interactive graph and enables natural language queries powered by AI.

## 🚀 Features

- **Interactive Graph Visualization**: Explore O2C relationships between sales orders, deliveries, billing documents, payments, and more
- **Natural Language Queries**: Ask questions in plain English and get instant SQL generation with graph highlighting
- **AI-Powered SQL Generation**: Uses Google Gemini API with two-layer guardrails for safe and accurate queries
- **Real-time Node Highlighting**: Relevant graph nodes light up based on query results
- **Comprehensive O2C Data**: 16 interconnected tables with 17K+ records
- **Modern Web Stack**: React frontend with TypeScript, FastAPI backend with SQLite

## 🏗️ Architecture

### Backend (FastAPI + SQLite)
- **Graph Construction**: NetworkX-based graph from SQLite data
- **LLM Integration**: Gemini API for natural language to SQL conversion
- **API Endpoints**: RESTful APIs for graph data and chat queries
- **Data Layer**: SQLite with 16 O2C tables (sales orders, billing, payments, etc.)

### Frontend (React + Vite)
- **Graph Visualization**: Force-directed graph using react-force-graph-2d
- **State Management**: Zustand for global state
- **Chat Interface**: Real-time messaging with SQL preview
- **Responsive Design**: Modern UI with error handling

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Git

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Graph-Based Data Modeling and Query System"
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

## ⚙️ Configuration

1. **Set API Key**
   ```bash
   # In backend directory
   $env:GEMINI_API_KEY = "your-gemini-api-key-here"
   ```

2. **Environment Variables** (optional)
   - `DB_PATH`: Path to SQLite database (default: backend/o2c.db)
   - `REACT_APP_API_BASE`: Backend URL (default: http://localhost:8000)

## 🚀 Running the Project

1. **Start Backend**
   ```bash
   cd backend
   .venv\Scripts\activate
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start Frontend** (in new terminal)
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access Application**
   - Frontend: http://localhost:5173/
   - Backend API: http://localhost:8000/
   - API Docs: http://localhost:8000/docs

## 📖 Usage

### Graph Exploration
- View the complete O2C process flow
- Click nodes to see details
- Zoom and pan the graph

### Natural Language Queries
Enter queries like:
- "Show me all sales orders"
- "Find overdue invoices"
- "List payments for customer X"
- "Show billing documents without deliveries"

### API Usage
```bash
# Get graph data
curl http://localhost:8000/api/graph

# Chat query
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all sales orders"}'
```

## 🔌 API Endpoints

### Core Endpoints
- `GET /health` - Server health check
- `GET /api/graph` - Full graph data (nodes and links)
- `POST /api/chat` - Natural language query processing

### Request/Response Examples

**POST /api/chat**
```json
{
  "message": "Show me all sales orders with their billing documents"
}
```

**Response**
```json
{
  "answer": "Found sales orders connected to billing documents...",
  "sql": "SELECT * FROM sales_order_headers soh JOIN billing_document_headers bdh ON soh.salesOrder = bdh.salesOrder",
  "sql_success": true,
  "highlighted_nodes": ["SO-1001", "BD-2001"],
  "error": null
}
```

## 🛡️ Security & Guardrails

- **Input Validation**: Pydantic models for all API requests
- **SQL Injection Protection**: Parameterized queries only
- **LLM Guardrails**: Two-layer validation (intent classification + SQL safety)
- **CORS Configuration**: Restricted origins in production

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Manual Testing
- Health check: `GET /health`
- Graph data: `GET /api/graph`
- Chat queries: `POST /api/chat` with sample messages

## 📊 Data Schema

The system includes 16 interconnected O2C tables:
- Sales Order Headers/Items
- Billing Document Headers/Items
- Outbound Delivery Headers
- Journal Entries (AR)
- Payments (AR)
- Business Partners
- Product Descriptions
- Plants
- And more...

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **SQLite**: Lightweight database
- **NetworkX**: Graph construction and analysis
- **Google Gemini API**: LLM for SQL generation
- **Pydantic**: Data validation

### Frontend
- **React 18**: UI framework with hooks
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and dev server
- **react-force-graph-2d**: Graph visualization
- **Zustand**: State management
- **Axios**: HTTP client

### Development
- **Python 3.11+**
- **Node.js 18+**
- **Git**: Version control

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues:
- Check the API documentation at `/docs`
- Review the browser console for frontend errors
- Ensure all prerequisites are installed

---

**Built with ❤️ for demonstrating advanced graph-based data modeling and AI-powered query systems.**