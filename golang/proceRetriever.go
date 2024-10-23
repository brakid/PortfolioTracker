package main

import (
	"fmt"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/go-shiori/dom"
	"golang.org/x/net/html"
)

func getPrice(isin string) (float32, error) {
	client := &http.Client{}

	req, err := http.NewRequest("GET", fmt.Sprintf("https://www.finanzen.net/suchergebnis.asp?_search=%s", isin), nil)
	if err != nil {
		return -1.0, err
	}
	req.Header.Add("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0")
	resp, err := client.Do(req)
	if err != nil {
		return -1.0, err
	}

	defer resp.Body.Close()

	doc, err := html.Parse(resp.Body)
	if err != nil {
		return -1.0, err
	}

	node := dom.QuerySelector(doc, "span.snapshot__value")
	priceText := dom.InnerText(node)

	price, err := strconv.ParseFloat(strings.Replace(priceText, ",", ".", 1), 32)
	if err != nil {
		return -1.0, err
	}

	return float32(price), nil
}

func ProcessPortfolioAsset(portfolioAsset PortfolioAsset) (*PortfolioRecord, error) {
	price, err := getPrice(portfolioAsset.Isin)
	if err != nil {
		return nil, err
	}

	currentDate := time.Now().Local().Format("2006-01-02")

	return &PortfolioRecord{Isin: portfolioAsset.Isin, Amount: portfolioAsset.Amount, Price: price, Date: currentDate}, nil
}
