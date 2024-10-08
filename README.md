
![Processing Microservice_Python](https://github.com/citysciencelab/processing-microservice-python/assets/61881523/42433e4c-c2ad-47cc-89fd-383f4a26c0c0)

# Processing Microservice - Python
This repository contains the code for a processing microservice in node.js. The microservice connects with an [Urban Model Server](https://github.com/citysciencelab/urban-model-server) via a Websocket connection. In this way, different simulation models can be hosted on different isolated microservices with their own programming language, packages and versions. 

![Urban Model Server Architektur](https://github.com/citysciencelab/processing-microservice-nodejs/assets/61881523/8abef56c-ba3c-4e0a-a340-7f8856b4562a)


## Configuration
All of the necessary configuration is done in the [config.py](./config.py) file. There are two mandatory configurations:
1. ```URL``` of the Urban Model Server. ⚠️ Make sure that both the Urban Model Server and the Processing Microservice are part of the same Docker bridge network. The URL is supposed to point to this Network Gateway and the Port of the Urban Model Platform container. 
2. ```PROCESS_METADATA``` that registers the process with the Urban Model Server in accordance with the [OGC API Processes](https://docs.ogc.org/is/18-062r2/18-062r2.html) standard. If an extension is used, import the metadata from that extension folder. Otherwise, specify it manually. 

## Extensions
Although one can use basically any algorithm to handle the input, do calculations and then return an output, there are multiple simulation packages written in Python that one can leverage. Thus, multiple extensions come along with this processing microservice that one can use out of the box. The following extensions are currently available: 

### Mesa / Mesa-geo
[Mesa](https://mesa.readthedocs.io/en/stable/) and [Mesa-geo](https://pypi.org/project/Mesa-Geo/0.2.0/) are native Python agent-based modelling libraries. To simulate a Mesa/Mesa-Geo model with the processing microserivce, ```import Mesa.ProcessManager as Mesa``` in the ```server.py``` file and ```await Mesa.simulate_results(inputParameters)``` in the execute event. Create Mesa/Mesa-geo model, save it in the ```Mesa/model```folder and adapt the ```Mesa/ProcessManager.py``` file to execute the model correctly.

### NetLogo
[NetLogo](https://ccl.northwestern.edu/netlogo/) is one of the most popular agent-based modelling softwares. Build on Java, models are written in a specific NetLogo language. With the help of the great [pynetlogo](https://pynetlogo.readthedocs.io/en/latest/) library, this Python processing microservice can run NetLogo models. 
To simulate a NetLogo model with the processing microservice, ```import NetLogo.ProcessManager as NetLogo``` in the ```server.py``` file and ```await NetLogo.simulate_results(inputParameters)``` in the execute event. Create or download the NetLogo model, save it in the ```NetLogo/model```folder and specify the correct NetLogo input variables and reporters in the ```NetLogo/ProcessMetadata.py``` file. 

## Other Processing Microservices
- [node.js Processing Microservice](https://github.com/citysciencelab/processing-microservice-nodejs/)