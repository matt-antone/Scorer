# Network API Examples

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [endpoints.md](./endpoints.md): Network API endpoints
- [protocols.md](./protocols.md): Network protocols documentation

## Overview

This document provides practical examples of using the Network API in different scenarios.

## Device Discovery Examples

### 1. Discovering Devices

```javascript
// Client-side JavaScript
async function discoverDevices() {
  const response = await fetch("http://localhost:8080/api/v1/network/devices", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();
  return data.devices;
}

// Example usage
const devices = await discoverDevices();
devices.forEach((device) => {
  console.log(
    `Found device: ${device.name} (${device.type}) at ${device.ip}:${device.port}`
  );
});
```

### 2. Registering a Device

```javascript
// Client-side JavaScript
async function registerDevice(name, type) {
  const response = await fetch(
    "http://localhost:8080/api/v1/network/devices/register",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        type: type,
        ip: getLocalIp(),
        port: 8080,
      }),
    }
  );

  return await response.json();
}

// Example usage
const device = await registerDevice("Player1", "player");
console.log("Device registered:", device.device_id);
```

## Connection Management Examples

### 1. Creating a Connection

```javascript
// Client-side JavaScript
async function createConnection(deviceId) {
  const response = await fetch(
    "http://localhost:8080/api/v1/network/connections",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        device_id: deviceId,
        type: "player",
      }),
    }
  );

  return await response.json();
}

// Example usage
const connection = await createConnection("device123");
console.log("Connection created:", connection.connection_id);
```

### 2. Managing Connections

```javascript
// Client-side JavaScript
async function manageConnections() {
  // Get all connections
  const response = await fetch(
    "http://localhost:8080/api/v1/network/connections",
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  // Close inactive connections
  for (const connection of data.connections) {
    if (connection.status === "inactive") {
      await closeConnection(connection.connection_id);
    }
  }

  return data.connections;
}

async function closeConnection(connectionId) {
  const response = await fetch(
    `http://localhost:8080/api/v1/network/connections/${connectionId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return await response.json();
}

// Example usage
const activeConnections = await manageConnections();
console.log("Active connections:", activeConnections.length);
```

## Network Configuration Examples

### 1. Getting Configuration

```javascript
// Client-side JavaScript
async function getNetworkConfig() {
  const response = await fetch("http://localhost:8080/api/v1/network/config", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return await response.json();
}

// Example usage
const config = await getNetworkConfig();
console.log("Network settings:", config.settings);
```

### 2. Updating Configuration

```javascript
// Client-side JavaScript
async function updateNetworkConfig(settings) {
  const response = await fetch("http://localhost:8080/api/v1/network/config", {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      settings: settings,
    }),
  });

  return await response.json();
}

// Example usage
const newSettings = {
  port: 8080,
  timeout: 30,
  retry_attempts: 3,
  retry_delay: 1000,
};

const result = await updateNetworkConfig(newSettings);
console.log("Config updated:", result.success);
```

## Network Status Examples

### 1. Getting Status

```javascript
// Client-side JavaScript
async function getNetworkStatus() {
  const response = await fetch("http://localhost:8080/api/v1/network/status", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return await response.json();
}

// Example usage
const status = await getNetworkStatus();
console.log("Network status:", status.status);
console.log("Active connections:", status.active_connections);
console.log("Total devices:", status.total_devices);
console.log("Uptime:", status.uptime);
```

### 2. Health Check

```javascript
// Client-side JavaScript
async function checkNetworkHealth() {
  const response = await fetch(
    "http://localhost:8080/api/v1/network/status/health",
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return await response.json();
}

// Example usage
const health = await checkNetworkHealth();
console.log("Network health:", health.status);
console.log("Latency:", health.latency);
console.log("Packet loss:", health.packet_loss);
console.log("Bandwidth:", health.bandwidth);
```

## Error Handling Examples

### 1. Handling API Errors

```javascript
// Client-side JavaScript
async function handleNetworkError(error) {
  if (error.response) {
    const data = await error.response.json();

    switch (error.response.status) {
      case 400:
        console.error("Bad request:", data.message);
        break;
      case 401:
        console.error("Unauthorized:", data.message);
        // Redirect to login
        break;
      case 404:
        console.error("Not found:", data.message);
        break;
      case 500:
        console.error("Server error:", data.message);
        break;
      default:
        console.error("Unknown error:", data.message);
    }
  } else {
    console.error("Network error:", error.message);
  }
}

// Example usage
try {
  await discoverDevices();
} catch (error) {
  await handleNetworkError(error);
}
```

### 2. Retry Logic

```javascript
// Client-side JavaScript
async function retryOperation(operation, maxRetries = 3) {
  let retries = 0;

  while (retries < maxRetries) {
    try {
      return await operation();
    } catch (error) {
      retries++;

      if (retries === maxRetries) {
        throw error;
      }

      // Exponential backoff
      const delay = Math.min(1000 * Math.pow(2, retries), 10000);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
}

// Example usage
try {
  const result = await retryOperation(() => discoverDevices());
  console.log("Operation succeeded:", result);
} catch (error) {
  console.error("Operation failed after retries:", error);
}
```

## Best Practices

1. **Error Handling**

   - Always use try-catch
   - Implement retry logic
   - Handle all error cases
   - Log errors appropriately

2. **Connection Management**

   - Monitor connection health
   - Handle disconnections
   - Implement reconnection
   - Clean up resources

3. **Performance**

   - Optimize network requests
   - Implement caching
   - Use efficient protocols
   - Monitor performance

4. **Security**
   - Validate all input
   - Use secure connections
   - Handle tokens properly
   - Implement rate limiting

# Change Log

## 2024-03-21

- Initial documentation
- Added device discovery examples
- Added connection management examples
- Added network configuration examples
- Added network status examples
- Added error handling examples
- Added best practices
