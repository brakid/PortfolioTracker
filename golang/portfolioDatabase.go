package main

import (
	"context"
	"database/sql"

	_ "github.com/mattn/go-sqlite3"
)

func Store(portfolioRecords []*PortfolioRecord, file string) error {
	db, err := sql.Open("sqlite3", file)
	if err != nil {
		return err
	}
	defer db.Close()

	_, err = db.Exec("CREATE TABLE IF NOT EXISTS asset_prices(isin varchar(255), date varchar(255), price float, amount int, UNIQUE(isin, date));")
	if err != nil {
		return err
	}

	tx, _ := db.BeginTx(context.Background(), nil)
	for _, portfolioRecord := range portfolioRecords {
		_, err := tx.Exec("INSERT INTO asset_prices VALUES (?, ?, ?, ?);", portfolioRecord.Isin, portfolioRecord.Date, portfolioRecord.Price, portfolioRecord.Amount)
		if err != nil {
			return err
		}
	}
	err = tx.Commit()
	if err != nil {
		return err
	}

	return nil
}
