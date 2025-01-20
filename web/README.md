## Multi Theft Auto: Wiki [Generator]

## License

The source code in this directory [(/web)](/web) is licensed under the GPLv3 license. See the [LICENSE](./LICENSE) file for more details.

## Development

### Prerequisites

- Python 3.5+

### Installation

Ensure you have installed the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

### Usage

```bash
# Build the Wiki
python wikigen.py build

# Serve the Wiki locally
python -m http.server -b 127.0.0.1 --directory output/html
```
