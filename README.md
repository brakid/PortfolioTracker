# Portfolio Tracker

* portfolio overview: *name*, *isin* and *amount* of the assets in file **portfolio.csv**
* daily [Cron job](https://en.wikipedia.org/wiki/Cron) to update the asset prices using website [Finanzen.net](https://finanzen.net)
  * ```0 21 * * * cd /path/to/script; python3.6 portfolio_updater.py >/dev/null 2>&1```
* stores daily snapshots (*isin*, *amount*, *price* and *date*) in an [SQLite Database](https://www.sqlite.org/) file **portfolio.db**
* runs as a [Streamlit App](https://docs.streamlit.io/): allows modifying the portfolio (e.g when buying or selling assets) and displays the portfolio development over time

## Golang based asset price retriever
Instead of using a sequential Python-based retriever to obtain current asset prices, switching to a Golangbased one increased the processing speed by 60x:

```
(python) root@localhost:~/Documents/PortfolioTracker$ time python3.8 portfolio_updater.py
real    0m24,727s
user    0m12,548s
sys     0m0,356s
```

```
(python) root@localhost:~/Documents/PortfolioTracker$ time ./portfolioUpdater portfolio.csv portfolio.db
real    0m0,413s
user    0m0,624s
sys     0m0,208s
````

2 main aspects get into play that explain the massive speed-up:
1. the Golang-based retriever is a compiled binary in comparison to the interpreted Python script 
2. the use of [goroutines](https://go.dev/tour/concurrency) allows for an easy concurrent processing of each asset price fetching. The same can be achieved using Python [Threads](https://docs.python.org/3/library/threading.html) or [asyncio](https://docs.python.org/3/library/asyncio.html#module-asyncio)

## Cross-compiling Golang binaries: x86 Linux (Docker on MacOS) to ARM64 Linux
In order to get the Golang binary for my [NVIDIA Jetson Nano](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-2gb-devkit) mini-computer, I need to cross-compile for that platform (unless I wanted to set up the Go dependencies there as well). I did this via the Golang Docker image and installing the [GNU ARM Toolchain](https://developer.arm.com/Tools%20and%20Software/GNU%20Toolchain) which contains a C-compiler.

```
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp golang:1.23 /bin/sh

apt-get update & apt-get install gcc-aarch64-linux-gnu 
env CC=aarch64-linux-gnu-gcc GOOS=linux GOARCH=arm64 CGO_ENABLED=1 go build -ldflags="-extldflags=-static" -o dist/portfolioUpdater 
```