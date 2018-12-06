package gitservercli

import (
	"encoding/json"
	"time"
)

type MergeRequest struct {
	id          int64
	title       string
	body        string
	labels      []string
	contributor Contributor
	url         string
	mergedAt    time.Time
}

func newMergeRequest(id int64, title string, body string, lables []string, contributor Contributor, url string, mergedAt time.Time) MergeRequest {
	return MergeRequest{
		id:          id,
		title:       title,
		body:        body,
		labels:      lables,
		contributor: contributor,
		url:         url,
		mergedAt:    mergedAt,
	}
}

func (mr MergeRequest) GetID() int64 {
	return mr.id
}

func (mr MergeRequest) GetTitle() string {
	return mr.title
}

func (mr MergeRequest) GetBody() string {
	return mr.body
}

func (mr MergeRequest) GetLabels() []string {
	return mr.labels
}

func (mr MergeRequest) GetContributor() Contributor {
	return mr.contributor
}

func (mr MergeRequest) GetURL() string {
	return mr.url
}

func (mr MergeRequest) GetMergedTime() time.Time {
	return mr.mergedAt
}

func (mr MergeRequest) ToString() string {
	resp, _ := json.Marshal(mr)
	return string(resp)
}
