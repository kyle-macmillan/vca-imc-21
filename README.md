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

## Dependencies

We use python to automate these calls and require the following packages:
- guibot
- pyautogui

## Automating many calls and limiting available bandwidth
We use `static.sh` to automate many calls and limit the available bandwidth.
It is a wrapper script for `test.py`, which is explained in the next section.
In our experiments, we shaped the interface on the router instead of on the 
devices. As a result, `static.sh` is configured to communicate with the 
router. It is possible to configure `static.sh` to shape on the device by 
omitting `ssh -n $ROUTER` from lines 22 and 25 and deleting line 8. It should be
noted that we use `tc` to shape interfaces, so it may be difficult to shape
locally on non-Unix machines. 

Assuming `static.sh` is correctly configured, you can automate calls using 
the following command:

`./static.sh [VCA] [DURATION] [CAPTURE INTERFACE] [SHAPING INTERFACE] [TRACE] [URL]`

- `VCA` is either 'zoom', 'meet', or 'teams'. 
- `DURATION` is the call duration. 
- `CAPTURE INTERACE` is the local interface that we capture network traffic on. 
- `SHAPING INTERACE` is the interface that we shape (either locally or at the 
router). 
- `TRACE` is the path to a trace file. `static.sh` will iterate over each line
of the trace file and shape the indicated interface accordingly. The format of
each line of the trace file is `[DURATION] [DOWNLINK BANDWIDTH] [UPLINK BANDWIDTH]`.
The bandwidths should be given in Mbps. A sample trace file is included in the
repo.
- `URL` is the url of the meeting to join. 
	
## Automating a single call
	
Alternatively, you may use `test.py` independently of `static.sh`. `test.py`
will automate one call. View all of the configuration options with 
`python3 test.py -h`. There is an option to launch in browser vs. using the 
client (for now we assume the application executables are in the working 
directory). You may also choose to capture the network traffic using the 
`-r` flag. Note: if you choose to capture traffic you must also specify an 
interface to capture on using the `-i` flag. A sample command could be:

`python3 test.py [VCA] [DURATION] -i [INTERFACE] -id [URL] -r [DOWN]-[UP]`

- `VCA` is either 'zoom', 'meet', or 'teams'.
- `DURATION` is the call duration.
- `INTERFACE` is the capture interface.
- `URL` is the meeting url
- `DOWN`-`UP` are identifiers used for logging

***

## Data Collected
Executing the sample command will automate the calls, save network traffic and
grab WebRTC (for meet and teams). Network traffic is saved in a directory 
called `captures` that is in the working directory. WebRTC stats are saved as
jsons in a directory called `webrtc` in the working directory. Finally, 
we use a log file to save metadata on the output stats and pcaps. Each pcap 
and json are given a unique ID. The network parameters, applications used, and
whether it was used in browser or client are associated with this unique ID in
a file called `stats.log`, also stored in the working directory. 

***

## Requesting data
We are happy to share the data we collected from our experiments upon request.
