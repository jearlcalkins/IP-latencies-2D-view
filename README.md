# IP-latencies-2D-view
create GIF animation, for a block of IP latencies, in 2 Dimensions, using a fractal Hilbert Curve transformation

##### make_png.py

##### mapIP2XY.py
This application will read a ping latency file, with sequential IP addresses, and convert them to a 2D heatmap visualization in a png file format.  The ping file needs to be a csv file, with each record formatted as: "IP,latency".  The file needs to hold a square sub-nets worth of sequential ping results.  For example, a /24 subnet holds 256 IP ping results, which gets mapped to a square 16X16 png graphic.  The application will not graph data from a /25 (16x8), because it is a non-square 16x8 geometry.  The application will convert the following "square" sub-net sizes:  

/30 4 IPs - 2x2  
/28 16 IPs - 4x4  
/26 64 IPs - 8x8  
/24 256 IPs - 16x16  
/22 1024 IPs - 64x64  
/20 4096 IPs - 256x256  
/18 16384 IPs - 1024x1024  
/16 65536 IPs - 4096x4096  
/14 262144 IPs - 16384x16384   
...

I don't know how-well the application and matplotlib will perform on larger subnet ping datasets, like a /8.  

The following is a snippet, from a raw CSV ping stat dataset

```
me@:~$ head 188.114.96.0-20-1590469441.txt 
188.114.96.0,unreachable
188.114.96.1,0.203748
188.114.96.2,unreachable
188.114.96.3,unreachable
188.114.96.4,unreachable
```

##### How-to create a single png heatmap, from a csv png file:  

```
python mapIP2XY.py 192.168.0.0-24-1590031803.txt
```
mapIP2XY.py will open a ping latency file, with an IPv4 and cidr "size" naming format  
192.168.0.0-24-1590031803.txt where  
192.168.0.0 is a base network address
24 is a cidr size
one would write the above, in cidr as:  
192.168.0.0/24  
in this example, the 

##### run environment:
AWS AMI linux on t2.micro  
tcpdump installed  
imaging Pillow environment installed
sudo or root access  
python 3.6 with these modules: PIL, math, matplotlib, numpy,  ipaddress, argparse, sys, re, time, datetime, subprocess, glob, os 
ethernet interface: eth0  
other linux or bsd unix's may use a different interface name. if so, the hardcoded tcpdump call, will need to be changed.  

##### rough install directions #####
be careful, getting your python3 environment setup, and there is a successful corresponding pip3 install.  the pip commands below are assuming the pip --version corresponds to your python36 version.  v

```
sudo yum update -y
sudo yum upgrade -y
sudo yum -y groupinstall development
sudo yum install python36 -y
sudo yum install tcpdump -y
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user

pip install numpy
pip install pandas
pip install scapy
pip install matplotlib
pip install ipaddress
pip install Pillow

```


  
  
