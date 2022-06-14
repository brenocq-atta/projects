import os
import json
from pathlib import Path
from datetime import datetime

issueUser = os.environ['ISSUE_USER']
issueBody = os.environ['ISSUE_BODY']
timeAdded = datetime.now().isoformat()

def addRequest(repo, user, timestamp):
    projectsFile = Path(__file__).parent.parent.with_name('projects.json')
    with open(projectsFile) as f:
        projectsDict = json.load(f)
    with open(projectsFile, 'w') as f:
        projectsDict['projects'].append({
            'repo': repo,
            'user': user,
            'timestamp': timestamp
        })
        json.dump(projectsDict, f, indent=4)

def processRequest(body, username, timestamp):
    # Parse repo github path
    repo = body.split('**Github repository**\n')[1].split('\n')[0]

    # Add request
    addRequest(repo, username, timestamp)

    # Build project path
    projectPath = repo.split('https://github.com/')[1]
    if projectPath[-1] == '/':
        projectPath = projectPath[:-1]
    return projectPath

projectPath = processRequest(issueBody, issueUser, timeAdded)
print("PROJECT_PATH="+projectPath)
