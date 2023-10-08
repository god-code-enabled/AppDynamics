import psutil
import requests
import json
import time
# replace with the Machine Agent address
APPDYNAMICS_MACHINE_AGENT_HOST = 'http://localhost:8293'

def get_cpu_usage():
    time.sleep(1)  # Wait a second to let the CPU accumulate usage stats
    cpu_percentages = psutil.cpu_percent(interval=None, percpu=True)
    return cpu_percentages

def generate_metrics(cpu_percentages):
    metrics = []
    for i, percentage in enumerate(cpu_percentages):
        metric = {
            "metricName": f"Custom Metrics|Hardware Resources|CPU|Usage|Core {i + 1}",
            "aggregatorType": "AVERAGE",
            "value": percentage
        }
        metrics.append(metric)
    return metrics

def send_to_appdynamics(metrics):
    headers = {"Content-Type": "application/json"}
    response = requests.post(f'{APPDYNAMICS_MACHINE_AGENT_HOST}/api/v1/metrics',
                             headers=headers,
                             json=metrics)
    print(f'Status code: {response.status_code}')
    print(f'Content: {response.content}')

cpu_percentages = get_cpu_usage()
metrics = generate_metrics(cpu_percentages)
send_to_appdynamics(metrics)