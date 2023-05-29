CIDR Probe
==========

CIDR Probe is a Python script that allows you to scan a CIDR range for open ports and retrieve the HTTP status codes of the corresponding services.

Installation
------------

1. Clone the repository:

    ```
    git clone https://github.com/brian404/CIDRProbe.git
    ```

2. Navigate to the project directory:

    ```
    cd CIDRProbe
    ```

3. Install the required dependencies using pip:

    ```
    pip install -r requirements.txt
    ```

Usage
-----

1. Run the script and provide the CIDR range and port to scan when prompted:

    ```
    python cidr.py
    ```

2. The script will scan the specified CIDR range for open ports and retrieve the corresponding HTTP status codes.

3. The results will be displayed in the console, showing the IP address, port, status (open/closed), and HTTP status code.

4. If an IP address has restrictions or is unreachable, the script will display an appropriate message.

Contributing
------------

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

License
-------

This project is licensed under the MIT License. See the `LICENSE` file for more information.
#CIDRscanner, #networking, #security, #Python