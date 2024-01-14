FROM ubuntu 

WORKDIR /usr/src/app 
COPY . ./ 

RUN apt update 
RUN apt -y upgrade 
RUN apt install -y python3-dev python3-pip 

RUN pip3 install -r requirements.txt

CMD ["python3", "run.py"]