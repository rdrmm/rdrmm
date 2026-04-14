from flask import Flask, render_template, jsonify, request
import psutil
import time
from collections import defaultdict

app = Flask(__name__)

# In-memory storage for agents
agents = defaultdict(dict)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/metrics')
def get_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    metrics = {
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'memory_used': memory.used,
        'memory_total': memory.total,
        'disk_percent': disk.percent,
        'disk_used': disk.used,
        'disk_total': disk.total,
        'timestamp': time.time()
    }
    return jsonify(metrics)

@app.route('/api/alerts')
def get_alerts():
    # Simple alerting: if CPU > 80% or memory > 80%
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    alerts = []
    if cpu > 80:
        alerts.append({'type': 'cpu', 'message': f'High CPU usage: {cpu}%'})
    if mem > 80:
        alerts.append({'type': 'memory', 'message': f'High memory usage: {mem}%'})
    return jsonify(alerts)

# Agent registration
@app.route('/api/agents/register', methods=['POST'])
def register_agent():
    data = request.json
    agent_id = data.get('agent_id')
    if not agent_id:
        return jsonify({'error': 'agent_id required'}), 400
    agents[agent_id]['last_seen'] = time.time()
    agents[agent_id]['instructions'] = agents[agent_id].get('instructions', [])
    return jsonify({'status': 'registered'})

# Agent reports metrics
@app.route('/api/agents/<agent_id>/metrics', methods=['POST'])
def report_metrics(agent_id):
    data = request.json
    agents[agent_id]['metrics'] = data
    agents[agent_id]['last_seen'] = time.time()
    return jsonify({'status': 'received'})

# Agent gets instructions
@app.route('/api/agents/<agent_id>/instructions', methods=['GET'])
def get_instructions(agent_id):
    instructions = agents[agent_id].get('instructions', [])
    # Clear instructions after sending
    agents[agent_id]['instructions'] = []
    return jsonify(instructions)

# Admin sets instructions (for demo)
@app.route('/api/agents/<agent_id>/instructions', methods=['POST'])
def set_instructions(agent_id):
    data = request.json
    instruction = data.get('instruction')
    if instruction:
        agents[agent_id]['instructions'].append(instruction)
    return jsonify({'status': 'added'})

# Get all agents
@app.route('/api/agents')
def get_agents():
    result = {}
    for agent_id, data in agents.items():
        result[agent_id] = {
            'last_seen': data.get('last_seen'),
            'metrics': data.get('metrics'),
            'instructions_pending': len(data.get('instructions', []))
        }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)