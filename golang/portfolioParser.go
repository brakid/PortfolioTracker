package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
)

func ReadPortfolioAssets(file string) ([]PortfolioAsset, error) {
	f, err := os.Open(file)
	if err != nil {
		log.Fatal(fmt.Sprintf("Unable to read input file %s", file), err)
	}
	defer f.Close()

	csvReader := csv.NewReader(f)
	csvReader.Comma = ';'
	_, err = csvReader.Read()
	if err != nil {
		return nil, err
	}
	records, err := csvReader.ReadAll()
	if err != nil {
		return nil, err
	}

	portfolio := make([]PortfolioAsset, len(records))

	for index, record := range records {
		isin := record[0]
		name := record[1]
		amountRaw, err := strconv.ParseFloat(record[2], 64)
		if err != nil {
			return nil, err
		}
		amountRaw = math.Round(amountRaw)
		amount := uint(amountRaw)
		portfolioPosition := PortfolioAsset{Isin: isin, Name: name, Amount: amount}
		portfolio[index] = portfolioPosition
	}

	return portfolio, nil
}
