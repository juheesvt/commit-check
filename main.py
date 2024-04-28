import requests
import datetime
import pytz
import os
from pprint import pprint


def get_commits(user, repo, since, until):
    url = f"https://api.github.com/repos/{user}/{repo}/commits"
    params = {
        'since': since,
        'until': until,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def send_message_to_discord(users, start_time, end_time):
    webhook_url = os.environ["WEBHOOK_URL"]
    message = f"""**✅ {start_time.year}년 {start_time.month}월 {start_time.day}일 ~ {end_time.year}년 {end_time.month}월 {end_time.day}일 기준 알고리즘 제출 목록**\n"""
    message += "\n"
    
    pprint(users)
    for user in users:

        problem_count = 0
        for date in user['commit_list'].keys():
            problem_count += len(user['commit_list'][date])
        message += f"\n- **{user['name']}** : {problem_count} 문제\n"

        for date, commit_list in user["commit_list"].items():
            message += f"  - {date} : \n"
            for commit in commit_list:
                message += f"    - {commit}\n"

        data = {"content": message}
        response = requests.post(webhook_url, json=data)

        if response.status_code == 204:
            print("메시지가 성공적으로 전송되었습니다.")
        else:
            print(f"메시지 전송 실패: {response}")

        message = ""

    message += """\n **벌금 제출자 **\n"""

    count = 0
    for user in users:
        if user["count"] < 3:
            message += f"- **{user['name']}** : {(3 - user['count']) * 1000} 원\n"
            count += 1

    if count == 0:
        message += "이번주 벌금 제출자 없음 🎉🎉🎉\n"
    message += "\n\n"

    data = {"content": message}
    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("메시지가 성공적으로 전송되었습니다.")
    else:
        print(f"메시지 전송 실패: {response}")
     

if __name__ == "__main__":

    user_list = [
        {
            "name": "강주희",
            "user": "juheesvt",
            "repo": "algorithm",
            "commit_list": {},
            "count": 0,
        },
        {
            "name": "윤지현",
            "user": "jihyun-Yun42",
            "repo": "Algorithm",
            "commit_list": {},
            "count": 0
        },
        {
            "name": "전예린",
            "user": "sweetyr928",
            "repo": "JS-algorithm",
            "commit_list": {},
            "count": 0
        },
        {
            "name": "최지훈",
            "user": "ChoiJi92",
            "repo": "algorithm",
            "commit_list": {},
            "count": 0
        },
        {
            "name": "이보람",
            "user": "E-ppo",
            "repo": "Algorithm",
            "commit_list": {},
            "count": 0
        },
        {
            "name": "백경렬",
            "user": "KyungRyeolBaek",
            "repo": "Baekjoon",
            "commit_list": {},
            "count": 0
        },
    ]

    # UTC 시간대로 날짜와 시간 설정
    utc_zone = pytz.utc
    local_zone = pytz.timezone('Asia/Seoul')  # 예시로 서울 시간대 사용

    # 현재 시간을 서울 시간대로 설정하고 UTC로 변환
    today = datetime.datetime.now(local_zone)

    week_time_list = []
    for i in range(7, 0, -1):
        local_since_time = datetime.datetime.now(local_zone).replace(day=today.day-i, hour=0, minute=0, second=0, microsecond=0)
        local_until_time = datetime.datetime.now(local_zone).replace(day=today.day-i, hour=23, minute=59, second=59, microsecond=999999)

        utc_since_time = local_since_time.astimezone(utc_zone)
        utc_until_time = local_until_time.astimezone(utc_zone)

        week_time_list.append({
            "since_time": utc_since_time,
            "until_time": utc_until_time,
        })

    start_time = week_time_list[0]['since_time'].astimezone(local_zone)
    end_time = week_time_list[-1]['until_time'].astimezone(local_zone)

    print(f"{start_time} ~ {end_time}")

    for day in week_time_list:
        current_date = day["since_time"].astimezone(local_zone)
        for user in user_list:
            commits = get_commits(user["user"], user["repo"], day["since_time"], day["until_time"])

            if not commits:
                continue
            else:
                for commit in commits:
                    if "Title" not in commit['commit']['message']:
                        continue

                    if current_date.date() not in user["commit_list"].keys():
                        user["commit_list"][current_date.date()] = []
                        user["commit_list"][current_date.date()].append(commit['commit']['message'])

    for user in user_list:
        user['count'] = len(user['commit_list'].keys())
        print(f"{user['name']} : {user['count']}")

    send_message_to_discord(user_list, start_time, end_time)
