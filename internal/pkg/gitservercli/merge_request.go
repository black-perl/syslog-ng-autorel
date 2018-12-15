package gitservercli

import (
	"encoding/json"
	"time"
)

type MergeRequest struct {
	Id          int64
	Title       string
	Body        string
	Labels      []string
	Contributor Contributor
	Url         string
	MergedAt    time.Time
}

func newMergeRequest(id int64, title string, body string, lables []string, contributor Contributor, url string, mergedAt time.Time) MergeRequest {
	return MergeRequest{
		Id:          id,
		Title:       title,
		Body:        body,
		Labels:      lables,
		Contributor: contributor,
		Url:         url,
		MergedAt:    mergedAt,
	}
}

func (mr MergeRequest) ToString() string {
	resp, _ := json.Marshal(mr)
	return string(resp)
}
