# IP-latencies-2D-view
create GIF animation, for a block of IP latencies, in 2 Dimensions, using a fractal Hilbert Curve transformation

##### make_png.py

##### mapIP2XY.py
the application will read a ping latency file, with sequential IP addresses, and convert them to a 2D png file heatmap.  the file needs to be a csv file with "IP,latency" and it needs to hold a square sub-nets worth of sequential ping results.  for example, a /24 subnet holds 256 IP ping results, which gets mapped to a 16X16 png graphic.  the application will not graph data from a /25, which would be a non-square 16x8 geometry.  the application will convert the following "square" sub-net sizes:  

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

I don't know how the application and matplotlib will perform on larger subnets, like a /8.  



```
[ec2-user@mymachine]$ head 63.228.78.0-24-1590030603.txt
63.228.78.0,unreachable
63.228.78.1,0.042451
63.228.78.2,0.058078
63.228.78.3,0.043587
63.228.78.4,0.062769
63.228.78.5,0.069607
63.228.78.6,0.042485
63.228.78.7,0.049929
63.228.78.8,0.060374
63.228.78.9,0.056385
```

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
sudo or root access  
python 3.6 with these modules: argparse, sys, ipaddress, datetime, subprocess and scapy  
ethernet interface: eth0  
other linux or bsd unix's may use a different interface name. if so, the hardcoded tcpdump call, will need to be changed.  

##### rough install directions #####
be careful with python3 environment, and a good corresponding pip3 install.  
```
sudo yum update -y
sudo yum upgrade -y
sudo yum install python36 -y
sudo yum install tcpdump -y
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user

pip install numpy
pip install pandas
pip install scapy
pip install matplotlib
pip install ipaddress
```
    
##### recovering ping result times via tcpdump

The tcpdump utility, running as sudo or root, captures a sequence of ICMP 'echo request' packets (aka a ping), destined for a block of IP hosts.
bigping.py utility, currently gives tcpdump 1 second to capture the ICMP 'echo responses' come-back from responding hosts.
The tcpdump utility is stopped, and the tcpdump's pcap file is analyzed for packets sent and packets received, noting how-long it takes for each responding host to reply.
If a host does not replay within the 1 second listening period, no time in the log indicates no response.  Changing the listen period from 1 second to 2 seconds time.sleep(2) may capture more icmp responses, especially those, on the other side of the globe.  however, the elapsed time, necessary to ping a block will become longer.

    2  sudo yum update
    4  sudo yum install -y httpd24 php72 mysql57-server php72-mysqlnd
   18  sudo yum list installed httpd24 php72 mysql57-server php72-mysqlnd
   52  sudo yum install php72-gd
   77  sudo yum update
   86  sudo yum update
   87  sudo yum upgrade
  145  sudo yum list
  146  sudo yum list | grep python
  147  sudo yum list | grep python3
  148  sudo yum install python36
  149  sudo yum update -y
  150  sudo yum upgrade -y
  151  sudo yum install pip36
  152  sudo yum -y groupinstall development
  153  sudo yum -y install zlib-devel
  154  sudo yum -y install openssl-devel
  218  sudo yum install traceroute
  219  sudo yum install tcpdump
  
  151  sudo yum install pip36
  156  curl -O https://bootstrap.pypa.io/get-pip.py
  158  python3 get-pip.py --user
  160  pip --version
  161  pip3 --version
  163  pip --version
  164  pip3 install awsebcli --upgrade --user
  172  pip --version
  173  pip install -U pip requests
  174  pip freeze
  180  pip install boto3
  181  pip install ipaddress
  182  pip install ipython
  183  pip install nltk
  184  pip install numpy
  185  pip install pandas
  186  pip install scapy
  187  pip install matplotlib
  563  pip install Pillow
  151  sudo yum install pip36
  156  curl -O https://bootstrap.pypa.io/get-pip.py
  158  python3 get-pip.py --user
  160  pip --version
  161  pip3 --version
  163  pip --version
  164  pip3 install awsebcli --upgrade --user
  172  pip --version
  173  pip install -U pip requests
  174  pip freeze
  180  pip install boto3
  181  pip install ipaddress
  182  pip install ipython
  183  pip install nltk
  184  pip install numpy
  185  pip install pandas
  186  pip install scapy
  187  pip install matplotlib
  563  pip install Pillow
  
  
