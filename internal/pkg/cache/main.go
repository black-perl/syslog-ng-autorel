package cache

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"sync"
	"time"

	"github.com/patrickmn/go-cache"
	"github.com/pkg/errors"
)

// Cache provides disk backed in-memory cache
type Cache struct {
	storage     *cache.Cache
	journalFile string
}

var cacheInstance *Cache
var once sync.Once

var (
	defaultItemExpirationTime = 24 * 60 * 7 * time.Minute
	defaultCleanUpInterval    = 10 * time.Minute

	// ItemExpirationTimeInMins provide the item expiration time
	ItemExpirationTimeInMins = "ITEM_EXPIRATION_TIME_IN_MINS"

	// CleanUpIntervalTimeInMins provide the item cleanup time after expiration
	CleanUpIntervalTimeInMins = "CLEAN_UP_INTERVAL_TIME_IN_MINS"
)

// New returns a configured Cache instance
func New(filename string, config map[string]string) (Cache, error) {
	var errorInInstantiation error
	once.Do(func() {
		// load the disk persisted cache
		bytesRead, err := ioutil.ReadFile(filename)
		if err != nil {
			errorInInstantiation = errors.Wrap(err, fmt.Sprintf("Not able to load cache from the file %s", filename))
		}
		var persistedCacheItems map[string]cache.Item
		json.Unmarshal(bytesRead, persistedCacheItems)

		// check if config is passed or not
		var itemExpirationTime, cleanUpInterval time.Duration
		val, ok := config[ItemExpirationTimeInMins]
		if ok {
			valStr, err := strconv.Atoi(val)
			if err != nil {
				errorInInstantiation = errors.Wrap(err, fmt.Sprintf("Not able to parse %s to integer provided as %s", val, ItemExpirationTimeInMins))
			} else {
				itemExpirationTime = time.Duration(valStr) * time.Minute
			}
		} else {
			itemExpirationTime = defaultItemExpirationTime
		}
		val, ok = config[CleanUpIntervalTimeInMins]
		if ok {
			valStr, err := strconv.Atoi(val)
			if err != nil {
				errorInInstantiation = errors.Wrap(err, fmt.Sprintf("Not able to parse %s to integer provided as %s", val, CleanUpIntervalTimeInMins))
			} else {
				cleanUpInterval = time.Duration(valStr) * time.Minute
			}
		} else {
			cleanUpInterval = defaultCleanUpInterval
		}
		cacheInstance = &Cache{
			storage:     cache.NewFrom(itemExpirationTime, cleanUpInterval, persistedCacheItems),
			journalFile: filename,
		}
	})
	return *cacheInstance, errorInInstantiation
}

// Put adds or replaces an entry in cache
func (c Cache) Put(key string, val interface{}) {
	c.storage.Set(key, val, 0) // use deafult expiration time
}

// Get a particular key
func (c Cache) Get(key string) (interface{}, bool) {
	return c.storage.Get(key)
}

// Delete a key
func (c Cache) Delete(key string) {
	c.storage.Delete(key)
}

// Flush the items in the cache
func (c Cache) Flush() {
	c.storage.Flush()
	os.Remove(c.journalFile)
}

// Persist all the items in the cache to the disk
func (c Cache) Persist() error {
	var cacheItems = c.storage.Items()
	serializedCacheItems, err := json.Marshal(cacheItems)
	if err != nil {
		return errors.Wrap(err, "Not able to unmarshall cache contents to json for disk persistance")
	}
	err = ioutil.WriteFile(c.journalFile, serializedCacheItems, os.FileMode(uint32(0777)))
	if err != nil {
		return errors.Wrap(err, fmt.Sprintf("Not able to persist cache items to disk file %s", c.journalFile))
	}
	return nil
}
