package gitservercli

import (
	"context"
	"fmt"

	"github.com/google/go-github/github"
	"github.com/pkg/errors"
	"golang.org/x/oauth2"
)

var (
	accessToken string
)

type GitServerCli struct {
	maskedServerClient *github.Client
}

func New(authenticationToken string) *GitServerCli {
	accessToken = accessToken
	return &GitServerCli{}
}

func (gsc *GitServerCli) setupMaskedGitServerClient(accessToken string, ctx context.Context) {
	tokenSource := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: accessToken},
	)
	transportClient := oauth2.NewClient(ctx, tokenSource)
	gsc.maskedServerClient = github.NewClient(transportClient)
}

func (gsc *GitServerCli) GetMergeRequest(ctx context.Context, user string, repo string, pullRequestId int) (MergeRequest, error) {
	var mergeRequest MergeRequest
	gsc.setupMaskedGitServerClient(accessToken, ctx)
	gitServerPullRequest, _, err := gsc.maskedServerClient.PullRequests.Get(ctx, user, repo, pullRequestId)
	if err != nil {
		return mergeRequest, errors.Wrap(err, fmt.Sprintf("Fetching merge request with id : %d failed for repository %s/%s", pullRequestId, user, repo))
	}
	// convert the gitServerPullRequest to MergeRequest
	gitServerUser := gitServerPullRequest.User
	contributor := newContributor(*gitServerUser.Login, *gitServerUser.Name, *gitServerUser.Email, *gitServerUser.HTMLURL)
	labels := make([]string, len(gitServerPullRequest.Labels))
	for _, elem := range gitServerPullRequest.Labels {
		labels = append(labels, *elem.Name)
	}
	mergeRequest = newMergeRequest(*gitServerPullRequest.ID, *gitServerPullRequest.Title, *gitServerPullRequest.Body, labels, contributor, *gitServerPullRequest.URL, *gitServerPullRequest.MergedAt)
	return mergeRequest, nil
}
