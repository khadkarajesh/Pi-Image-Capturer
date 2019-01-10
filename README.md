# IOT Example with Google Cloud Platform and Raspberry Pi/Pi Camera

(IOT) Internet of things, is simply the ecosystem consists of web-enabled smart devices that use embedded processors, sensors and communication hardware to collect, send and act on data they acquire from their environments. Simple example of IOT is
smart homes that are equipped with smart thermostats, smart appliances and connected heating, lighting and electronic devices can be controlled remotely via computers, smartphones or other mobile devices.

For this example we have used Google Cloud Platform for the IOT Gateway. Here is the overflow of the example.

<img src="https://github.com/rajeshkumarkhadka/iot-camera-gcp/blob/master/overview.jpg"/>


# How to run the Project?

**In device 1 (Raspberry pi with Pi Camera)**

Run the script raspberry_pi_with_camera.py with you information
```
Python  raspberry_pi_with_camera.py  --project_id your_project_id --registry_id your_retistry_id --device_id your_device_id --private_key_file path_to_private_key --algorithm algorithm_used_to_generate_key --ca_clerts path_to_roots.pem
```

If you have followed RS256 algorithm to generate private_key and saved private_key.pem and roots.pem inside folder device_1 then you can run only providing
```
Python  raspberry_pi_with_camera.py  --project_id your_project_id --registry_id your_retistry_id --device_id your_device_id 
```

**In device 2** 

Run the script subscriber.py
```
Python  subscriber.py  --project_id your_project_id --subscription_name your_subscription_name
```

**In Server**

Run the script server.py
```
Python server.py --project_id your_project_id --service_account_json path_to_key.json --registry_id your_retistry_id --device_id your_device_id --command command_string
```


1. The server sends a request/command using rest api to IOT core
2. Google IOT core sends the capture command to the raspberry pi 
3. Raspberry pi captures an image and sends it to google storage bucket
4. Cloud storage sends uploaded image url on successful upload
5. The device sends image url to google cloud IOT core
6. Device 2 will get uploaded image url
