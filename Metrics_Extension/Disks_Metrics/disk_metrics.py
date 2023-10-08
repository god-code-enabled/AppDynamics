import psutil
import requests
import subprocess
import json
import time

APPDYNAMICS_MACHINE_AGENT_HOST = 'http://localhost:8293'

def bytes_to_mb(value_in_bytes):
    return round(value_in_bytes / (1024 * 1024))

def get_mountpoints_from_df():
    result = subprocess.run(['df'], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split('\n')[1:]  # Skip header line
    mountpoints = [line.split()[-1] for line in lines]  # Last column is the mountpoint
    return mountpoints

def get_disk_metrics():
    metrics = []

    # Get metrics for each disk partition
    mountpoints = get_mountpoints_from_df()
    for mountpoint in mountpoints:
        try:
            usage = psutil.disk_usage(mountpoint)
            total_space_mb = bytes_to_mb(usage.total)
            available_space_mb = bytes_to_mb(usage.free)
            used_space_mb = total_space_mb - available_space_mb  # Calculate used space in MB

            metrics.append({
                "metricName": f"Custom Metrics|Disks|{mountpoint}|Total Space (MB)",
                "aggregatorType": "AVERAGE",
                "value": total_space_mb
            })
            metrics.append({
                "metricName": f"Custom Metrics|Disks|{mountpoint}|Available Space (MB)",
                "aggregatorType": "AVERAGE",
                "value": available_space_mb
            })
            metrics.append({
                "metricName": f"Custom Metrics|Disks|{mountpoint}|Used Space (MB)",
                "aggregatorType": "AVERAGE",
                "value": used_space_mb
            })
            metrics.append({
                "metricName": f"Custom Metrics|Disks|{mountpoint}|Used Percentage",
                "aggregatorType": "AVERAGE",
                "value": round(usage.percent)
            })
        except Exception as e:
            print(f"Could not get metrics for {mountpoint}: {e}")

    return metrics

def send_to_appdynamics(metrics):
    headers = {"Content-Type": "application/json"}
    response = requests.post(f'{APPDYNAMICS_MACHINE_AGENT_HOST}/api/v1/metrics',
                             headers=headers,
                             json=metrics)
    print(f'Status code: {response.status_code}')
    print(f'Content: {response.content}')

if __name__ == "__main__":
    while True:
        disk_metrics = get_disk_metrics()
        send_to_appdynamics(disk_metrics)
        time.sleep(60)  # Send metrics every 60 seconds
