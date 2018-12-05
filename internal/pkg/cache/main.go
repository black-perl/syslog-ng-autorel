package cache

import (
	"os"
	"encoding/json"
	"io/ioutil"
	"sync"
	"time"
	"github.com/patrickmn/go-cache"
)

type Cache struct {
	storage *cache.Cache
	journalFile string
}

var cacheInstance *Cache = nil
var once sync.Once

type CacheItem struct {
    Object     interface{}
    Expiration int64
}

// Constructor
func New(filename string) Cache {
	once.Do(func() {
		// load the disk persisted cache 
		bytesRead, err := ioutil.ReadFile(filename)
		if err != nil {
			//  in case the file is not found, we don't panic
		}
		var persistedCacheItems map[string]CacheItem
		json.Unmarshal(bytesRead,persistedCacheItems)
		cacheInstance = &Cache{
			storage : cache.NewFrom(5*time.Minute, 10*time.Minute,persistedCacheItems)
			journalFile : filename
		}

	})
}

// Add or replace an entry in cache
func (c Cache) Put(key string, val interface{}) {
	c.storage.Set(key,val)
}

// Get a particular key
func (c Cache) Get(key string) (interface{},bool) {
	return c.storage.Get(key)
}

// Delete a key
func (c Cache) Delete(key string) (string,bool) {
	c.storage.Delete(key)
}

// Purge the cache
func (c Cache) Flush() {
	c.storage.Flush()
	os.Remove(c.journalFile)
}

// Persists all the items in the cache to the disk
func (c Cache) Persist() {
	var cacheItems map[string]CacheItem = c.storage.Items()
	serializedCacheItems := json.Marshal(cacheItems)
	err:= ioutil.WriteFile(c.journalFile,serializedCacheItems,os.FileMode(uint32(0777)))
	if err != nil {
		// Don't panic at all
	}
}