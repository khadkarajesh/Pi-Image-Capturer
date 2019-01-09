
![Block diagram](https://github.com/rajeshkumarkhadka/iot-camera-gcp/blob/master/diagram.png)

1. The server sends a request using rest api to IOT core
2. Google IOT core sends the capture command to the raspberry pi 
3. Raspberry pi captures an image and sends it to google storage bucket
4. Cloud storage sends uploaded image url on successful upload
5. The device sends image url to google cloud IOT core
6. Device 2 will get uploaded image url
