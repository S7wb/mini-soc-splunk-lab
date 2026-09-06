# n8n Installation

## Overview

n8n was deployed inside the Mini SOC lab to provide a security automation and orchestration layer between Splunk alerts and external notification channels.

The n8n instance runs as a Docker container on the Splunk Server and uses persistent Docker storage so that workflows and configuration remain available after container or server restarts.

## Deployment Architecture

```text
Mini SOC Lab
     |
     v
Splunk Server
     |
     v
Docker Engine
     |
     v
n8n Container
     |
     v
Port 5678
     |
     v
n8n Web Interface
```

## Deployment Host

| Setting | Value |
|---|---|
| Host | Splunk Server |
| Platform | Ubuntu Server |
| Container Platform | Docker |
| n8n Container Name | `n8n` |
| n8n Port | `5678` |
| Persistent Volume | `n8n_data` |
| Time Zone | `Asia/Riyadh` |
| Restart Policy | `unless-stopped` |
| Lab IP | `192.168.56.10` |

## Docker Verification

Docker was installed and verified before deploying n8n.

The Docker service was confirmed to be running successfully.

A basic Docker test was also performed using:

```bash
docker run hello-world
```

This confirmed that the Docker Engine was able to download and execute containers successfully.

## Persistent Storage

A dedicated Docker volume was created for n8n:

```bash
docker volume create n8n_data
```

The volume stores n8n configuration and workflow data outside the container.

This prevents workflow data from being lost if the n8n container is recreated.

The persistent data is mounted to:

```text
/home/node/.n8n
```

inside the container.

## n8n Container Deployment

The n8n container was deployed using the following command:

```bash
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -e TZ=Asia/Riyadh \
  -e GENERIC_TIMEZONE=Asia/Riyadh \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

### Configuration Explanation

| Parameter | Purpose |
|---|---|
| `-d` | Runs the container in detached mode |
| `--name n8n` | Assigns the container name `n8n` |
| `--restart unless-stopped` | Automatically restarts n8n after server or Docker restarts |
| `-p 5678:5678` | Exposes the n8n web interface on TCP port 5678 |
| `TZ=Asia/Riyadh` | Configures the container time zone |
| `GENERIC_TIMEZONE=Asia/Riyadh` | Configures the workflow time zone |
| `n8n_data:/home/node/.n8n` | Provides persistent storage for n8n |
| `docker.n8n.io/n8nio/n8n` | Official n8n Docker image |

## Container Verification

After deployment, the container status was verified using:

```bash
docker ps
```

The container was shown as running with port mapping similar to:

```text
0.0.0.0:5678->5678/tcp
```

This confirmed that the n8n service was active and listening on TCP port `5678`.

The container can also be checked using:

```bash
docker ps --filter name=n8n
```

## Log Verification

Container logs can be reviewed with:

```bash
docker logs n8n
```

For a shorter log view:

```bash
docker logs --tail 50 n8n
```

The logs were reviewed after deployment to verify that the n8n service started successfully.

A Python runner-related warning was also observed during log review.

This warning did not prevent the implemented SOC automation workflow from operating because the workflow does not depend on Python code execution.

## Web Interface Access

After the container started successfully, the n8n interface became accessible from the lab network at:

```text
http://192.168.56.10:5678
```

Successful access to the n8n web interface confirmed:

- The Docker container was running.
- Port `5678` was exposed correctly.
- The Splunk Server was reachable from the management system.
- The n8n application was operational.

## Automatic Restart

The container was deployed using:

```text
--restart unless-stopped
```

This ensures that n8n automatically starts again after:

- Docker service restarts.
- Splunk Server reboots.
- Unexpected container termination.

The container will remain stopped only when it is manually stopped.

## Useful Management Commands

Check container status:

```bash
docker ps
```

View n8n logs:

```bash
docker logs --tail 50 n8n
```

Restart n8n:

```bash
docker restart n8n
```

Stop n8n:

```bash
docker stop n8n
```

Start n8n:

```bash
docker start n8n
```

Inspect the persistent volume:

```bash
docker volume inspect n8n_data
```

## Security Considerations

The n8n instance is deployed inside the isolated Mini SOC lab environment.

The following security practices are followed:

- n8n is not intentionally exposed directly to the public Internet.
- Credentials are stored using the n8n credential system.
- Secrets and authentication tokens are not committed to GitHub.
- Telegram bot tokens are excluded from screenshots and exported documentation.
- Passwords and session information are excluded from the repository.
- The lab uses private internal addressing for communication between systems.

## Validation

The n8n deployment was validated successfully.

| Test | Result |
|---|---|
| Docker Engine operational | Passed |
| Persistent volume created | Passed |
| n8n container started | Passed |
| Container remained running | Passed |
| TCP port 5678 exposed | Passed |
| n8n web interface accessible | Passed |
| Persistent storage configured | Passed |
| Automatic restart policy configured | Passed |

## Result

n8n was successfully deployed as the automation layer for the Mini SOC lab.

The environment was ready for the next integration stage:

```text
Splunk Alert
     |
     v
Webhook
     |
     v
n8n
```

The next step was to configure Splunk to send security alert data to the n8n webhook endpoint.
