# Copilot Supervisor Bridge

This is a custom Home Assistant add-on scaffold for controlled Supervisor
operations. It declares `hassio_api: true`, but it does not expose the
Supervisor token to SSH or to clients.

## Installation

The first installation must be performed manually from Home Assistant because
the current SSH add-on does not have Supervisor authorization:

1. Add this repository as a local add-on repository, or package this directory
   as a custom add-on repository.
2. Install **Copilot Supervisor Bridge**.
3. Set a long random `access_token` in the add-on configuration.
4. Enable only the operation flags that are required.
5. Start the add-on and enable **Start on boot**.

The API is exposed on port `8126` and requires:

```text
Authorization: Bearer <configured-bridge-token>
```

The Supervisor token is held inside the add-on only. Do not paste either token
into chat, source control, or workspace files.

## Current endpoints

- `GET /health`
- `GET /apps`
- `GET /logs`
- `POST /core/restart`

Backup/restore and HACS management require additional implementation and
explicit endpoint design before being enabled in production. They are not
implemented by this scaffold merely because the corresponding flags exist.
