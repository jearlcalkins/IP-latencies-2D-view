#!/home/ec2-user/python3-virtualenv/bin/python3

import platform
import ipaddress
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
import re
import time

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    #im = ax.imshow(data, **kwargs)
    #im = ax.imshow(data, extent=[0,64,0,64], vmin = 0.0, vmax = .40, **kwargs)
    im = ax.imshow(data, vmin = 0.0, vmax = .40, **kwargs)
   
    x_label_list = ['0', '16', '32', '48', '64']
    ax.set_xticks([0,16,32,48,64])
    ax.set_xticklabels(x_label_list)
    
    y_label_list = ['0', '16', '32', '48', '64']
    ax.set_yticks([0,16,32,48,64])
    ax.set_yticklabels(y_label_list)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    return im, cbar

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

def rot ( n, x, y, rx, ry ):

#*****************************************************************************80
#
## ROT rotates and flips a quadrant appropriately.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    03 January 2016
#
#  Parameters:
#
#    Input, integer N, the length of a side of the square.
#    N must be a power of 2.
#
#    Input/output, integer X, Y, the coordinates of a point.
#
#    Input, integer RX, RY, ???
#
    if ( ry == 0 ):
#
#  Reflect.
#
        if ( rx == 1 ):
            x = n - 1 - x
            y = n - 1 - y
#
#  Flip.
#
        t = x
        x = y
        y = t

    return x, y

def d2xy ( m, d ):

