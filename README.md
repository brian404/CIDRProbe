# CIDR Probe

CIDR Probe is a Python script that allows you to scan a CIDR range for open ports and retrieve the HTTP status codes of the corresponding services.

## Installation

0. Run the following command to quickly set up CIDR Probe:
        ```bash
    wget https://raw.githubusercontent.com/brian404/CIDRProbe/main/install.sh && chmod +x install.sh && ./install.sh --venv

1. Clone the repository:

    ```bash
    git clone https://github.com/brian404/CIDRProbe.git
    ```

2. Navigate to the project directory:

    ```bash
    cd CIDRProbe
    ```

3. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```
    ### Option B: Using pip (with virtual environment)
```bash
# Set up a virtual environment:
python3 -m venv .venv

# Activate the virtual environment:
source .venv/bin/activate

# Install the required dependencies using pip:
python3 -m pip install -r requirements.txt
```

## Usage

To use CIDR Probe, follow these steps:

1. Run the script and provide the CIDR range and port to scan when prompted:

    ```bash
    python cidr.py
    ```

2. The script will scan the specified CIDR range for open ports and retrieve the corresponding HTTP status codes.

3. The results will be displayed in the console, showing the IP address, port, status (open/closed), and HTTP status code.

4. If an IP address has restrictions or is unreachable, the script will display an appropriate message.

### Advanced Usage

You can also customize your scans using the following options:

- Specify a different port to scan (default is 80):

    ```bash
    python cidr.py -p 8080
    ```

- Perform SSL/TLS checks (default is off):

    ```bash
    python cidr.py -ssl
    ```

- Save the scan results to a file:

    ```bash
    python cidr.py > scan_results.txt
    ```
    - Reverse lookup CIDR/ip address using hacker target 

    ```bash
    python cidr.py -ht
    ```
    

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

#CIDRscanner #networking #security #Python #cidr
