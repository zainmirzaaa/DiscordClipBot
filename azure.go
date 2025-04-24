package main

import "fmt"

func fetchFromAzure(container string) []string {
	// TODO: replace with SDK calls
	fmt.Println("fetching clips from Azure container:", container)
	return []string{
		"https://azure.blob/mock1.mp4",
		"https://azure.blob/mock2.mp4",
	}
}
