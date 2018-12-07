package cache

import (
	"encoding/gob"
	"fmt"
	"os"
	"sync"
	"time"

	"github.com/patrickmn/go-cache"
	"github.com/pkg/errors"
)

// Cache provides disk backed in-memory cache
type Cache struct {
	storage       *cache.Cache
	journalFile   string
	mutex         sync.RWMutex
	cachableTypes []interface{}
}

var cacheInstance *Cache
var once sync.Once

var (
	defaultItemExpirationTime = 24 * 60 * 7 * time.Minute
	defaultCleanUpInterval    = 10 * time.Minute
)

// NewCache returns a Cache instance
func NewCache(filename string, cachableTypes []interface{}) (*Cache, error) {
	var errorInInstantiation error
	once.Do(func() {
		// register the types for decoding by gob
		for _, cachable := range cachableTypes {
			gob.Register(cachable)
		}
		// load the disk persisted cache
		persistedCacheItems := make(map[string]cache.Item)
		diskCacheFile, err := os.OpenFile(filename, os.O_RDONLY|os.O_CREATE, 0666)
		if err != nil {
			errorInInstantiation = errors.Wrap(err, fmt.Sprintf("Not able to open journal file %s for reading persisted cache items", filename))
		}
		dec := gob.NewDecoder(diskCacheFile)
		err = dec.Decode(&persistedCacheItems)
		if err != nil && err.Error() != "EOF" {
			errorInInstantiation = errors.Wrap(err, fmt.Sprintf("Not able to decode the cache from the file %s", filename))
		}
		cacheInstance = &Cache{
			storage:       cache.NewFrom(defaultItemExpirationTime, defaultCleanUpInterval, persistedCacheItems),
			journalFile:   filename,
			cachableTypes: cachableTypes,
		}
	})
	return cacheInstance, errorInInstantiation
}

// NewCacheWithDefaults returns a configured Cache instance
func NewCacheWithDefaults(filename string, cachableTypes []interface{}, itemExpirationTime time.Duration, cleanUpInterval time.Duration) (*Cache, error) {
	var errorInInstantiation error
	once.Do(func() {
		// register the types for decoding by gob
		for _, cachable := range cachableTypes {
			gob.Register(cachable)
		}
		// load the disk persisted cache
		diskCacheFile, err := os.OpenFile(filename, os.O_RDONLY|os.O_CREATE, 0666)
		if err != nil {
			errorInInstantiation = errors.Wrap(err, fmt.Sprintf("Not able to load cache from the file %s", filename))
		}
		var persistedCacheItems map[string]cache.Item
		dec := gob.NewDecoder(diskCacheFile)
		err = dec.Decode(&persistedCacheItems)
		if err != nil {
			errorInInstantiation = errors.Wrap(err, fmt.Sprintf("Not able to decode the cache from the file %s", filename))
		}
		cacheInstance = &Cache{
			storage:       cache.NewFrom(itemExpirationTime, cleanUpInterval, persistedCacheItems),
			journalFile:   filename,
			cachableTypes: cachableTypes,
		}
	})
	return cacheInstance, errorInInstantiation
}

// Put adds or replaces an entry in cache
func (c *Cache) Put(key string, val interface{}) {
	c.storage.Set(key, val, 0) // use deafult expiration time
}

// Get a particular key
func (c *Cache) Get(key string) (interface{}, bool) {
	return c.storage.Get(key)
}

// Delete a key
func (c *Cache) Delete(key string) {
	c.storage.Delete(key)
}

// Flush the items in the cache
func (c *Cache) Flush() {
	c.mutex.Lock()
	defer c.mutex.Unlock()
	c.storage.Flush()
	os.Remove(c.journalFile)
}

// Persist all the items in the cache to the disk
func (c *Cache) Persist() error {
	c.mutex.Lock()
	defer c.mutex.Unlock()
	// encode the cache items
	diskCacheFile, err := os.OpenFile(c.journalFile, os.O_RDWR, 0600)
	if err != nil {
		return errors.Wrap(err, fmt.Sprintf("Not able to open journal file %s for persisting cache", c.journalFile))
	}
	cacheItems := c.storage.Items()
	enc := gob.NewEncoder(diskCacheFile)
	err = enc.Encode(cacheItems)
	if err != nil {
		return errors.Wrap(err, fmt.Sprintf("Not able to persist cache items to journal file %s", c.journalFile))
	}
	return nil
}

func (c *Cache) RegisterCachableType(cachable interface{}) {
	c.cachableTypes = append(c.cachableTypes, cachable)
}
