# Portfolio Tracker

* portfolio overview: *name*, *isin* and *amount* of the assets in file ```portfolio.csv````
* daily [Cron job](https://en.wikipedia.org/wiki/Cron) to update the asset prices using website [Finanzen.net](https://finanzen.net)
  * ```0 21 * * * cd /path/to/script; python3.6 portfolio_updater.py >/dev/null 2>&1
* stores daily snapshots (*isin*, *amount*, *price* and *date*) in an [SQLite Database](https://www.sqlite.org/) file ```portfolio.db```
* runs as a [Streamlit App](https://docs.streamlit.io/): allows modifying the portfolio (e.g when buying or selling assets) and displays the portfolio development over time