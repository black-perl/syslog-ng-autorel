package gitservercli

import (
	"context"
	"fmt"

	"github.com/google/go-github/github"
	"github.com/pkg/errors"
	"golang.org/x/oauth2"
)

var (
	gitServerAPIAccessToken string
)

type GitServerCli struct {
	maskedServerClient *github.Client
}

func NewGitServerClient(accessToken string) *GitServerCli {
	gitServerAPIAccessToken = accessToken
	return &GitServerCli{}
}

func (gsc *GitServerCli) setupMaskedGitServerClient(gitServerAPIAccessToken string, ctx context.Context) {
	tokenSource := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: gitServerAPIAccessToken},
	)
	transportClient := oauth2.NewClient(ctx, tokenSource)
	gsc.maskedServerClient = github.NewClient(transportClient)
}

func (gsc *GitServerCli) GetMergeRequest(ctx context.Context, user string, repo string, pullRequestId int) (MergeRequest, error) {
	var mergeRequest MergeRequest
	gsc.setupMaskedGitServerClient(gitServerAPIAccessToken, ctx)
	gitServerPullRequest, _, err := gsc.maskedServerClient.PullRequests.Get(ctx, user, repo, pullRequestId)
	if err != nil {
		return mergeRequest, errors.Wrap(err, fmt.Sprintf("Fetching merge request with id : %d failed for repository %s/%s", pullRequestId, user, repo))
	}
	// convert the gitServerPullRequest to MergeRequest
	gitServerUser := gitServerPullRequest.User
	contributor := newContributor(*gitServerUser.Login, *gitServerUser.HTMLURL)
	labels := make([]string, len(gitServerPullRequest.Labels))
	for _, elem := range gitServerPullRequest.Labels {
		labels = append(labels, *elem.Name)
	}
	mergeRequest = newMergeRequest(*gitServerPullRequest.ID, *gitServerPullRequest.Title, *gitServerPullRequest.Body, labels, contributor, *gitServerPullRequest.HTMLURL, *gitServerPullRequest.MergedAt)
	return mergeRequest, nil
}
