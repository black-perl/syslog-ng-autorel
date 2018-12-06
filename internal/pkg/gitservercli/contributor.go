package gitservercli

import (
	"encoding/json"
)

type Contributor struct {
	username   string
	name       string
	email      string
	profileURL string
}

func newContributor(username string, name string, email string, profileURL string) Contributor {
	return Contributor{
		username:   username,
		name:       name,
		email:      email,
		profileURL: profileURL,
	}
}

func (c Contributor) getUsername() string {
	return c.username
}

func (c Contributor) getEmail() string {
	return c.email
}

func (c Contributor) getProfileURL() string {
	return c.profileURL
}

func (c Contributor) getName() string {
	return c.name
}

func (c Contributor) ToString() string {
	resp, _ := json.Marshal(c)
	return string(resp)
}
