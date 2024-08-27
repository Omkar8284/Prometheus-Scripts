from prometheus_client import start_http_server, Gauge
import time
import subprocess

def get_wifi_details():
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID,SIGNAL,BSSID,DEVICE', 'device', 'wifi'],
                                stdout=subprocess.PIPE, universal_newlines=True)
        wifi_data = result.stdout.splitlines()
        
        active_wifi = [line.split(':') for line in wifi_data if line.startswith("yes")]
        
        if active_wifi:
            ssid, signal, bssid, device = active_wifi[0][1], int(active_wifi[0][2]), active_wifi[0][3], active_wifi[0][4]
            return ssid, signal, bssid, device
        else:
            return None, None, None, None
    except Exception as e:
        print(f"Error fetching Wi-Fi details: {e}")
        return None, None, None, None

wifi_signal_strength = Gauge('wifi_signal_strength_percent', 'Wi-Fi Signal Strength in percentage')
wifi_connected = Gauge('wifi_connected', 'Wi-Fi Connection Status', ['ssid', 'bssid', 'device'])

def monitor_wifi():
    while True:
        ssid, signal, bssid, device = get_wifi_details()
        
        if ssid:
            wifi_signal_strength.set(signal)
            wifi_connected.labels(ssid=ssid, bssid=bssid, device=device).set(1)
        else:
            wifi_signal_strength.set(0)
            wifi_connected.labels(ssid='none', bssid='none', device='none').set(0)
        
        time.sleep(5)

if __name__ == '__main__':
    start_http_server(8004)
    print("Prometheus server started on port 8004")
    monitor_wifi()
