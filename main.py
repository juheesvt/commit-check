import requests
import datetime

def get_commits(user, repo, since, until):
    url=f"https://api.github.com/repos/{user}/{repo}/commits"
    params = {
        'since': since,
        'untile': until,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code
    

if __name__ == "__main__":

    user = "juheesvt"
    repo = "commit-check"
    since = datetime.datetime.now().date().isoformat() 
    until = (datetime.datetime.now() + datetime.timedelta(days=1)).date().isoformat()

    commits = get_commits(user, repo, since, until)
    print(commits)
