# openleadr-docker-setup
Using OpenLEADR to implement an OpenADR test network managed with Docker

OpenLEADR is the leading open source implementation of OpenADR, which is an Internet protocol to automate demand/response programs.  Setting up OpenADR requires two kinds of entities:

* A VTN (Virtual Top Node) is the system for sending out "signals" or commands.
* A VEN (Virtual End Node) are the system or systems that control or monitor individual pieces of equipment or resources.

In this repository we demonstrate a simple system meant for experimentation with OpenADR/OpenLEADR on your laptop.  This setup is in part designed to support software development of VTN and VEN servers.  Namely:

* A Docker container, `robogeek/python-openleadr-nodemon`, contains Python v3, a number of preinstalled Python packages required for OpenLEADR
* The container includes Nodemon configured to watch the source tree for both OpenLEADR and the VEN or VTN service
* Mounting into the container OpenLEADR source code
* Mounting into the container the VEN or VTN service

The result is you can construct a Docker Compose file with multiple services, where the Docker container will restart the service as soon as you edit one of the files.  That will tighten the software development loop by automatically restarting with the changes you've made.

The Docker setup in this repository is discussed here: https://techsparx.com/energy-system/openadr/openleadr-docker.html

The example VTN and VEN code here was originally developed from sample code on the OpenLEADR website, and then checked carefully against a different example in https://github.com/bbartling/openadrtester

