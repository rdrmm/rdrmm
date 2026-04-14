# RDRMM - Remote Device Remote Monitoring and Management

A simple Python-based remote monitoring and management system built with Flask.

## Features

- Real-time system monitoring (CPU, memory, disk usage)
- Web dashboard for viewing metrics
- Basic alerting system
- Remote agent support for monitoring multiple hosts
- Instruction system for remote management

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python app.py
   ```

3. Open your browser to `http://localhost:5000`

## Usage

### Server
The dashboard displays local system metrics and connected remote agents.

### Agents
To deploy agents on remote machines:

1. Copy `agent.py` to the remote machine
2. Update `SERVER_URL` in `agent.py` to point to your server
3. Install dependencies: `pip install requests psutil`
4. Run the agent: `python agent.py`

Agents will automatically register with the server and start reporting metrics every 30 seconds.

### API Endpoints

- `GET /api/metrics` - Local system metrics
- `GET /api/alerts` - Local alerts
- `GET /api/agents` - List all agents
- `POST /api/agents/register` - Register an agent
- `POST /api/agents/{id}/metrics` - Agent reports metrics
- `GET /api/agents/{id}/instructions` - Agent fetches instructions
- `POST /api/agents/{id}/instructions` - Set instructions for agent
