
![Processing Microservice_Python](https://github.com/citysciencelab/processing-microservice-python/assets/61881523/42433e4c-c2ad-47cc-89fd-383f4a26c0c0)

# Processing Microservice - Python
This repository contains the code for a processing microservice in node.js. The microservice connects with an [Urban Model Server](https://github.com/citysciencelab/urban-model-server) via a Websocket connection. In this way, different simulation models can be hosted on different isolated microservices with their own programming language, packages and versions. 

![Urban Model Server Architektur](https://github.com/citysciencelab/processing-microservice-nodejs/assets/61881523/8abef56c-ba3c-4e0a-a340-7f8856b4562a)


## Configuration
All of the necessary configuration is done in the [config.py](./config.py) file. There are two mandatory configurations:
1. ```URL``` of the Urban Model Server. ⚠️ Make sure that both the Urban Model Server and the Processing Microservice are part of the same Docker bridge network. The URL is supposed to point to this Network Gateway and the Port of the Urban Model Platform container. 
2. ```PROCESS_METADATA``` that registers the process with the Urban Model Server in accordance with the [OGC API Processes](https://docs.ogc.org/is/18-062r2/18-062r2.html) standard. 

## Extensions
Although one can use basically any algorithm to handle the input, do calculations and then return an output, there are multiple simulation packages written in Python that one can leverage. Thus, multiple extensions come along with this processing microservice that one can use out of the box. The following extensions are currently available: 

### Mesa / Mesa-geo


## Other Processing Microservices
- [node.js Processing Microservice](https://github.com/citysciencelab/processing-microservice-nodejs/)