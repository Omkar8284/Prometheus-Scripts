from prometheus_client import start_http_server, Gauge
import psutil
import time

# Define Prometheus metrics
disk_usage_total = Gauge('disk_usage_total_bytes', 'Total disk usage in bytes', ['mountpoint'])
disk_usage_used = Gauge('disk_usage_used_bytes', 'Used disk space in bytes', ['mountpoint'])
disk_usage_free = Gauge('disk_usage_free_bytes', 'Free disk space in bytes', ['mountpoint'])
disk_usage_percent = Gauge('disk_usage_percent', 'Percentage of disk space used', ['mountpoint'])

def collect_disk_usage():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage_total.labels(mountpoint=partition.mountpoint).set(usage.total)
            disk_usage_used.labels(mountpoint=partition.mountpoint).set(usage.used)
            disk_usage_free.labels(mountpoint=partition.mountpoint).set(usage.free)
            disk_usage_percent.labels(mountpoint=partition.mountpoint).set(usage.percent)
            print(f"Metrics updated for {partition.mountpoint}")
        except Exception as e:
            print(f"Error collecting disk usage for {partition.mountpoint}: {e}")

def monitor_storage():
    while True:
        collect_disk_usage()
        time.sleep(60)  # Collect data every 60 seconds

if __name__ == '__main__':
    try:
        start_http_server(8005)  # Start Prometheus server on port 8005
        print("Prometheus server started on port 8005")
        monitor_storage()
    except Exception as e:
        print(f"Error starting Prometheus server or monitoring storage: {e}")
