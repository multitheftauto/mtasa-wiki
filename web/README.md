## Multi Theft Auto: Wiki [Generator]

## License

The source code in this directory [(/web)](/web) is licensed under the GPLv3 license. See the [LICENSE](./LICENSE) file for more details.

## Deployment

This static site is served with CloudFlare pages (this is not managed on this repository).

CloudFlare Pages handles custom error pages. For example, it serves `404.html`, when a page is not found.

## Development

### Prerequisites

- Python 3.5+

### Installation

Ensure you have installed the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

### Usage

The `wikigen.py` script is intended to be executed from the root of the repository.

To build the repository, run `tools/build_web.sh` or `tools/build_web.cmd` depending on your operating system.

To serve the repository locally, run the following command:

```bash
python -m http.server -b 127.0.0.1 --directory web/output/html
```
