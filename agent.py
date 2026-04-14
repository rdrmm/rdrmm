import requests
import psutil
import time
import socket
import json

# Configuration
SERVER_URL = 'http://localhost:5000'  # Change to your server URL
AGENT_ID = socket.gethostname()  # Use hostname as agent ID

def get_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'memory_used': memory.used,
        'memory_total': memory.total,
        'disk_percent': disk.percent,
        'disk_used': disk.used,
        'disk_total': disk.total,
        'timestamp': time.time()
    }

def register_agent():
    try:
        response = requests.post(f'{SERVER_URL}/api/agents/register', json={'agent_id': AGENT_ID})
        if response.status_code == 200:
            print("Agent registered successfully")
        else:
            print(f"Registration failed: {response.text}")
    except Exception as e:
        print(f"Registration error: {e}")

def send_metrics():
    try:
        metrics = get_metrics()
        response = requests.post(f'{SERVER_URL}/api/agents/{AGENT_ID}/metrics', json=metrics)
        if response.status_code == 200:
            print("Metrics sent successfully")
        else:
            print(f"Failed to send metrics: {response.text}")
    except Exception as e:
        print(f"Error sending metrics: {e}")

def get_instructions():
    try:
        response = requests.get(f'{SERVER_URL}/api/agents/{AGENT_ID}/instructions')
        if response.status_code == 200:
            instructions = response.json()
            if instructions:
                print(f"Received instructions: {instructions}")
                # Here you would execute the instructions
                for instruction in instructions:
                    execute_instruction(instruction)
            else:
                print("No instructions")
        else:
            print(f"Failed to get instructions: {response.text}")
    except Exception as e:
        print(f"Error getting instructions: {e}")

def execute_instruction(instruction):
    # Simple instruction execution - in real RMM, this would be more sophisticated
    print(f"Executing: {instruction}")
    if instruction == 'restart':
        print("Simulating restart...")
    elif instruction.startswith('run:'):
        cmd = instruction[4:]
        print(f"Would run command: {cmd}")
    else:
        print(f"Unknown instruction: {instruction}")

if __name__ == '__main__':
    print(f"Starting agent {AGENT_ID}")
    register_agent()
    while True:
        send_metrics()
        get_instructions()
        time.sleep(30)  # Report every 30 seconds