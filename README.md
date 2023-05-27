# CIDRProbe

CIDRProbe is an advanced CIDR scanner tool that performs HTTP requests to IP addresses within a specified CIDR range. It can help identify alive IP addresses and detect open ports.

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
