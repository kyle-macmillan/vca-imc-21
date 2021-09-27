# Automating videoconferencing applications (VCA)

This is a repo containing the code used to automate video conferencing calls
in [Measuring the Performance and Network Utilization of Popular Video 
Conferencing Applications](https://arxiv.org/pdf/2105.13478.pdf). 

***

This code allows you to simulate videoconferencing calls on three major 
applications: Google Meet, Zoom, and Microsoft Teams. This code relies on 
the python [guibot](https://guibot.readthedocs.io/en/latest/README.html)
module. We have included images used by guibot to interact with the 
applications. 

## Sample Usage
In our experiments, we shaped the interface on the router instead of on the 
devices. As a result, `static.sh` is configured to communicate with the 
router. It is possible to configure `static.sh` to shape on the device by 
changing 
