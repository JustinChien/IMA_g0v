from github import Github
import csv
import requests
import json
import time

# 初始化 GitHub API (需申請 personal access token)
# Justin Chien : web crewler use
g = Github("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")

def get_repo_info(owner, repo):
    """使用 GitHub API 獲取 repo 資訊"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        'Authorization': f'token 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',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200, response.json() if response.status_code == 200 else None

def get_contributors(owner, repo):
    """獲取 repo 的貢獻者資訊"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {
        'Authorization': f'token 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',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_user_info(username):
    """獲取用戶詳細資訊"""
    url = f"https://api.github.com/users/{username}"
    headers = {
        'Authorization': f'token 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',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_user_contributions(owner, repo, username):
    """獲取用戶在特定 repo 的詳細貢獻資訊"""
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
    headers = {
        'Authorization': f'token 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',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for contributor in data:
            if contributor['author']['login'] == username:
                return contributor
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
    
    for repo_name, owner in da_list.items():
        # 處理特殊情況
        if owner == "":  # 空字串表示不需要 username
            url = f"https://github.com/{repo_name}"
            print(f"跳過 {repo_name} (特殊 URL: {url})")
            writer.writerow({
                'repo': repo_name,
                'owner': '',
                'repo_url': url,
                'status': 'special_url'
            })
            continue
            
        # 處理多個 owner 的情況
        owners = [owner] if not isinstance(owner, list) else owner
        found = False
        
        for current_owner in owners:
            # 先檢查 repo 是否存在
            exists, repo_data = get_repo_info(current_owner, repo_name)
            if exists:
                print(f"找到 {current_owner}/{repo_name}")
                found = True
                
                # 獲取貢獻者列表
                contributors = get_contributors(current_owner, repo_name)
                if contributors:
                    for contributor in contributors:
                        # 獲取貢獻者詳細資訊
                        user_info = get_user_info(contributor['login'])
                        # 獲取詳細貢獻資料
                        contribution_stats = get_user_contributions(current_owner, repo_name, contributor['login'])
                        
                        writer.writerow({
                            # Repo 資訊
                            'repo': repo_name,
                            'owner': current_owner,
                            'repo_url': f"https://github.com/{current_owner}/{repo_name}",
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
                        })
                    break
                else:
                    print(f"無法獲取 {current_owner}/{repo_name} 的貢獻者資訊")
                    writer.writerow({
                        'repo': repo_name,
                        'owner': current_owner,
                        'repo_url': f"https://github.com/{current_owner}/{repo_name}",
                        'status': 'error_getting_contributors'
                    })
        
        if not found:
            # 嘗試使用 g0v 作為 owner
            exists, repo_data = get_repo_info('g0v', repo_name)
            if exists:
                print(f"在 g0v 組織中找到 {repo_name}")
                contributors = get_contributors('g0v', repo_name)
                if contributors:
                    for contributor in contributors:
                        user_info = get_user_info(contributor['login'])
                        contribution_stats = get_user_contributions('g0v', repo_name, contributor['login'])
                        
                        writer.writerow({
                            # Repo 資訊
                            'repo': repo_name,
                            'owner': 'g0v',
                            'repo_url': f"https://github.com/g0v/{repo_name}",
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
                        })
                else:
                    print(f"無法獲取 g0v/{repo_name} 的貢獻者資訊")
                    writer.writerow({
                        'repo': repo_name,
                        'owner': 'g0v',
                        'repo_url': f"https://github.com/g0v/{repo_name}",
                        'status': 'error_getting_contributors'
                    })
            else:
                print(f"找不到 {repo_name} (嘗試過 {', '.join(owners)} 和 g0v)")
                writer.writerow({
                    'repo': repo_name,
                    'owner': '',
                    'repo_url': '',
                    'status': 'not_found'
                })
        
        # 添加延遲以避免觸發 GitHub API 限制
        time.sleep(1)
