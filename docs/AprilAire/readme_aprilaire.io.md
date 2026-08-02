# AprilAire Cloud REST interface (`aprilaire.io`)

This document is a reverse-engineered reference derived from `custom_components/aprilaire_cloud` (Home Assistant). It documents the REST interface and behaviors observed in that reference integration; this repository's implementation may only cover a subset. It is **not** an official AprilAire API specification.

## Scope

The integration talks to two HTTPS origins:

| Host | Purpose |
| --- | --- |
| `https://account.aprilaire.io` | account/user lookup |
| `https://device.aprilaire.io` | hierarchy, device status, device settings, writes |

WebSocket traffic is handled separately via `wss://socket.aprilaire.io/` and is out of scope for this file.

## Authentication

REST calls use an Amazon Cognito ID token in the `Authorization` header:

```http
Authorization: Bearer <id_token>
Content-Type: application/json
```

The integration acquires tokens through Cognito SRP login using:

- region: `us-west-2`
- user pool id: `us-west-2_skfkpmVv6`
- client id: `3aiakr6qdoqtajv7qgtapecerg`

Observed token lifecycle from the integration:

1. Full login returns `id_token`, `access_token`, and `refresh_token`.
2. The ID token is reused until it is within 5 minutes of expiry.
3. The integration prefers refresh-token renewal when possible.
4. A 401 on a REST request forces one token refresh and retries the request once.
5. If the retry also gets a 401, the integration raises an authentication error.

## Common transport behavior

- Request timeout: **20 seconds**
- Expected success body: **JSON object**
- Empty success body is treated as `{}`.
- JSON arrays or malformed JSON are treated as API errors.
- 429 handling:
  - `Retry-After` is clamped to **1..300** seconds
  - invalid/missing `Retry-After` falls back to **60** seconds
  - write requests (`PATCH`) auto-retry once only when `Retry-After <= 2` seconds
- Error logging is sanitized to avoid leaking URLs, response prose, or tokens.

## Endpoints in active use

### 1. Get current user

```http
GET https://account.aprilaire.io/user
```

Used during config flow and coordinator startup.

Observed fields consumed by the integration:

- `userId` (required)
- `email` (optional fallback to configured username)

Minimal response shape:

```json
{
  "userId": "123456",
  "email": "user@example.com"
}
```

### 2. Get device hierarchy

```http
GET https://device.aprilaire.io/hierarchy
```

This is the discovery document for locations, rooms, and device references.

Observed fields consumed by the integration:

```json
{
  "locations": [
    {
      "locationId": "location-1",
      "name": "Home",
      "timeZone": "America/New_York",
      "rooms": [
        {
          "name": "Basement",
          "devices": [
            {
              "deviceId": "device-1",
              "access": "manage",
              "zone": 1
            }
          ]
        }
      ]
    }
  ]
}
```

Notes:

- `access` governs whether writes are allowed; the integration expects `manage` for writable commands.
- `zone` is used for thermostat zoning (`1 -> PZ1`, `2 -> SZ2`, `3 -> SZ3`).

### 3. Get full device status

```http
GET https://device.aprilaire.io/{device_id}/status
```

This is a full device-level status document. The integration stores it as `device_status`.

Observed behavior:

- treated as a full replacement payload for the REST status section
- timestamp ordering uses `asOf` when present

### 4. Get full device settings

```http
GET https://device.aprilaire.io/{device_id}/settings
```

This is the authoritative writable settings snapshot. The integration stores it as `device_settings`.

Observed behavior:

- treated as a full replacement payload for confirmed settings
- timestamp ordering uses `asOf` when present
- used after writes for reconciliation/confirmation

### 5. Get profile-specific status documents

```http
GET https://device.aprilaire.io/{device_id}/status/{status}
```

The integration uses this route for profile-owned supplemental status payloads.

Observed `status` values:

| Status path | Stored key | Used for |
| --- | --- | --- |
| `dehumidifier` | `dehumidifier` | standalone dehumidifier status |
| `thermostat/PZ1` | `thermostatPZ1` | thermostat primary zone status |
| `thermostat/SZ2` | `thermostatSZ2` | thermostat secondary zone 2 status |
| `thermostat/SZ3` | `thermostatSZ3` | thermostat secondary zone 3 status |
| `humidifier` | `iaq_humidifier` | thermostat-attached humidifier status |
| `dehumidifier` | `iaq_dehumidifier` | thermostat IAQ dehumidifier status |
| `freshair` | `iaq_freshair` | fresh-air accessory status |
| `aircleaning` | `iaq_aircleaning` | air-cleaning accessory status |

Notes:

- `dehumidifier` is used in two contexts:
  - as the standalone dehumidifier profile status key
  - as the thermostat IAQ accessory endpoint
- the endpoint path is the same; interpretation depends on the recognized device profile

## Writes

### Patch device settings

```http
PATCH https://device.aprilaire.io/{device_id}/settings
Content-Type: application/json
Authorization: Bearer <id_token>
```

The integration sends partial nested JSON payloads matching the device settings schema.

#### Standalone dehumidifier payloads

Power:

```json
{
  "dehumidifier": {
    "mode": "on"
  }
}
```

Target humidity:

```json
{
  "dehumidifier": {
    "humiditySetpoint": 50
  }
}
```

High humidity alert:

```json
{
  "dehumidifier": {
    "alertLimits": {
      "highHum": 60
    }
  }
}
```

#### Thermostat-attached humidifier payloads

Power:

```json
{
  "humidifier": {
    "mode": "off"
  }
}
```

Target humidity:

```json
{
  "humidifier": {
    "humiditySetpoint": 35
  }
}
```

#### Thermostat zone payloads

Zone payloads are wrapped by zone settings key:

- `thermostatPZ1`
- `thermostatSZ2`
- `thermostatSZ3`

The integration mirrors the key style already present in the device's settings document.

Examples:

String enum style:

```json
{
  "thermostatPZ1": {
    "mode": "heat"
  }
}
```

Numeric enum style:

```json
{
  "thermostatPZ1": {
    "ModeId": 2
  }
}
```

Observed writable thermostat enums:

| Setting | String key | Numeric key | Values |
| --- | --- | --- | --- |
| mode | `mode` | `ModeId` | `off`, `heat`, `cool`, `auto`, `emergency-heat` |
| fan | `fan` | `FanId` | `auto`, `on`, `circulate` |
| hold | `holdType` | `HoldType` | `none`, `temporary`, `permanent`, `vacation` |

Special case:

- model `8920W_GS` uses string fan value `circ` when the normalized command value is `circulate`

### Not currently written by the integration

Thermostat heat/cool setpoint writes are **not** emitted by the current integration because the PATCH contract is treated as unconfirmed.

## Response/data conventions inferred by the integration

These conventions are relied on by the state reducer and profile logic:

- payloads may include `asOf` timestamps for ordering
- settings documents are nested objects merged by key path
- profile status documents are stored independently by logical key
- thermostat zones are identified by:
  - hierarchy `zone`
  - settings keys `thermostatPZ1`, `thermostatSZ2`, `thermostatSZ3`
- thermostat accessory status endpoints are only fetched when installed equipment is inferred from setup/settings

## Practical request sequence used by the integration

Startup/config validation sequence:

1. Cognito authenticate
2. `GET /user`
3. `GET /hierarchy`
4. For each device needing hydration:
   1. `GET /{device_id}/status`
   2. `GET /{device_id}/settings`
   3. zero or more `GET /{device_id}/status/{status}`

Write sequence:

1. `PATCH /{device_id}/settings` with a partial nested payload
2. accept any 2xx response body if present
3. reconcile against later settings/status refreshes

