# ObjectDetection-AWS
Program to detect objects in an uploaded image. Server side using Python flask and client side using spring rest template
 
Demo
----
![image](https://user-images.githubusercontent.com/68453981/136864906-74207284-0dd6-4773-a14d-6d3229a10f37.png)


Instance configured in AWS EC2 instance
----------------------------------------
![image](https://user-images.githubusercontent.com/68453981/136864039-8bded8d6-de01-4842-950b-e2bc9ea3284f.png)


Elastic IP Configured to prevent change in IP on restart of Server
-----------------------------------------------------------------
![image](https://user-images.githubusercontent.com/68453981/136864196-41daa4d6-e787-40b1-b291-d20ca7f68f18.png)

Security group rules set to give access only to required ports
--------------------------------------------------------------
![image](https://user-images.githubusercontent.com/68453981/136864310-de3bda5f-fc42-4ea8-a66e-d4389cfe7e61.png)

Client and server Instances deployed as containers in docker in EC2. Accessed using PuTTy.
-----------------------------------------------------------------------
![image](https://user-images.githubusercontent.com/68453981/136864439-ccfa4b03-a124-4647-a638-ffafb5aad005.png)

Demo: Upload image window
---
![image](https://user-images.githubusercontent.com/68453981/136864575-faa5d4e4-2e59-4597-ac2a-0fb4c90198fa.png)

Demo: Detected Images
---
![image](https://user-images.githubusercontent.com/68453981/136864807-e13ff494-9463-40c0-8b88-257c2502f097.png)

To run the instance
-------------------
1. To list all existing images: docker image ls
2. To containerise the client docker image:: <b>docker run -dp 5500:8080 objectdetection-client</b>
   - 5500 : External port to run the application at. 8080 is port in which the client spring boot application runs.
   - If image doesnot exist then to build image, go to folder where client docker file is, then run docker built -t <image-name-to-create> .
3. To cintainerise the server docker image:: <b>docker run -dp 5000:5000 tonytm1234/objectdetect-server</b>
   - 5000 is port which spring boot client application points to. Second 5000 is the port in which the python client application runs.
   - If image doesnot exist then to build image, go to folder where client docker file is, then run docker built -t <image-name-to-create> .
