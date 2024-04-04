# 5GCore Implementation Comparison

This repository is for the final project of graduate 5G Course (COMP 5900) in Winter 2024 at Carleton University.

## Introduction

The purpose of this project is to make a comprehensive comparison between two well-known 5G core implementations: Free5GC and Open5gs.

Our evaluation has two aspects: Performance Evaluation and Security Evaluation


## Performance Evaluation

In order to evaluate and compare the performance of Free5GC and Open5gs we created three virtual machines:

 - Free5GC: Uubntu 20.04 server, 2GB RAM, 2 CPU cores
 - Open5gs: Uubntu 20.04 server, 2GB RAM, 2 CPU cores
 - UERANSIM: Uubntu 20.04 server, 2GB RAM, 2 CPU cores

There are three metrics that we are using to compare the performance of Free5GC and Open5gs:
 - Latency
 - Throughput
 - Resource Consumption

### File Structure

Inside the performance_metrics folder are all the files that are used to facilitate the process of performance metric collection from the 5G core networks.

Inside this folder there are 4 python scripts, 1 notebook file and three folders for keepting the results of collecting metrics for each 5G core network.
 - latency.py: This file will be run in the UERANSIM VM and execuate a ping command multiple times. The results were printed in the console and then copy and pasted in the latency.txt files for each case of not using 5G core, using Free5GC and using Open5gs.
 - throughputusingspeedtest.py: This is the script that uses the speedtest-cli python library to measure the upload and download speed. This script was executed in the UERANSIM VM. In order to make sure the speedtest traffic is going through the 5G core network, the default interface of the VM should be changed to uesimtun0 before running this python program.
 - downloadspeedusingwget.py: This is the scripts that measures the download speed of the VM. wget has a command line argument that allows to modify the interface that the traffic will go through. Since there was a significant drop in the downlink speed of the VM when the traffic was going through the 5G core network, we used the wget command line argument as an alternative to changing the default interface of the VM and made sure that the download speed that we measured based on this method is consistant with the collected measurments from speedtest-cli.
 - resourcemonitor.py: This is the script that should be run inside the VM that is hosting the 5G core network. It will capture the CPU and memory consumption of the VM every second and writes them into files. It will continue this task forever until it is terminiated manually.
 - data_analysis.ipynb: This is the notebook file that reads the collected measurements and plot them into figures.
 - Free5GC: This folder contains the files that have the collected metrics of the Free5GC core network.
 - Open5gs: This folder contains the files that have the collected metrics of the Open5gs core network.
 - without5Gcore: This folder contains the files that have the collected metrics of the network when the traffic is going directly to the Internet instead of going through the 5G core network.

## Security Evaluation

Tested with python 3.11.5 for generating secuiry report.


To create the **security report** for comparing each image's vulnerability between Clair and Trivy, run:

```
python compareReport.py
```

It will generate an output, named "image_comparison_results.log".


To create the **security report** for comparing each prototype's vulnerability, run:

```
python comparePrototypes.py
```

It will generate an output, named "prototype_comparison_results.log".