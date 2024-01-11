import requests
import datetime
import pytz
import os

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
    

def send_message_to_discord(time, commits, no_commit_users):
    webhook_url = os.environ["WEBHHOK_URL"]
    message = f"""**✅ {time.year}년 {time.month}월 {time.day} 기준 알고리즘 미제출자**\n"""
    for user in no_commit_users:
        message += f"- **{user['user']}**\n"

    message += """\n✅ **알고리즘 저장소 커밋 내역**\n"""

    for commit in commits:
        message += f"- **{commit['author']['login']}** {commit['commit']['message']}\n"
     
    data = {"content": message}
    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("메시지가 성공적으로 전송되었습니다.")
    else:
        print("메시지 전송 실패.")
    

if __name__ == "__main__":

    user_list = [
        {
            "user": "juheesvt",
            "repo": "algorithm",
        },
        {
            "user": "jihyun-Yun42",
            "repo": "Algorithm",
        },
        {
            "user": "sweetyr928",
            "repo": "JS-algorithm",
        },
        {
            "user": "Ljinyh",
            "repo": "codingTest",
        },
        {
            "user": "E-ppo",
            "repo": "codingTest_JS",
        },
        {
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

    # 'since'를 오늘 UTC 시간으로 설정
    since = utc_time.date().isoformat()
    # 'until'을 내일 UTC 시간으로 설정
    until = (utc_time + datetime.timedelta(days=1)).date().isoformat()

    print(since, until, local_time, utc_time)

    commits = []
    no_commit_users = []
    for user in user_list:
        commit = get_commits(user["user"], user["repo"], since, until)

        if not commit:
            no_commit_users.append(user)
        else:
            commits.append(commit[-1])

    send_message_to_discord(utc_time, commits, no_commit_users)

