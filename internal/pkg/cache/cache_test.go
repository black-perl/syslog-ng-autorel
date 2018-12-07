package cache

import (
	"os"
	"testing"
)

type student struct {
	Name   string
	RollNo int
}

// These tests are required to be executed one by one
// because of the singleton instance

func TestPersist(t *testing.T) {
	// instantiate cache
	k := []interface{}{}
	k = append(k, student{})
	cache, err := NewCache("./temp", k)
	if err != nil {
		panic(err)
	}

	cacheJournalFile, _ := os.Open("./temp")
	fileInfo, err := cacheJournalFile.Stat()
	if err != nil {
		t.Error("Not able to get the journal file information")
		panic(err)
	} else {
		if fileInfo.Size() > 0 {
			t.Error("Cache file has already some contents, clean it and rerun")
		}
	}
	cacheJournalFile.Close()

	entry1 := student{
		Name:   "peter",
		RollNo: 3,
	}
	entry2 := student{
		Name:   "parker",
		RollNo: 4,
	}

	//Put
	cache.Put("student1", entry1)
	cache.Put("student2", entry2)

	//Persist
	err = cache.Persist()
	if err != nil {
		panic(err)
	}

	cacheJournalFile, _ = os.Open("./temp")
	fileInfo, err = cacheJournalFile.Stat()
	if err != nil {
		t.Error("Not able to get the journal file information")
		panic(err)
	} else {
		if fileInfo.Size() == 0 {
			t.Error("JournalFile has still size 0")
		}
	}
	cacheJournalFile.Close()

	// clean up
	cache.Flush()
}

func TestPutAndGet(t *testing.T) {
	// instantiate cache
	k := []interface{}{}
	k = append(k, student{})
	cache, err := NewCache("./temp", k)
	if err != nil {
		panic(err)
	}

	entry := student{
		Name:   "peter",
		RollNo: 3,
	}

	// Put
	cache.Put("student", entry)

	// Get
	resp, _ := cache.Get("student")
	expectedEntry := resp.(student)
	if expectedEntry != entry {
		t.Error("Test failed")
	}

	// clean up
	cache.Flush()
}

func TestFlush(t *testing.T) {
	// instantiate cache
	k := []interface{}{}
	k = append(k, student{})
	cache, err := NewCache("./temp", k)
	if err != nil {
		panic(err)
	}

	entry := student{
		Name:   "peter",
		RollNo: 3,
	}

	// Put
	cache.Put("student", entry)

	// Flush
	cache.Flush()

	// Get
	_, isFound := cache.Get("student")
	if isFound {
		t.Error("Test failed")
	}
}
