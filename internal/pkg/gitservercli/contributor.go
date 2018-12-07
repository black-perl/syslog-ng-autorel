package gitservercli

import (
	"encoding/json"
)

type Contributor struct {
	username   string
	profileURL string
}

func newContributor(username string, profileURL string) Contributor {
	return Contributor{
		username:   username,
		profileURL: profileURL,
	}
}

func (c Contributor) getUsername() string {
	return c.username
}

func (c Contributor) getProfileURL() string {
	return c.profileURL
}

func (c Contributor) ToString() string {
	resp, _ := json.Marshal(c)
	return string(resp)
}
