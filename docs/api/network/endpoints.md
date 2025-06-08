# Network API Endpoints

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [protocols.md](./protocols.md): Network protocols documentation
- [examples.md](./examples.md): Usage examples

## Overview

The Network API provides endpoints for managing network connections, device discovery, and network configuration. It handles the communication between the Kivy app, client applications, and the state server.

## Base URL

```
http://{host}:{port}/api/v1/network
```

## Authentication

All endpoints require authentication using a Bearer token:

```
Authorization: Bearer {token}
```

## Endpoints

### Device Discovery

#### GET /devices

Get all available devices on the network.

**Response:**

```json
{
  "devices": [
    {
      "device_id": "string",
      "name": "string",
      "type": "string",
      "status": "string",
      "ip": "string",
      "port": number
    }
  ],
  "timestamp": "ISO8601"
}
```

#### POST /devices/register

Register a new device.

**Request Body:**

```json
{
  "name": "string",
  "type": "string",
  "ip": "string",
  "port": number
}
```

**Response:**

```json
{
  "device_id": "string",
  "name": "string",
  "type": "string",
  "status": "string",
  "ip": "string",
  "port": number,
  "timestamp": "ISO8601"
}
```

### Connection Management

#### GET /connections

Get all active connections.

**Response:**

```json
{
  "connections": [
    {
      "connection_id": "string",
      "device_id": "string",
      "status": "string",
      "type": "string",
      "started_at": "ISO8601"
    }
  ],
  "timestamp": "ISO8601"
}
```

#### POST /connections

Create a new connection.

**Request Body:**

```json
{
  "device_id": "string",
  "type": "string"
}
```

**Response:**

```json
{
  "connection_id": "string",
  "device_id": "string",
  "status": "string",
  "type": "string",
  "started_at": "ISO8601",
  "timestamp": "ISO8601"
}
```

#### DELETE /connections/{connection_id}

Close a connection.

**Parameters:**

- `connection_id` (path): Unique connection identifier

**Response:**

```json
{
  "success": boolean,
  "message": "string",
  "timestamp": "ISO8601"
}
```

### Network Configuration

#### GET /config

Get network configuration.

**Response:**

```json
{
  "settings": {
    "port": number,
    "timeout": number,
    "retry_attempts": number,
    "retry_delay": number
  },
  "timestamp": "ISO8601"
}
```

#### PUT /config

Update network configuration.

**Request Body:**

```json
{
  "settings": {
    "port": number,
    "timeout": number,
    "retry_attempts": number,
    "retry_delay": number
  }
}
```

**Response:**

```json
{
  "success": boolean,
  "message": "string",
  "timestamp": "ISO8601"
}
```

### Network Status

#### GET /status

Get network status.

**Response:**

```json
{
  "status": "string",
  "active_connections": number,
  "total_devices": number,
  "uptime": number,
  "timestamp": "ISO8601"
}
```

#### GET /status/health

Get network health status.

**Response:**

```json
{
  "status": "string",
  "latency": number,
  "packet_loss": number,
  "bandwidth": number,
  "timestamp": "ISO8601"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

```json
{
  "error": "string",
  "message": "string",
  "timestamp": "ISO8601"
}
```

### 401 Unauthorized

```json
{
  "error": "string",
  "message": "string",
  "timestamp": "ISO8601"
}
```

### 404 Not Found

```json
{
  "error": "string",
  "message": "string",
  "timestamp": "ISO8601"
}
```

### 500 Internal Server Error

```json
{
  "error": "string",
  "message": "string",
  "timestamp": "ISO8601"
}
```

## Rate Limits

- 100 requests per minute per IP
- 1000 requests per hour per IP
- Burst limit: 10 requests per second

## Security

- All endpoints require HTTPS in production
- Tokens expire after 24 hours
- Rate limiting per IP
- Input validation required

## Examples

See [examples.md](./examples.md) for detailed usage examples.

# Change Log

## 2024-03-21

- Initial documentation
- Added device discovery endpoints
- Added connection management endpoints
- Added network configuration endpoints
- Added network status endpoints
- Added error responses
- Added rate limits
