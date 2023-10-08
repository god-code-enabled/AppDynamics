import psutil
import time

def print_metrics(metrics):
    for metric in metrics:
        print(f'{metric["metricName"]}: {metric["value"]}')

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

# Main function to test the script
if __name__ == "__main__":
    while True:
        cpu_percentages = get_cpu_usage()
        metrics = generate_metrics(cpu_percentages)
        print_metrics(metrics)
        time.sleep(60)  # Print metrics every 60 seconds