import requests, base64, json, getpass
from bs4 import BeautifulSoup

gitusername = input("Enter your github username\n")
pwd = getpass.getpass("Enter your github password\n")
print("Processing.......")
response = requests.get('https://api.github.com/', auth=(gitusername, pwd))
if response.status_code != 200:
    print("\n\n ***Check your github username and password !***\n\n")
    quit()
cf_handle = input("Enter your codeforces handle name\n")

response_codeforces = requests.get("http://codeforces.com/api/user.status", params={'handle': cf_handle})

if response_codeforces.status_code != 200:
    print("\n\n ***Please Check your codeforces handle name***\n\n")
    print(response_codeforces.json())
    quit()
else:
    print("Processing......")

repo_name = "Codeforces_Submissions"
data = {"name": repo_name, "auto_init": True, "private": True, "gitignore_template": "nanoc"}
response = requests.post('https://api.github.com/user/repos', auth=(gitusername, pwd), data=json.dumps(data))
if response.status_code != 200 and response.status_code != 201:
    print("\n\n ***Something went wrong .Please try again later !1***\n\n")
    print(
        "\n\n ***Please check if a repo with name " + repo_name + " already exists ?Delete if present and try again.***\n\n")
    print(response.json())
    quit()

submission_count = 0
dict = response_codeforces.json()
for x in dict['result']:
    if (x['verdict'] != 'OK'):
        continue
    pid = x['id']
    contestId = x['problem']['contestId']
    html = BeautifulSoup(
        requests.get("http://codeforces.com/contest/" + str(contestId) + "/submission/" + str(pid)).content,
        "html.parser")
    try:
        html = html.select_one("#program-source-text").get_text()
    except AttributeError:
        continue
    html = base64.b64encode(bytes(html, 'utf-8'))
    data = {"message": "Initial Commit",
            "content": html.decode('utf-8'),
            }
    filename = x['problem']['name'] + " - " + str(pid)
    response = requests.put(
        'https://api.github.com/repos/' + gitusername + '/' + repo_name + '/contents/' + filename + ".txt",
        auth=(gitusername, pwd), data=json.dumps(data))
    if response.status_code != 200 and response.status_code != 201:
        print("\n\n ***Something went wrong .Please try again later !3***\n\n")
        print(response.json())
        quit()
    else:
        print("OK.....")
    submission_count += 1

print("Total ", submission_count, " number of files copied ! \n")
