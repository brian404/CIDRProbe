# CIDRProbe

CIDRProbe is an advanced CIDR scanner tool that performs HTTP requests to IP addresses within a specified CIDR range. It helps identify alive IP addresses and detect open ports.

## Installation

1. Clone the repository:

```shell

git clone https://github.com/brian404/CIDRProbe.git

cd CIDRProbe
pip install -r requirements.txt

## Usage

To use CIDRProbe, follow these steps:

1. Open a terminal and navigate to the CIDRProbe directory.

2. Run the CIDRProbe tool with the desired CIDR range:

   ```shell

   python cidr.py <CIDR_RANGE> [-p PORT] [-t TIMEOUT]

##example
python cidr.py 192.168.0.0/24 -p 80 -t 2

In this example, CIDRProbe will scan the CIDR range 192.168.0.0/24 for alive IP addresses. It will check for open port 80 and set the timeout for HTTP requests to 2 seconds.

Wait for the tool to scan the CIDR range and display the results.

The tool will save the alive IP addresses to a file named alive.txt in the current directory.
