## Welcome
This folder is your UI. Yes we know, very minimalist.

## Usage
### Set setpoints
Edit the setpoints.csv file
```
nano setpoints.csv
```

### View real time sensors & actuators
```
watch cat current_variables.csv
```

### Download data
Copy the data from the ```/data``` folder to your personal flash drive


### Configure the system
Edit the config file
```
nano config.csv
```
To get the id for the atlas sensors, run
```
python3 -m pylibftdi.examples.list_devices
```

### Debug the system
```
cat main.log
```
