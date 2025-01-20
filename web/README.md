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

Depending on your operating system, you can run the following commands:

#### Linux

```bash
# Build the wiki website
./tools/build_web.sh

# Serve the website locally
./tools/serve_web.sh
```

#### Windows

```bash
# Build the wiki website
./tools/build_web.cmd

# Serve the website locally
./tools/serve_web.cmd
```
