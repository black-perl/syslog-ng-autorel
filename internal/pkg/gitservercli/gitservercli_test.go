package gitservercli

import (
	"context"
	"testing"
)

func TestGetMergeRequest(t *testing.T) {
	accessToken := "<access-token-here"
	gcli := NewGitServerClient(accessToken)
	ctx := context.Background()
	mr, err := gcli.GetMergeRequest(ctx, "balabit", "syslog-ng", 2408)
	if err != nil {
		t.Errorf("Error occured in fetching merge request %v", err)
	}
	t.Log(mr)
}
