# API Documentation

Complete API reference for AIKAILNOV4.

## Base URL

```
http://localhost:8080/api/v1
```

## Authentication

All API endpoints require authentication using JWT tokens.

### Get Access Token

**Endpoint:** `POST /api/v1/auth/token`

**Request Body:**
```json
{
  "username": "admin",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Usage:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/api/v1/scan
```

## Endpoints

### Health Check

Check API server health status.

**Endpoint:** `GET /api/v1/health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

---

### Create Scan

Initiate a new security scan.

**Endpoint:** `POST /api/v1/scan`

**Request Body:**
```json
{
  "target": "192.168.1.100",
  "ports": "1-1000",
  "scan_type": "comprehensive",
  "ai_analysis": true
}
```

**Parameters:**
- `target` (required): IP address, hostname, or network range
- `ports` (optional): Port range (default: "1-1000")
- `scan_type` (optional): "quick", "comprehensive", or "deep" (default: "comprehensive")
- `ai_analysis` (optional): Enable AI analysis (default: true)

**Response:**
```json
{
  "scan_id": "abc123",
  "status": "initiated",
  "target": "192.168.1.100",
  "started_at": "2025-01-01T00:00:00Z"
}
```

---

### Get Scan Status

Retrieve the status of a scan.

**Endpoint:** `GET /api/v1/scan/{scan_id}`

**Response:**
```json
{
  "scan_id": "abc123",
  "status": "completed",
  "progress": 100,
  "target": "192.168.1.100",
  "started_at": "2025-01-01T00:00:00Z",
  "completed_at": "2025-01-01T00:05:30Z"
}
```

**Status Values:**
- `initiated`: Scan has been queued
- `running`: Scan is in progress
- `completed`: Scan finished successfully
- `failed`: Scan encountered an error

---

### Get Scan Results

Retrieve detailed scan results.

**Endpoint:** `GET /api/v1/results/{scan_id}`

**Response:**
```json
{
  "scan_id": "abc123",
  "target": "192.168.1.100",
  "scan_time": "2025-01-01T00:00:00Z",
  "hosts": [
    {
      "ip": "192.168.1.100",
      "hostname": "server.local",
      "state": "up",
      "open_ports": [
        {
          "port": 80,
          "protocol": "tcp",
          "service": "http",
          "version": "Apache 2.4.41"
        }
      ]
    }
  ],
  "total_open_ports": 5,
  "vulnerabilities": [
    {
      "severity": "medium",
      "description": "HTTP service detected",
      "host": "192.168.1.100",
      "port": 80
    }
  ]
}
```

---

### AI Analysis

Request AI analysis on scan results.

**Endpoint:** `POST /api/v1/analyze`

**Request Body:**
```json
{
  "scan_id": "abc123",
  "mode": "advanced"
}
```

**Parameters:**
- `scan_id` (required): ID of the scan to analyze
- `mode` (optional): "basic", "advanced", or "full" (default: "basic")

**Response:**
```json
{
  "analysis_id": "xyz789",
  "scan_id": "abc123",
  "risk_score": 6.5,
  "risk_level": "medium",
  "threat_categories": [
    "unencrypted_protocols",
    "exposed_database"
  ],
  "recommendations": [
    {
      "priority": "high",
      "title": "Disable Telnet Service",
      "description": "Replace with SSH"
    }
  ],
  "insights": [
    "Detected 3 potential vulnerabilities",
    "Overall risk level: MEDIUM"
  ]
}
```

---

### List Modules

Get available security modules.

**Endpoint:** `GET /api/v1/modules`

**Response:**
```json
{
  "modules": [
    {
      "name": "port_scanner",
      "description": "Advanced port scanning",
      "status": "active",
      "version": "1.0.0"
    },
    {
      "name": "web_scanner",
      "description": "Web application testing",
      "status": "active",
      "version": "1.0.0"
    }
  ]
}
```

---

### Execute Module

Run a specific security module.

**Endpoint:** `POST /api/v1/modules/{module_name}/run`

**Request Body:**
```json
{
  "target": "192.168.1.100",
  "parameters": {
    "depth": 3,
    "aggressive": false
  }
}
```

**Response:**
```json
{
  "execution_id": "def456",
  "module": "web_scanner",
  "status": "running",
  "started_at": "2025-01-01T00:00:00Z"
}
```

---

### Generate Report

Generate a report from scan results.

**Endpoint:** `POST /api/v1/reports`

**Request Body:**
```json
{
  "scan_id": "abc123",
  "format": "html",
  "sections": [
    "executive_summary",
    "findings",
    "recommendations"
  ]
}
```

**Parameters:**
- `scan_id` (required): Scan to generate report for
- `format` (optional): "html", "pdf", "json", or "xml" (default: "html")
- `sections` (optional): Report sections to include

**Response:**
```json
{
  "report_id": "rep789",
  "scan_id": "abc123",
  "format": "html",
  "download_url": "/api/v1/reports/rep789/download",
  "generated_at": "2025-01-01T00:00:00Z"
}
```

---

### Download Report

Download a generated report.

**Endpoint:** `GET /api/v1/reports/{report_id}/download`

**Response:** Binary file (HTML, PDF, etc.)

---

## Error Responses

All errors follow a consistent format:

```json
{
  "error": {
    "code": "INVALID_TARGET",
    "message": "The specified target is invalid",
    "details": {
      "target": "invalid_host"
    },
    "timestamp": "2025-01-01T00:00:00Z"
  }
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created
- `400 Bad Request`: Invalid request
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Codes

- `INVALID_TARGET`: Target specification is invalid
- `SCAN_NOT_FOUND`: Scan ID does not exist
- `INVALID_PARAMETERS`: Request parameters are invalid
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `AUTHENTICATION_REQUIRED`: Missing or invalid token
- `MODULE_NOT_FOUND`: Specified module does not exist
- `INSUFFICIENT_PERMISSIONS`: User lacks required permissions

## Rate Limiting

API requests are rate-limited to prevent abuse:

- **Default**: 100 requests per hour
- **Authenticated**: 1000 requests per hour
- **Premium**: 10000 requests per hour

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Results per page (default: 20, max: 100)

**Response Headers:**
```
X-Total-Count: 150
X-Page: 1
X-Per-Page: 20
Link: </api/v1/scans?page=2>; rel="next"
```

## Webhooks

Configure webhooks to receive notifications:

**Endpoint:** `POST /api/v1/webhooks`

**Request Body:**
```json
{
  "url": "https://your-server.com/webhook",
  "events": ["scan.completed", "vulnerability.found"],
  "secret": "webhook_secret"
}
```

**Webhook Payload:**
```json
{
  "event": "scan.completed",
  "scan_id": "abc123",
  "timestamp": "2025-01-01T00:00:00Z",
  "data": {}
}
```

## Code Examples

### Python

```python
import requests

# Authenticate
response = requests.post(
    'http://localhost:8080/api/v1/auth/token',
    json={'username': 'admin', 'password': 'password'}
)
token = response.json()['access_token']

# Create scan
headers = {'Authorization': f'Bearer {token}'}
response = requests.post(
    'http://localhost:8080/api/v1/scan',
    headers=headers,
    json={'target': '192.168.1.100', 'ai_analysis': True}
)
scan_id = response.json()['scan_id']

# Get results
response = requests.get(
    f'http://localhost:8080/api/v1/results/{scan_id}',
    headers=headers
)
results = response.json()
```

### JavaScript

```javascript
// Authenticate
const authResponse = await fetch('http://localhost:8080/api/v1/auth/token', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username: 'admin', password: 'password'})
});
const {access_token} = await authResponse.json();

// Create scan
const scanResponse = await fetch('http://localhost:8080/api/v1/scan', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({target: '192.168.1.100', ai_analysis: true})
});
const {scan_id} = await scanResponse.json();

// Get results
const resultsResponse = await fetch(
  `http://localhost:8080/api/v1/results/${scan_id}`,
  {headers: {'Authorization': `Bearer ${access_token}`}}
);
const results = await resultsResponse.json();
```

### cURL

```bash
# Authenticate
TOKEN=$(curl -X POST http://localhost:8080/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}' \
  | jq -r '.access_token')

# Create scan
SCAN_ID=$(curl -X POST http://localhost:8080/api/v1/scan \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target":"192.168.1.100","ai_analysis":true}' \
  | jq -r '.scan_id')

# Get results
curl -X GET http://localhost:8080/api/v1/results/$SCAN_ID \
  -H "Authorization: Bearer $TOKEN"
```

---

For more information, visit the [main documentation](../README.md).
