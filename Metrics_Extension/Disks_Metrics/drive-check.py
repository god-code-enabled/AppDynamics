import psutil
import subprocess
import time

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
            used_space_mb = total_space_mb - available_space_mb  # Calculating used space in MB

            metrics.append({
                "metricName": f"Custom Metrics|Disk|{mountpoint}|Total Space (MB)",
                "value": total_space_mb
            })
            metrics.append({
                "metricName": f"Custom Metrics|Disk|{mountpoint}|Available Space (MB)",
                "value": available_space_mb
            })
            metrics.append({
                "metricName": f"Custom Metrics|Disk|{mountpoint}|Used Space (MB)",
                "value": used_space_mb
            })
            metrics.append({
                "metricName": f"Custom Metrics|Disk|{mountpoint}|Used Percentage",
                "value": round(usage.percent)
            })
        except Exception as e:
            print(f"Could not get metrics for {mountpoint}: {e}")

    return metrics

def print_metrics(metrics):
    for metric in metrics:
        print(f'{metric["metricName"]}: {metric["value"]}')

if __name__ == "__main__":
    while True:
        disk_metrics = get_disk_metrics()
        print_metrics(disk_metrics)
        time.sleep(60)  # Print metrics every 60 seconds