#*****************************************************************************80
#
## D2XY converts a 1D Hilbert coordinate to a 2D Cartesian coordinate.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license. 
#
#  Modified:
#
#    03 January 2016
#
#  Parameters:
#
#    Input, integer M, the index of the Hilbert curve.
#    The number of cells is N=2^M.
#    0 < M.
#
#    Input, integer D, the Hilbert coordinate of the cell.
#    0 <= D < N * N.
#
#    Output, integer X, Y, the Cartesian coordinates of the cell.
#    0 <= X, Y < N.
#
    n = 2 ** m

    x = 0
    y = 0
    t = d
    s = 1

    while ( s < n ):

      rx = ( ( t // 2 ) % 2 )
      if ( rx == 0 ):
          ry = ( t % 2 )
      else:
          ry = ( ( t ^ rx ) % 2 )

      x, y = rot ( s, x, y, rx, ry )
      x = x + s * rx
      y = y + s * ry
      t = ( t // 4 )

      s = s * 2

    return x, y

def build_ixy_mapper(m, first_ip_int):
#
#   function creates a dict, indexed / keyed by IP integers
#   and the dict data holds an X, Y tuple
#   not sure if i can start the IP integer mapper with real big integers
#
    mapper = {}
    n = 2 ** m
    #print("  m:", m, "n:", n)
    #print ('  D   X   Y')

    #print("first ", first_ip_int, type(first_ip_int), "n", n)

    for d in range (first_ip_int, first_ip_int + n*n):
        x,y = d2xy(m, d)
        mapper[d] = (x, y)
        #print ('%10d %10d %10d' % (d, x, y))

    return mapper

def makeNxN(col_ct, filler):
#
# function builds an N x N array
# the data structure is a list of lists
# the structure is initialized with the
# filler value
# the structure is accessed by:
# matrix[x][y], where x & y are integers, 
# smaller than the N x N 
    cols = col_ct 
    rows = col_ct 

    matrix = []
    for i in range(cols):
        col = []
        for j in range(rows):
            col.append(filler)
        matrix.append(col)

    return matrix

def readPingStats(fname, unreachable):

    i = 0
    unreachable_ct = 0
    ips = list()
    pingtimes = list()

    with open (fname, "r") as fh:
        line = fh.readline()
        result = line.split(",")
        ip = result[0]
        pingtime = result[1].rstrip()

        ips.append( int(ipaddress.ip_address(ip)))
        first_ip_int = ips[-1]
        if pingtime == 'unreachable':
            unreachable_ct += 1
            pingtimes.append(unreachable) 
        else:
            pingtimes.append(float(pingtime)) 

        #print("first IP & pingtime we read:", i, ip, first_ip_int)
        i += 1

        for line in fh:
            result = line.split(",")
            ip = result[0]
            pingtime = result[1].strip()
            ips.append( int(ipaddress.ip_address(ip)))     # save the int, not the ip string
            if pingtime == 'unreachable':
                unreachable_ct += 1
                pingtimes.append(unreachable)
            else:
                pingtimes.append(float(pingtime))

            i += 1
        
        #print("last IP & ping time we read:",i, ip, ips[-1], pingtimes[-1])
        #print("unreachable ct:", unreachable_ct)

    #print(pingtimes)
    return i, unreachable_ct, first_ip_int, ips, pingtimes, ip

def find_hilbert_order(column_ct):
    i = 0
    j = 2**i
    while j < column_ct:
        i += 1
        j = 2**i
        #print(i, j)
    return i

square_cidrs = [2**(i*2) for i in range(2,12)]

filename = "23.235.33.0-22.txt"

#print("repr:", repr(sys.argv))
#print("str:", str(sys.argv))
parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, required=True, help="filename")
args = parser.parse_args()
filename = args.f

# 23.235.32.0-20-1589922121

m0 = re.search( r'(.+)\.txt', filename)
if m0:
    base_filename = m0.group(1)

m = re.search( r'(.+)-(\d+)-(\d+)\.txt', filename)
if m:
    network_ip = m.group(1)
    cidr_number = m.group(2)
    utc_time = int(m.group(3))
    #print("fname info:", network_ip, cidr_number, utc_time, "txt")
else:
    print("filename is problematic:", filename)
    exit(-1)

ts_string = time.strftime("%m-%d-%Y %H:%M:%S", time.gmtime(utc_time))
print(ts_string)

unreachable = math.nan

i, unreachable_ct, first_ip_int, ips, pingtimes, last_ip = readPingStats(filename, unreachable)
#print("i ctr:", i, "IP count read in:", len(ips), "ping times read in:", len(pingtimes),"firstipint:", first_ip_int)
if i in square_cidrs:
    pass
else:
    print("this IP count does not lead to a square hilbert space")
    exit(-1)
if i == unreachable_ct:
    print("100% unreachable, do not plot")
    exit(-1)

xx = math.sqrt(i)
column_ct = int(xx)

hilbert_order = find_hilbert_order(column_ct)
#print("column ct", column_ct, "hilbert order:", hilbert_order)
#print("")

mapper_dict = build_ixy_mapper(hilbert_order, first_ip_int)
matrix = makeNxN(column_ct, unreachable )
#print("matrix complete for column_ct:", column_ct)

# update the matrix here:
long_ping = -100.0
short_ping = 100.0

i = 0
for ip in ips:
    (x,y) = mapper_dict[ip]
    matrix[x][y] = pingtimes[i]
    pt = pingtimes[i]

    if str(pingtimes[i]) == 'nan':
        pass
    else:
        if pt >= long_ping:
            long_ping = pt
        if pt <= short_ping:
            short_ping = pt 
        #print(i, pt, x, y, short_ping, long_ping)
    i += 1

#print("longest / shortest ping times:", long_ping, short_ping)

pingresults = np.array(matrix)
#im = ax.imshow(pingresults)
#fig, ax = plt.subplots()


fig, ax = plt.subplots()
a_title = "2D ping times " + network_ip + " /" + cidr_number + " - " + \
          last_ip + " " + str(len(ips)) + " IPs"  + '\n' + ts_string

ax.set_title(a_title)

im, cbar = heatmap(pingresults, [], [], ax=ax, cmap="coolwarm", cbarlabel="ping times in seconds")

fig.tight_layout()
#plt.show()
png_filename = base_filename + '.png'
plt.savefig(png_filename)

#     im = ax.imshow(data, vmin = 0.0, vmax = 1.0, **kwargs)
