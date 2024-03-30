# Function to install and grafana directories and prometheus.yml file
import os

directories = [
    "/opt/grafana/grafana/appdata",
    "/opt/grafana/prometheus/config",
    "/opt/grafana/prometheus/data"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

prometheus_config = """\
# my global config
global:
  scrape_interval: 10
  evaluation_interval: 10

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

scrape_configs:
  - job_name: "ultrafeeder"
    static_configs:
      - targets: ["localhost:9273", "localhost:9274"]

  - job_name: "prometheus"
    static_configs: 
      - targets: ["localhost:9090"]

remote_write:
  - url: https://prometheus-prod-13-prod-us-east-0.grafana.net/api/prom/push
    basic_auth:
      username: 1488847
      password: glc_eyJvIjoiMTA4MjgwNiIsIm4iOiJzdGFjay04ODc4MjAtaG0tcmVhZC1kZWZsaS1kb2NrZXIiLCJrIjoiN2NXNjJpMDkyTmpZUWljSDkwT3NOMDh1IiwibSI6eyJyIjoicHJvZC11cy1lYXN0LTAifX0=
"""
prometheus_file_path = "/opt/grafana/prometheus/config/prometheus.yml"
with open(prometheus_file_path, "w") as file:
    file.write(prometheus_config)

print("Directories and Prometheus configuration file created successfully.")
