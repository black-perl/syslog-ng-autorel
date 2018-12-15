package gitservercli

import (
	"encoding/json"
)

type Contributor struct {
	Username   string
	ProfileURL string
}

func newContributor(username string, profileURL string) Contributor {
	return Contributor{
		Username:   username,
		ProfileURL: profileURL,
	}
}

func (c Contributor) ToString() string {
	resp, _ := json.Marshal(c)
	return string(resp)
}
