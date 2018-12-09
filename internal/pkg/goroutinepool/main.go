package goroutinepool

// Inspired by https://github.com/gobwas/ws-examples/tree/master/src/gopool

import (
	"time"

	"github.com/pkg/errors"
)

// ErrScheduleTimeout to indicate that there are no goroutines available to process
var ErrScheduleTimeout = errors.New("schedule error: timed out")

// GoRoutinePool contains logic of goroutine reuse.
type GoRoutinePool struct {
	semaphore chan struct{} // for controlling maximum number of workers that can be run
	workQueue chan func()   // work queue carrying the work payload
}

// NewGoRoutinePool creates a new go routine pool with spawn number of
// workers running initially
func NewGoRoutinePool(poolSize, queueSize, spawn int) *GoRoutinePool {
	if spawn <= 0 && queueSize > 0 {
		panic("Dead queue configuration detected as no workers to process the work queue")
	}
	if spawn > poolSize {
		panic("spawn > max workers")
	}
	pool := &GoRoutinePool{
		semaphore: make(chan struct{}, poolSize),
		workQueue: make(chan func(), queueSize),
	}
	for i := 0; i < spawn; i++ {
		pool.semaphore <- struct{}{}
		go pool.worker(func() {})
	}

	return pool
}

// Schedule schedules task to be executed over pool's workers.
func (pool *GoRoutinePool) Schedule(task func()) {
	pool.schedule(task, nil)
}

// ScheduleTimeout schedules task to be executed over pool's workers.
// It returns ErrScheduleTimeout when no free workers met during given timeout.
func (pool *GoRoutinePool) ScheduleTimeout(timeout time.Duration, task func()) error {
	return pool.schedule(task, time.After(timeout))
}

func (pool *GoRoutinePool) schedule(task func(), timeout <-chan time.Time) error {
	select {
	case <-timeout:
		return ErrScheduleTimeout
	case pool.workQueue <- task:
		return nil
	case pool.semaphore <- struct{}{}:
		go pool.worker(task)
		return nil
	}
}

func (pool *GoRoutinePool) worker(task func()) {
	defer func() { <-pool.semaphore }()
	task()

	for task := range pool.workQueue {
		task()
	}
}
