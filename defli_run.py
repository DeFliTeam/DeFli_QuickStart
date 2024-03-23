#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import subprocess
import yaml
import os
import sys

# Function to check for sudo privileges
def check_sudo():
    if os.geteuid() != 0:
        return False
    return True 

# Function to create Grafana directory and subdirectories
os.makedir(/opt/grafana)
os.makedirs(/opt/grafana/grafana/appdata)
os.makedirs(/opt/grafana/prometheus/config)
os.makedirs(/opt/grafana/prometheus/data)

# Function to load the current configuration values for a Docker service
def load_current_config(file_path, lat_entry, lon_entry, tz_entry, alt_entry):
    with open(file_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    lat = ''
    lon = ''
    tz = ''
    alt = ''
    bucketid = ''
    ip = ''

    if 'services' in config:
        for service in config['services']:
            env = config['services'][service].get('environment', [])
            for var in env:
                if var.startswith('LAT='):
                    lat = var.split('=')[1]
                elif var.startswith('LONG='):
                    lon = var.split('=')[1]
                elif var.startswith('TZ='):
                    tz = var.split('=')[1]
                elif var.startswith('ALT='):
                    tz = var.split('=')[1] 
                elif var.startswith('BUCKETID='):
                    tz = var.split('=')[1]
                elif var.startswith('IP='):
                    tz = var.split('=')[1]

    lat_entry.delete(0, tk.END)
    lon_entry.delete(0, tk.END)
    tz_entry.delete(0, tk.END)
    alt_entry.delete(0, tk.END)
    bucketid_entry.delete(0, tk.END)
    ip_entry.delete(0, tk.END)

    lat_entry.insert(0, lat)
    lon_entry.insert(0, lon)
    tz_entry.insert(0, tz)
    alt_entry.insert(0, alt)
    bucketid_entry.insert(0, bucketid)
    ip_entry.insert(0, ip)

# Function to check if a Docker service is running
def is_service_running(service_name):
    result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], stdout=subprocess.PIPE)
    return service_name in result.stdout.decode().splitlines()

# Function to update the running indicator
def update_running_indicator(is_running, running_label):
    if is_running:
        running_label.config(text="Running", foreground="green")
    else:
        running_label.config(text="Not Running", foreground="red")

# Check for sudo privileges before running the script
if not check_sudo():
    print("This script requires sudo privileges. Please run it with sudo.")
    sys.exit(1)

# Function to apply temporary changes to a Docker service configuration
def apply_temporary_changes(file_path, new_lat, new_lon, new_tz, new_alt, new_bucketid, new_ip):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    for service in config['services']:
        env = config['services'][service].get('environment', [])
        for i in range(len(env)):
            if env[i].startswith('LAT='):
                env[i] = f'LAT={new_lat}'
            elif env[i].startswith('LONG='):
                env[i] = f'LONG={new_lon}'
            elif env[i].startswith('TZ='):
                env[i] = f'TZ={new_tz}'
            elif env[i].startswith('ALT='):
                env[i] = f'TZ={new_alt}'
            elif env[i].startswith('BUCKETID='):
                env[i] = f'TZ={new_bucketid}' 
            elif env[i].startswith('IP='):
                env[i] = f'TZ={new_ip}'

    with open(file_path, 'w') as file:
        yaml.dump(config, file)

# Function to start a Docker service
def start_service(file_path, lat_entry, lon_entry, tz_entry, alt_entry, bucketid_entry, ip_entry, running_label):
    apply_temporary_changes(file_path, lat_entry.get(), lon_entry.get(), tz_entry.get(), alt_entry.get(), bucketid_entry.get(), ip_entry.get())
    subprocess.Popen(["docker", "compose", "--file", file_path, "up", "-d"])
    update_running_indicator(True, running_label)

# Function to stop a Docker service
def stop_service(file_path, running_label):
    subprocess.Popen(["docker", "compose", "--file", file_path, "down"])
    update_running_indicator(False, running_label)

