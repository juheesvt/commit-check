import requests
import datetime
import pytz

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

    user_list = [
        {
            "name": "강주희",
            "user": "juheesvt",
            "repo": "algorithm",
        },
        {
            "name": "윤지현",
            "user": "jihyun-Yun42",
            "repo": "Algorithm",
        },
        {
            "name": "전예린",
            "user": "sweetyr928",
            "repo": "JS-algorithm",
        },
        {
            "name": "이진희",
            "user": "Ljinyh",
            "repo": "codingTest",
        },
        {
            "name": "이보람",
            "user": "E-ppo",
            "repo": "codingTest_JS",
        },
        {
            "name": "백경렬",
            "user": "KyungRyeolBaek",
            "repo": "Baekjoon",
        },
    ]

    # UTC 시간대로 날짜와 시간 설정
    utc_zone = pytz.utc
    local_zone = pytz.timezone('Asia/Seoul')  # 예시로 서울 시간대 사용

    # 현재 시간을 서울 시간대로 설정하고 UTC로 변환
    local_time = datetime.datetime.now(local_zone)
    utc_time = local_time.astimezone(utc_zone)

    # 'since'를 어제의 UTC 시간으로 설정
    since = (utc_time - datetime.timedelta(days=1)).date().isoformat()
    # 'until'을 오늘의 UTC 시간으로 설정
    until = utc_time.date().isoformat()


    no_commit_users = []
    for user in user_list:
        commits = get_commits(user["user"], user["repo"], since, until)
        if not commits:
            no_commit_users.append(user)

    for user in no_commit_users:
        print(user["name"], end=" ")

