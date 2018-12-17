# iotcore-heartrate

This project contains the code necessary to setup either (1) a Raspberry Pi with a heart rate sensor or (2) a Google Cloud Compute Engine VM with a data simulation script in order to demonstrate how Google Cloud IoT Core works. The full instructions are contained this Codelab (https://g.co/codelabs/iotcore-heartrate). The instructions below provide the gcloud commands which are parallel to the Cloud Console UI instructions that are given in the Codelab.

## Data Simulation Quickstart

NOTE: Replace PROJECT_ID with your project in the following commands

1. Login to Google Cloud. If desired, create a new project and select it once it is ready. Open a Cloud shell.

2. Enable the necessary APIs

        gcloud services enable compute.googleapis.com
        gcloud services enable dataflow.googleapis.com
        gcloud services enable pubsub.googleapis.com
        gcloud services enable cloudiot.googleapis.com

3. Create a BigQuery dataset and table:

        bq --location=US mk --dataset PROJECT_ID:heartRateData
        bq mk --table PROJECT_ID:heartRateData.heartRateDataTable sensorID:STRING,uniqueID:STRING,timecollected:TIMESTAMP,heartrate:FLOAT
        
   In the case the table needs to be deleted (i.e. in order to be recreated)...
   
        bq rm -t -f PROJECT_ID:heartRateData.heartRateDataTable

4. Create a PubSub topic:

        gcloud beta pubsub topics create projects/PROJECT_ID/topics/heartratedata

5. Create a Dataflow process:

        Calling Google-provided Dataflow templates from the command line is not yet supported. 
        Follow the Codelab to do so via the Cloud Console.

6. Create a registry:

        gcloud beta iot registries create heartrate \
            --project=PROJECT_ID \
            --region=us-central1 \
            --event-pubsub-topic=projects/PROJECT_ID/topics/heartratedata

7. Create a VM

        gcloud compute instances create data-simulator-1 --zone us-central1-c

8. Connect to the VM. Install the necessary software and create a security certificate. Note the full path of the directory that the security certificate is stored in (the results of the "pwd" command). Then exit the connection.

        gcloud compute ssh data-simulator-1
        sudo apt-get update
        sudo apt-get install git
        git clone https://github.com/sunsetmountain/iotcore-heartrate
        cd iotcore-heartrate
        chmod +x initialsoftware.sh
        ./initialsoftware.sh
        chmod +x generate_keys.sh
        ./generate_keys.sh
        cd ../.ssh
        pwd
        exit

9. Use SCP to copy the public key that was just generated. The path the SSH keys was the result of the "pwd" command in the previous step.

        gcloud compute scp data-simulator-1:/[PATH TO SSH KEYS]/ec_public.pem .

10. Register the VM as an IoT device:

        gcloud beta iot devices create myVM \
            --project=PROJECT_ID \
            --region=us-central1 \
            --registry=heartrate \
            --public-key path=ec_public.pem,type=es256

11. Connect to the VM. Send the mock data (data/SampleData.json) using the simulateData.py script. This publishes several hundred JSON-formatted messages to the device's MQTT topic one by one:

        gcloud compute ssh data-simulator-1
        cd iotcore-heartrate
        python heartrateSimulator.py --registry_id=heartrate --project_id=PROJECT_ID --device_id=myVM --private_key_file=../.ssh/ec_private.pem
        exit
        
    Exit from the Cloud Shell
    
        exit

12. Go to BigQuery, query the data and export it to Google Sheets.

13. After you are done, clean everything up

        gcloud dataflow jobs list
        gcloud dataflow jobs cancel [JOB_ID]
        bq rm -r PROJECT_ID:heartRateData
        gcloud beta pubsub topics delete heartratedata
        gcloud beta iot devices list --registry=heartrate --region=us-central1
        gcloud beta iot devices delete [DEVICE_ID]
        gcloud beta iot registries delete heartrate --region=us-central1
        gcloud compute instances delete data-simulator-1
