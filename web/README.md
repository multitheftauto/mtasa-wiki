## Multi Theft Auto: Wiki [Generator]

## License

The source code in this directory [(/web)](/web) is licensed under the GPLv3 license. See the [LICENSE](./LICENSE) file for more details.

## Deployment

This static site is served with CloudFlare pages (this is not managed on this repository).

CloudFlare Pages handles custom error pages. it serves `404.html` when a page is not found. CloudFlare Pages also has a custom redirections system defined via [_redirects](./resources/_redirects).

## Development

### Prerequisites

- Python 3.5+

### Installation

Ensure you have installed the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

### Usage

Depending on your operating system, you can run the following commands to build and serve the wiki website.

You may keep `server_web` running in the background (in another terminal) and rebuild the website with `build_web` whenever you make changes.

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
