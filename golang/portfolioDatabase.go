package main

import (
	"context"
	"database/sql"
	"fmt"

	_ "github.com/mattn/go-sqlite3"
)

func Store(portfolioRecords []*PortfolioRecord, file string, table string) error {
	db, err := sql.Open("sqlite3", file)
	if err != nil {
		return err
	}
	defer db.Close()

	_, err = db.Exec(fmt.Sprintf("CREATE TABLE IF NOT EXISTS %s (isin varchar(255), date varchar(255), price float, amount int, UNIQUE(isin, date));", table))
	if err != nil {
		return err
	}

	tx, _ := db.BeginTx(context.Background(), nil)
	for _, portfolioRecord := range portfolioRecords {
		_, err := tx.Exec(fmt.Sprintf("INSERT INTO %s VALUES (?, ?, ?, ?);", table), portfolioRecord.Isin, portfolioRecord.Date, portfolioRecord.Price, portfolioRecord.Amount)
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
