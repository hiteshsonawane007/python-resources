from github import Github
g = Github(base_url="https://url/api/v3", login_or_token='token')
repo = g.get_repo("gts-mft/mft-selfservice")
print(repo)