# DeFli_QuickStart
Quick Start DeFli and Push to Grafana

GUI based service to deploy DeFli_Run, Grafana and AcarsHub. 

## This will enable you to produce your own Grafana Dashboard as well as view tar1090.

Instructions: 

Install Docker and Docker Pre-Requirements 

```bash
bash <(wget -q -O - https://raw.githubusercontent.com/sdr-enthusiasts/docker-install/main/docker-install.sh)
```
```bash
sudo reboot
```

Clone in to Repository 

```bash
git clone https://github.com/DeFliTeam/DeFli_QuickStart.git
```

Enter Directory 

```bash
cd DeFli_Quickstart/
```

Run Script 

```bash
sudo python3 defli_run.py
```

If you have configured the containers as described above, you should be able to browse to the following web pages: You should now be able to browse to:

http://dockerhost/ to access the tar1090 web interface.
http://dockerhost/?replay to see a replay of past data
http://dockerhost/?heatmap to see the heatmap for the past 24 hours
http://dockerhost/?heatmap&realHeat to see a different heatmap for the past 24 hours
http://dockerhost/?pTracks to see the tracks of all planes for the past 24 hours
http://dockerhost/graphs1090/ to see performance graphs 

Note you can replace dockerhost with localhost or your IP address

## How to load your Grafana Dashboard 

1) Navigate to http://localhost:3000/
2) Use Username 'admin' and password 'admin' to spin up your Grafana Instance. You will be asked to set a new password after the first login.
3) From the main panel select "add your first data source". Choose "prometheus".
4) Under name input 'ultrafeeder' and under url 'http://prometheus:9090/'.
5) Click "Save and Test". If you get a "failure" message please replace the url from step 4 with "http://localhost:9090/' and run the "save and test" again.
6) Once you get the "test successful" message please click "create dashboard".
7) In the second tab down named "import from grafana.com" type "18398". In the next tab down select "ultrafeeder". Click "import".
8) Your dashboard with live data will be generated

## Incorporate Tar1090 and Graphs1090 in to Grafana 

1) From within your dashboard click on the "cog" icon (dashboard settings)
2) Choose "JSON Model" from the setting menu on the left of the screen and then click anywhere in the JSON text.
3) Press ctrl+f and press the > button to show "find and replace".
4) Find all (2) instances of my_feeder and replace them with the IP of your tar1090 map page (probably http://localhost:8078/).
5) Press Save dashboard at the top right of the screen, followed by Save on the next screen.
6) Press ESC to go back to your dashboard.

## Troubleshooting 

If you are not getting any output from your localhost you can edit the IP address used. 

To do this enter your Ubuntu terminal and run 
```bash
cd /opt/grafana/prometheus/config/
```
then 
```bash
sudo nano prometheus.yml
```
Within the file you can edit the "localhost" addresses to any you like. 

To save
```bash
ctrl + x
y
```
```bash
sudo restart prometheus
```

Then navigate back to your grafana instance at http://localhost:3000/
Choose "data sources" from the left hand menu 
Change the url to "http://your-ip-address:9090/" 
Follow the save and test + dashboard creation steps from above 

If you are running a virtual machine or a DeFli Device and are getting an error message of "RTL-SDR" not found please ensure that 
you have completed the USB attachment steps as listed here https://github.com/DeFliTeam/flightview_gui?tab=readme-ov-file#windows-including-defli-device 

If you are getting an error message saying "bind address already in use" please run the following commands: 

```bash
sudo netstat -tulpn
```
Identify the PID of the process running on the bind address from the output of the command 

Kill the process by running 

```bash
sudo kill -9 PID
```

## Note if you are running on a virtual machine or on a DeFli Device you will need to enter the IP address assigned to the virtual environment
