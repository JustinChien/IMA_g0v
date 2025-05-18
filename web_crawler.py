from github import Github
import csv
import requests
import json
import time
import logging


logging.basicConfig(
    filename='web_crawler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)



# 初始化 GitHub API (需申請 personal access token)
# Justin Chien : web crewler use
GITHUB_TOKEN = "placeholder"
g = Github(GITHUB_TOKEN)

def get_repo_info(owner, repo):
    """使用 GitHub API 獲取 repo 資訊"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 404:
            logging.warning(f"Repository {owner}/{repo} not found")
            return False, None
        else:
            logging.error(f"Error accessing {owner}/{repo}: Status code {response.status_code}")
            logging.error(f"Response: {response.text}")
            return False, None
    except Exception as e:
        logging.error(f"Exception while accessing {owner}/{repo}: {str(e)}")
        return False, None

def get_contributors(owner, repo):
    """獲取 repo 的貢獻者資訊"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            logging.warning(f"No contributors found for {owner}/{repo}")
            return None
        else:
            logging.error(f"Error getting contributors for {owner}/{repo}: Status code {response.status_code}")
            logging.error(f"Response: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Exception while getting contributors for {owner}/{repo}: {str(e)}")
        return None

def get_user_info(username):
    """獲取用戶詳細資訊"""
    url = f"https://api.github.com/users/{username}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            logging.warning(f"User {username} not found")
            return None
        else:
            logging.error(f"Error getting user info for {username}: Status code {response.status_code}")
            logging.error(f"Response: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Exception while getting user info for {username}: {str(e)}")
        return None

def get_user_contributions(owner, repo, username):
    """獲取用戶在特定 repo 的詳細貢獻資訊"""
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for contributor in data:
                if contributor['author']['login'] == username:
                    return contributor
            logging.warning(f"No contribution data found for {username} in {owner}/{repo}")
            return None
        elif response.status_code == 404:
            logging.warning(f"No contribution stats found for {owner}/{repo}")
            return None
        else:
            logging.error(f"Error getting contribution stats for {owner}/{repo}: Status code {response.status_code}")
            logging.error(f"Response: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Exception while getting contribution stats for {owner}/{repo}: {str(e)}")
        return None

da_list = {
    "hackfoldr-2.0" : "hackfoldr",
    "dev-env" : "ronnywang",
    "ideapool" : "tka",
    "g0vphotos" : "zbryikt",
    "metadata-editor" : "poga",
    "axe.g0v.tw" : "ronnywang",
    "coVerbatim" : "jessy1092",
    "quick-timer" : "zbryikt",
    "goban" : "bestian",
    "tw-court-parser" : "ronnywang",
    "extract_declared_sentence" : "superChing",
    "taiwan-cabinet" : "ronnywang",
    "dgbas.gov.tw" : "kiang",
    "tommy87166.github.io" : "tommy87166",
    "soidid.github.io" : "soidid",
    "elections" : "kiang",
    "wp2014s_final_project" : "frank00125",
    "vote2014" : ["ctiml", "ronnywang"],
    "cf-viz" : "fuyei",
    "g0v" : "chungcheng",
    "campaign-finance.g0v.ronny.tw" : "ronnywang",
    "tw-campaign-finance" : "ronnywang",
    "campaign-finance.g0v.ctiml.tw" : "ctiml",
    "councilor2014.github.io" : "councilor2014",
    "tncc" : "kiang",
    "taipei-pop" : "dz1984",
    "taipei-building-has-reward" : "cades",
    "taiwan-address-lookup" : "ronnywang",
    "data.g0v.ronny.tw" : "ronnywang",
    "Real-time-Air-Quality-Map" : "immortalmice",
    "twlandsat-browse" : "jimyhuang",
    "cacci-opendata" : "Drainet",
    "visualize" : "zbryikt",
    "mrt" : "zbryikt",
    "ecolife.epa.gov.tw" : "ronnywang",
    "lead_pipes" : "kiang",
    "visualize" : "zbryikt",
    "drinking_water" : "teia-tw",
    "amis-safolu" : "miaoski",
    "amis-francais" : "miaoski",
    "moe" : "andreyt",
    "salary" : "kiang",
    "jobhelper" : "ronnywang",
    "jobhelper-mobile" : "nansenat16",
    "jobhelper_ff" : "yisheng-liu",
    "jobhelper-ie" : "nansenat16",
    "fepztw" : "", #https://github.com/fepztw
    "pcc" : "mlwmlw",
    "twcompany" : "ronnywang",
    "billy3321.github.io" : "billy3321",
    "open_crops" : "a0726h77",
    "chimney_map" : "kiang",
    "sheethub" : "", #https://sheethub.com/
    "ly-tel" : ["junsuwhy", "chilijung"],
    "boycott-helper" : "zhusee2",
    "BatDrone" : "kevinphys",
    "iHelp-android" : "weitsai",
    "petneed.me" : "jsleetw",
    "g8v" : "a0000778",
    "inLiveTW" : "", #https://github.com/inLiveTW
    "4movement" : "", #https://github.com/4movement
    "newsdiff" : "ronnywang",
    "bifrostio" : "", #https://github.com/bifrostio
    "MuscidaeFlash" : "ddio",
    "Solveissues" : "jcsky",
    "ncc-complain-data" : "godgunman",
    "news-seg" : "yonchenlee",
    "newstrend.g0v.ronny.tw" : "ronnywang",
    "linkCollector" : "lanfon72",
    "lagnews" : "ronnywang",
    "ppllink" : "zbryikt",
    "newshelper-safari" : "yllan",
}

def process_contributor(contributor, repo_name, owner, repo_data, writer):
    """Process a single contributor and write their data to CSV"""
    logging.info(f"Processing contributor {contributor['login']} for {owner}/{repo_name}")
    
    # Get contributor details
    user_info = get_user_info(contributor['login'])
    if not user_info:
        logging.warning(f"Could not get user info for {contributor['login']}")
    
    contribution_stats = get_user_contributions(owner, repo_name, contributor['login'])
    if not contribution_stats:
        logging.warning(f"Could not get contribution stats for {contributor['login']} in {owner}/{repo_name}")
    
    # Prepare data for CSV
    row_data = {
        # Repo 資訊
        'repo': repo_name,
        'owner': owner,
        'repo_url': f"https://github.com/{owner}/{repo_name}",
        'repo_description': repo_data.get('description', ''),
        'repo_stars': repo_data.get('stargazers_count', 0),
        'repo_forks': repo_data.get('forks_count', 0),
        
        # 貢獻者基本資訊
        'contributor': contributor['login'],
        'contributions': contributor['contributions'],
        'contributor_url': contributor.get('html_url', ''),
        'contributor_avatar_url': contributor.get('avatar_url', ''),
        
        # 貢獻者個人資料
        'contributor_name': user_info.get('name', '') if user_info else '',
        'contributor_company': user_info.get('company', '') if user_info else '',
        'contributor_location': user_info.get('location', '') if user_info else '',
        'contributor_email': user_info.get('email', '') if user_info else '',
        'contributor_bio': user_info.get('bio', '') if user_info else '',
        'contributor_blog': user_info.get('blog', '') if user_info else '',
        'contributor_twitter': user_info.get('twitter_username', '') if user_info else '',
        'contributor_created_at': user_info.get('created_at', '') if user_info else '',
        'contributor_updated_at': user_info.get('updated_at', '') if user_info else '',
        
        # 貢獻者統計資料
        'contributor_public_repos': user_info.get('public_repos', 0) if user_info else 0,
        'contributor_public_gists': user_info.get('public_gists', 0) if user_info else 0,
        'contributor_followers': user_info.get('followers', 0) if user_info else 0,
        'contributor_following': user_info.get('following', 0) if user_info else 0,
        
        # 詳細貢獻資料
        'total_commits': contribution_stats.get('total', 0) if contribution_stats else 0,
        'total_additions': contribution_stats.get('weeks', [{}])[-1].get('a', 0) if contribution_stats else 0,
        'total_deletions': contribution_stats.get('weeks', [{}])[-1].get('d', 0) if contribution_stats else 0,
        
        # 狀態
        'status': 'success'
    }
    
    writer.writerow(row_data)
    logging.info(f"Successfully processed contributor {contributor['login']} for {owner}/{repo_name}")

def verify_repository(owner, repo):
    """Verify if a repository exists and is accessible"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 404:
            logging.warning(f"Repository {owner}/{repo} does not exist")
            return False, None
        elif response.status_code == 401:
            logging.error("Authentication failed. Please check your GitHub token.")
            return False, None
        else:
            logging.error(f"Error accessing {owner}/{repo}: Status code {response.status_code}")
            logging.error(f"Response: {response.text}")
            return False, None
    except Exception as e:
        logging.error(f"Exception while verifying {owner}/{repo}: {str(e)}")
        return False, None

def process_repo(repo_name, owner, writer):
    """Process a single repository and its contributors"""
    logging.info(f"Processing repository {repo_name} with owner {owner}")
    
    # First verify if the repository exists
    exists, repo_data = verify_repository(owner, repo_name)
    if not exists:
        logging.warning(f"Repository {owner}/{repo_name} not found or not accessible")
        writer.writerow({
            'repo': repo_name,
            'owner': owner,
            'repo_url': f"https://github.com/{owner}/{repo_name}",
            'status': 'not_found'
        })
        return False
    
    logging.info(f"Found repository {owner}/{repo_name}")
    
    # Get contributors
    contributors = get_contributors(owner, repo_name)
    if not contributors:
        logging.error(f"Could not get contributors for {owner}/{repo_name}")
        writer.writerow({
            'repo': repo_name,
            'owner': owner,
            'repo_url': f"https://github.com/{owner}/{repo_name}",
            'status': 'error_getting_contributors'
        })
        return False
    
    logging.info(f"Found {len(contributors)} contributors for {owner}/{repo_name}")
    
    # Process each contributor
    for contributor in contributors:
        process_contributor(contributor, repo_name, owner, repo_data, writer)
    
    return True

# Main processing loop
with open('contributors.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        # Repo 資訊
        'repo', 'owner', 'repo_url', 'repo_description', 'repo_stars', 'repo_forks',
        # 貢獻者基本資訊
        'contributor', 'contributions', 'contributor_url', 'contributor_avatar_url',
        # 貢獻者個人資料
        'contributor_name', 'contributor_company', 'contributor_location',
        'contributor_email', 'contributor_bio', 'contributor_blog',
        'contributor_twitter', 'contributor_created_at', 'contributor_updated_at',
        # 貢獻者統計資料
        'contributor_public_repos', 'contributor_public_gists', 'contributor_followers',
        'contributor_following',
        # 詳細貢獻資料
        'total_commits', 'total_additions', 'total_deletions',
        # 狀態
        'status'
    ])
    writer.writeheader()
    
    # Read repo list from file
    repo_list = []
    with open('repo_list.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if ' - ' in line:
                repo_name = line.split(' - ')[0].strip()
                repo_list.append(repo_name)
    
    logging.info(f" *** Starting to process {len(repo_list)} repositories *** ")
    
    # Process all repos
    for idx, repo_name in enumerate(repo_list):
        logging.info(f" ---- Processing repository {idx + 1}/{len(repo_list)}: {repo_name} ---- ")
        
        # Check if repo has special handling in da_list
        owner = da_list.get(repo_name, 'g0v')
        
        # Handle special cases
        if owner == "":  # Empty string means no username needed
            url = f"https://github.com/{repo_name}"
            logging.info(f"{repo_name} - (特殊 URL: {url})")
            continue
        
        # Process multiple owners if needed
        owners = [owner] if not isinstance(owner, list) else owner
        found = False
        
        for current_owner in owners:
            logging.info(f"Trying owner {current_owner} for {repo_name}")
            if process_repo(repo_name, current_owner, writer):
                found = True
                break
        
        if not found:
            logging.info(f"Trying g0v organization for {repo_name}")
            process_repo(repo_name, 'g0v', writer)
        
        # Add delay to avoid GitHub API rate limits
        time.sleep(1)
        logging.info(f"Completed processing repository {repo_name}")

logging.info(" *** Finished processing all repositories *** ")
