package main

type PortfolioAsset struct {
	Name   string
	Isin   string
	Amount uint
}

type PortfolioRecord struct {
	Isin   string
	Amount uint
	Price  float32
	Date   string
}
