package main

import (
	"log"
	"sync"
)

func processAsset(portfolioAsset PortfolioAsset, wg *sync.WaitGroup, pChan chan *PortfolioRecord, eChan chan error) {
	defer wg.Done()
	log.Printf("Processing %v\n", portfolioAsset)
	portfolioRecord, err := ProcessPortfolioAsset(portfolioAsset)
	if err != nil {
		eChan <- err
		return
	}
	pChan <- portfolioRecord
}

func main() {
	portfolio, err := ReadPortfolioAssets("../portfolio.csv")
	if err != nil {
		log.Fatalf("Error while reading Portfolio file: %v", err)
	}

	log.Printf("Portfolio contains %v assets\n", len(portfolio))

	var wg sync.WaitGroup
	portfolioRecordChan := make(chan *PortfolioRecord, len(portfolio))
	errorChan := make(chan error, len(portfolio))

	for _, portfolioAsset := range portfolio {
		wg.Add(1)
		go processAsset(portfolioAsset, &wg, portfolioRecordChan, errorChan)
	}

	wg.Wait()
	close(portfolioRecordChan)
	close(errorChan)
	errorCount := 0
	for err := range errorChan {
		log.Printf("Error: %v\n", err)
		errorCount += 1
	}
	if errorCount > 0 {
		log.Fatalf("Encountered %v errors, stopping as complete data is needed\n", errorCount)
	}

	portfolioRecords := make([]*PortfolioRecord, len(portfolio))
	i := 0
	for portfolioRecord := range portfolioRecordChan {
		portfolioRecords[i] = portfolioRecord
		i += 1
	}

	err = Store(portfolioRecords, "portfolio.db")
	if err != nil {
		log.Fatalf("Error while storing Portfolio records: %v", err)
	}
}