# Function to load the current configuration values for the DeFli_Run service
def load_defli_run_config(file_path, lat_entry, lon_entry, tz_entry, alt_entry, bucketid_entry):
    with open(file_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    lat = ''
    lon = ''
    tz = ''

    if 'services' in config and 'defli_run' in config['services']:
        env = config['services']['defli_run'].get('environment', [])
        for var in env:
            if var.startswith('READSB_LAT='):
                lat = var.split('=')[1]
            elif var.startswith('READSB_LON='):
                lon = var.split('=')[1]
            elif var.startswith('TZ='):
                tz = var.split('=')[1]
            elif var.startswith('ALT='):
                tz = var.split('=')[1]
            elif var.startswith('BUCKETID='):
                tz = var.split('=')[1]

    lat_entry.delete(0, tk.END)
    lon_entry.delete(0, tk.END)
    tz_entry.delete(0, tk.END)
    alt_entry.delete(0, tk.END)
    bucketid_entry.delete(0, tk.END)

    lat_entry.insert(0, lat)
    lon_entry.insert(0, lon)
    tz_entry.insert(0, tz)
    alt_entry.insert(0, tz)
    bucketid_entry.insert(0, tz)

# Function to check if the DeFli_Run service is running
def is_readsb_service_running():
    return is_service_running("defli_run")

# Function to apply temporary changes to the DeFli_Run service configuration
def apply_temporary_defli_run_changes(file_path, new_lat, new_lon, new_tz, new_alt, new_bucketid):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    if 'services' in config and 'defli_run' in config['services']:
        env = config['services']['defli_run'].get('environment', [])
        for i in range(len(env)):
            if env[i].startswith('READSB_LAT='):
                env[i] = f'READSB_LAT={new_lat}'
            elif env[i].startswith('READSB_LON='):
                env[i] = f'READSB_LON={new_lon}'
            elif env[i].startswith('TZ='):
                env[i] = f'TZ={new_tz}'
            elif env[i].startswith('ALT='):
                env[i] = f'ALT={new_tz}'
            elif env[i].startswith('BUCKETID='):
                env[i] = f'BUCKETID={new_tz}'

    with open(file_path, 'w') as file:
        yaml.dump(config, file)

# Function to start the DeFli_Run service
def start_defli_run_service(file_path, lat_entry_2, lon_entry_2, tz_entry_2, alt_entry_2, bucketid_entry_2, running_label_2):
    apply_temporary_defli_run_changes(file_path, lat_entry_2.get(), lon_entry_2.get(), tz_entry_2.get(), alt_entry_2.get(), bucketid_entry_2.get())
    subprocess.Popen(["docker", "compose", "--file", file_path, "up", "-d"])
    update_running_indicator(True, running_label_2)

# Function to stop the DeFli_Run service
def stop_defli_run_service(file_path, running_label_2):
    subprocess.Popen(["docker", "compose", "--file", file_path, "down"])
    update_running_indicator(False, running_label_2)

# Function to save changes to a Docker service configuration
def save_changes(file_path, new_lat, new_lon, new_tz, new_alt, new_bucketid):
    apply_temporary_changes(file_path, new_lat, new_lon, new_tz, new_alt, new_bucketid)

# Function to save changes for the DeFli_Run service configuration
def save_defli_run_changes(file_path, new_lat, new_lon, new_tz, new_alt, new_bucketid):
    apply_temporary_defli_run_changes(file_path, new_lat, new_lon, new_tz, new_alt, new_bucketid)

# Function to load the current configuration values for the acarshub service
def load_acarshub_config(file_path, lat_entry, lon_entry, tz_entry alt_entry, bucketid_entry, feed_entry):
    with open(file_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    lat = ''
    lon = ''
    tz = ''
    alt = ''
    feed = ''
    

    if 'services' in config:
        if 'acarshub' in config['services']:
            acarshub_env = config['services']['acarshub'].get('environment', [])
            for var in acarshub_env:
                if var.startswith('ADSB_LAT='):
                    lat = var.split('=')[1]
                elif var.startswith('ADSB_LON='):
                    lon = var.split('=')[1]
                elif var.startswith('TZ='):
                    tz = var.split('=')[1]
                elif var.startswith('ALT='):
                    alt = var.split('=')[1]

        if 'acarsdec' in config['services']:
            acarsdec_env = config['services']['acarsdec'].get('environment', [])
            for var in acarsdec_env:
                if var.startswith('FEED_ID='):
                    feed = var.split('=')[1]

    lat_entry.delete(0, tk.END)
    lon_entry.delete(0, tk.END)
    tz_entry.delete(0, tk.END)
    alt_entry.delete(0, tk.END)
    feed_entry.delete(0, tk.END)
    feed_entry.insert(0, feed)

    lat_entry.insert(0, lat)
    lon_entry.insert(0, lon)
    tz_entry.insert(0, tz)
    alt_entry.insert(0, alt)
    feed_entry.insert(0, alt)

# Function to check if the acarshub service is running
def is_acarshub_service_running():
    return is_service_running("acarshub")

# Function to apply temporary changes to the acarshub service configuration
def apply_temporary_acarshub_changes(file_path, new_lat, new_lon, new_tz, new_alt, new_feed):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    if 'services' in config:
        if 'acarshub' in config['services']:
            acarshub_env = config['services']['acarshub'].get('environment', [])
            for i in range(len(acarshub_env)):
                if acarshub_env[i].startswith('ADSB_LAT='):
                    acarshub_env[i] = f'ADSB_LAT={new_lat}'
                elif acarshub_env[i].startswith('ADSB_LON='):
                    acarshub_env[i] = f'ADSB_LON={new_lon}'
                elif acarshub_env[i].startswith('TZ='):
                    acarshub_env[i] = f'TZ={new_tz}'
                elif acarshub_env[i].startswith('ALT='):
                    acarshub_env[i] = f'ALT={new_alt}'

        if 'acarsdec' in config['services']:
            acarsdec_env = config['services']['acarsdec'].get('environment', [])
            for i in range(len(acarsdec_env)):
                if acarsdec_env[i].startswith('FEED_ID='):
                    acarsdec_env[i] = f'FEED_ID={new_feed}'

    with open(file_path, 'w') as file:
        yaml.dump(config, file)

# Function to start the acarshub service
def start_acarshub_service(file_path, lat_entry, lon_entry, tz_entry, alt_entry, feed_entry, running_label_3):
    apply_temporary_acarshub_changes(file_path, lat_entry.get(), lon_entry.get(), tz_entry.get(), alt_entry.get(), feed_entry.get())
    subprocess.Popen(["docker", "compose", "--file", file_path, "up", "-d"])
    update_running_indicator(True, running_label_3)

# Function to stop the acarshub service
def stop_acarshub_service(file_path, running_label_3):
    subprocess.Popen(["docker", "compose", "--file", file_path, "down"])
    update_running_indicator(False, running_label_3)

# Function to save changes to the acarshub service configuration
def save_acarshub_changes(file_path, new_lat, new_lon, new_tz, new_alt, new_feed):
    apply_temporary_acarshub_changes(file_path, new_lat, new_lon, new_tz, new_alt, new_feed)

# Create the main window
window = tk.Tk()
window.title("DeFli Installation")

# Create a notebook for split view
notebook = ttk.Notebook(window)
notebook.pack(fill='both', expand=True)

# Create a tab for each Docker service
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook) 


notebook.add(tab1, text="Service 1 (DeFli_Run)")
notebook.add(tab2, text="Service 2 (Grafana)")
notebook.add(tab3, text="Service 3 (acarshub)")

# Function to manually set the initial focus
def set_initial_focus(event):
    start_button_3.focus_set()

# Bind an event to the third tab to set the initial focus
tab3.bind("<Visibility>", set_initial_focus)

# Create and configure widgets for Service 1 (defli_run)
start_button_1 = tk.Button(tab1, text="Start DeFli_Run Service", command=lambda: start_service("docker-compose-defli_run.yml", lat_entry, lon_entry, tz_entry, alt_entry running_label))
stop_button_1 = tk.Button(tab1, text="Stop DeFli_Run Service", command=lambda: stop_service("docker-compose-defli_run.yml", running_label))
save_button_1 = tk.Button(tab1, text="Save Changes", command=lambda: save_changes("docker-compose-defli_run.yml", lat_entry.get(), lon_entry.get(), tz_entry.get(), alt_entry.get()))
lat_label_1 = tk.Label(tab1, text="Latitude:")
lon_label_1 = tk.Label(tab1, text="Longitude:")
tz_label_1 = tk.Label(tab1, text="Timezone:")
alt_label_1 = tk.Label(tab1, text="Altitude M:")
lat_entry = tk.Entry(tab1)
lon_entry = tk.Entry(tab1)
tz_entry = tk.Entry(tab1)
alt_entry = tk.Entry(tab1)
running_label = tk.Label(tab1, text="Not Running", foreground="red")

# Load and display the current configuration values for Service 1 (defli_run)
load_current_config("docker-compose-tar1090.yml", lat_entry, lon_entry, tz_entry, alt_entry)
update_running_indicator(is_service_running("docker-compose-defli_run.yml"), running_label)

# Arrange widgets for Service 1 (defli_run)
start_button_1.grid(row=0, column=0, padx=10, pady=10)
stop_button_1.grid(row=0, column=1, padx=10, pady=10)
save_button_1.grid(row=4, column=0, padx=10, pady=10)
lat_label_1.grid(row=1, column=0, padx=10, pady=10)
lat_entry.grid(row=1, column=1, padx=10, pady=10)
lon_label_1.grid(row=2, column=0, padx=10, pady=10)
lon_entry.grid(row=2, column=1, padx=10, pady=10)
tz_label_1.grid(row=3, column=0, padx=10, pady=10)
tz_entry.grid(row=3, column=1, padx=10, pady=10)
alt_label_1.grid(row=4, column=0, padx=10, pady=10)
alt_entry.grid(row=4, column=1, padx=10, pady=10)
running_label.grid(row=5, column=1, padx=10, pady=10)

# Create and configure widgets for Service 2 (grafana)
start_button_2 = tk.Button(tab2, text="Start Grafana Service", command=lambda: start_grafana_service("docker-compose-grafana.yml", lat_entry_2, lon_entry_2, tz_entry_2, running_label_2))
stop_button_2 = tk.Button(tab2, text="Stop GRAFANA Service", command=lambda: stop_grafana_service("docker-compose-grafana.yml", running_label_2))
save_button_2 = tk.Button(tab2, text="Save Changes", command=lambda: save_grafana_changes("docker-compose-grafana.yml", lat_entry_2.get(), lon_entry_2.get(), tz_entry_2.get()))
lat_label_2 = tk.Label(tab2, text="Latitude:")
lon_label_2 = tk.Label(tab2, text="Longitude:")
tz_label_2 = tk.Label(tab2, text="Timezone:")
lat_entry_2 = tk.Entry(tab2)
lon_entry_2 = tk.Entry(tab2)
tz_entry_2 = tk.Entry(tab2)
running_label_2 = tk.Label(tab2, text="Not Running", foreground="red")

# Load and display the current configuration values for Service 2 (grafana)
load_readsb_config("docker-compose-readsb.yml", lat_entry_2, lon_entry_2, tz_entry_2)
update_running_indicator(is_readsb_service_running(), running_label_2)

# Arrange widgets for Service 2 (grafana)
start_button_2.grid(row=0, column=0, padx=10, pady=10)
stop_button_2.grid(row=0, column=1, padx=10, pady=10)
save_button_2.grid(row=4, column=0, padx=10, pady=10)
lat_label_2.grid(row=1, column=0, padx=10, pady=10)
lat_entry_2.grid(row=1, column=1, padx=10, pady=10)
lon_label_2.grid(row=2, column=0, padx=10, pady=10)
lon_entry_2.grid(row=2, column=1, padx=10, pady=10)
tz_label_2.grid(row=3, column=0, padx=10, pady=10)
tz_entry_2.grid(row=3, column=1, padx=10, pady=10)
running_label_2.grid(row=4, column=1, padx=10, pady=10)

# Create and configure widgets for Service 3 (acarshub)
feed_label = tk.Label(tab3, text="FEED_ID:")
feed_entry = tk.Entry(tab3)  # Entry for entering new FEED_ID
start_button_3 = tk.Button(tab3, text="Start acarshub Service", command=lambda: start_acarshub_service("docker-compose-acars.yml", lat_entry_3, lon_entry_3, tz_entry_3, feed_entry, alt_entry3, running_label_3))
stop_button_3 = tk.Button(tab3, text="Stop acarshub Service", command=lambda: stop_acarshub_service("docker-compose-acars.yml", running_label_3))
save_button_3 = tk.Button(tab3, text="Save Changes", command=lambda: save_acarshub_changes("docker-compose-acars.yml", lat_entry_3.get(), lon_entry_3.get(), tz_entry_3.get(), alt_entry_3.get(), feed_entry.get()))
lat_label_3 = tk.Label(tab3, text="Latitude:")
lon_label_3 = tk.Label(tab3, text="Longitude:")
tz_label_3 = tk.Label(tab3, text="Timezone:")
alt_label_3 = tk.Label(tab3, text="Altitude M:")
lat_entry_3 = tk.Entry(tab3)
lon_entry_3 = tk.Entry(tab3)
tz_entry_3 = tk.Entry(tab3) 
alt_entry_3 = tk.Entry(tab3) 
running_label_3 = tk.Label(tab3, text="Not Running", foreground="red")

# Load and display the current configuration values for Service 3 (acarshub)
load_acarshub_config("docker-compose-acars-vhf.yml", lat_entry_3, lon_entry_3, tz_entry_3, alt_entry, feed_entry)
update_running_indicator(is_acarshub_service_running(), running_label_3)

# Arrange widgets for Service 3 (acarshub)
start_button_3.grid(row=0, column=0, padx=10, pady=10)
stop_button_3.grid(row=0, column=1, padx=10, pady=10)
save_button_3.grid(row=6, column=0, padx=10, pady=10)
lat_label_3.grid(row=1, column=0, padx=10, pady=10)
lat_entry_3.grid(row=1, column=1, padx=10, pady=10)
lon_label_3.grid(row=2, column=0, padx=10, pady=10)
lon_entry_3.grid(row=2, column=1, padx=10, pady=10)
tz_label_3.grid(row=3, column=0, padx=10, pady=10)
tz_entry_3.grid(row=3, column=1, padx=10, pady=10)
alt_label_3.grid(row=4, column=0, padx=10, pady=10)
alt_label_3.grid(row=4, column=1, padx=10, pady=10)
feed_label.grid(row=5, column=0, padx=10, pady=10)
feed_entry.grid(row=5, column=1, padx=10, pady=10)
running_label_3.grid(row=6, column=1, padx=10, pady=10)

# Start the GUI event loop
window.mainloop()
