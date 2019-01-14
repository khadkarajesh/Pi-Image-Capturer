# IoT Example with Google Cloud Platform and Raspberry Pi/Pi Camera

(IoT) Internet of things, is simply the ecosystem consists of web-enabled smart devices that use embedded processors, sensors and communication hardware to collect, send and act on data they acquire from their environments. Simple example of IOT is
smart homes that are equipped with smart thermostats, smart appliances and connected heating, lighting and electronic devices can be controlled remotely via computers, smartphones or other mobile devices.

For this example we have used Google Cloud Platform for the IoT Gateway. Here is the overflow of the example.

<img src="https://github.com/rajeshkumarkhadka/iot-camera-gcp/blob/master/overview.jpg"/>

***
# Hardware
1. [Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
2. [Raspberry Pi Camera Module](https://www.raspberrypi.org/products/pi-noir-camera-v2/)

***
# IoT ecosystem setup
1. [Setup raspbian](https://github.com/rajeshkumarkhadka/iot-camera-gcp/wiki/Project-Setup-in-GCP)
2. [Install Pi Camera](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
3. [Project setup in Google Cloud Platform](https://github.com/rajeshkumarkhadka/iot-camera-gcp/wiki/Project-Setup-in-GCP)
4. [Device Authentication](https://github.com/rajeshkumarkhadka/iot-camera-gcp/wiki/Device-Authentication)
5. [Add device to registry](https://github.com/rajeshkumarkhadka/iot-camera-gcp/wiki/Add-Device-to-Registry)

*** 
# How to run the Project?

**In device 1 (Raspberry pi with Pi Camera)**

Run the script raspberry_pi_with_camera.py with you information
  ``` coffeescript
  $ python  raspberry_pi_with_camera.py  --project_id your_project_id --registry_id your_retistry_id --device_id your_device_id --private_key_file path_to_private_key --algorithm algorithm_used_to_generate_key --ca_clerts path_to_roots.pem
  ```

If you have followed RS256 algorithm to generate private_key and saved private_key.pem and roots.pem inside folder device_1 then you can run only providing
```coffeescript
$ python  raspberry_pi_with_camera.py  --project_id your_project_id --registry_id your_retistry_id --device_id your_device_id 
```

**In device 2** 

Run the script subscriber.py
``` coffeescript
$ python  subscriber.py  --project_id your_project_id --subscription_name your_subscription_name
```

**In Server**

Run the script server.py
``` coffeescript
$ python server.py --project_id your_project_id --service_account_json path_to_key.json --registry_id your_retistry_id --device_id your_device_id --command command_string
```

## License

[MIT](https://github.com/rajeshkumarkhadka/iot-camera-gcp/blob/master/LICENSE)
