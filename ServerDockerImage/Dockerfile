FROM ubuntu:18.04
RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev ffmpeg libsm6 libxext6 libxrender-dev
WORKDIR /code
ADD object_detection.py /code
COPY requirements.txt requirements.txt
ADD yolo_tiny_configs /code/yolo_tiny_configs
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "/code/object_detection.py", "yolo_tiny_configs/"]
