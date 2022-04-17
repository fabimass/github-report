import requests
import os
import pandas as pd

df = pd.DataFrame(columns = ['Repo', 'Owner', 'Last Commit', 'Date'])

token = os.getenv('GITHUB_PAT', '...')

owner = "utn-fra-td3"
repo = "2022_td3_5xx_apellido"
query_url = f"https://api.github.com/repos/{owner}/{repo}/forks"
params = {
    'per_page': 100
}
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}
print(f'pulling forks for {repo}')
response = requests.get(query_url, headers=headers, params=params)

for repo in response.json():

    owner = repo['owner']['login']
    repo_name = repo['name']
    query_url = f"https://api.github.com/repos/{owner}/{repo_name}/commits/main"
    params = {
        'per_page': 100
    }
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    print(f'pulling last commit from {repo_name}')
    response = requests.get(query_url, headers=headers, params=params)
    commit = response.json()

    new_row = pd.DataFrame({'Repo' : repo['name'], 'Owner' : repo['owner']['login'], 'Last Commit': commit['commit']['message'], 'Date': commit['commit']['author']['date'][0:10]}, index=[0])
    df = pd.concat([new_row,df.loc[:]]).reset_index(drop=True)

print(df)

if not os.path.exists('./_report/'):
    os.makedirs('./_report/')
df.to_csv('_report/report.csv', index=False)