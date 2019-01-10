# IOT Example with Google Cloud Platform and Raspberry Pi/Pi Camera

(IOT) Internet of things, is simply the ecosystem consists of web-enabled smart devices that use embedded processors, sensors and communication hardware to collect, send and act on data they acquire from their environments. Simple example of IOT is
smart homes that are equipped with smart thermostats, smart appliances and connected heating, lighting and electronic devices can be controlled remotely via computers, smartphones or other mobile devices.

For this example we have used Google Cloud Platform for the IOT Gateway. Here is the overflow of the example.

<img src="https://github.com/rajeshkumarkhadka/iot-camera-gcp/blob/master/overview.jpg"/>



1. The server sends a request/command using rest api to IOT core
2. Google IOT core sends the capture command to the raspberry pi 
3. Raspberry pi captures an image and sends it to google storage bucket
4. Cloud storage sends uploaded image url on successful upload
5. The device sends image url to google cloud IOT core
6. Device 2 will get uploaded image url
