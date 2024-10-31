import requests
import csv


token = "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"  
headers = {"Authorization": f"token {token}"}
url = "https://api.github.com/search/users?q=location:Stockholm+followers:>100"


def fetch_users():
    users_data = []
    page = 1

    while True:
        response = requests.get(f"{url}&page={page}", headers=headers)
        data = response.json()

       
        print(f"User data (page {page}): {data}")

        if "items" not in data or len(data["items"]) == 0:
            break

        users_data.extend(data["items"])
        page += 1

    return users_data


def get_user_details(username):
    user_url = f"https://api.github.com/users/{username}"
    response = requests.get(user_url, headers=headers)
    return response.json()


def process_and_save_users(users):
    with open("users.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers",
             "following", "created_at"])

        for user in users:
            user_details = get_user_details(user["login"])
            print(user_details) 
            
            company = user_details.get("company", "")
            if company:
                company = company.strip().lstrip("@").upper()

            writer.writerow([
                user_details.get("login", ""),
                user_details.get("name", ""),
                company,
                user_details.get("location", ""),
                user_details.get("email", ""),
                user_details.get("hireable", ""),
                user_details.get("bio", ""),
                user_details.get("public_repos", ""),
                user_details.get("followers", ""),
                user_details.get("following", ""),
                user_details.get("created_at", "")
            ])


def fetch_and_save_repositories(users):
    repos_data = []

    for user in users:
        repos_url = f"https://api.github.com/users/{user['login']}/repos"
        response = requests.get(repos_url, headers=headers)
        repos = response.json()

       
        print(f"Repos for {user['login']}: {repos}")

       
        if isinstance(repos, list):
            for repo in repos[:500]: 
                repos_data.append({
                    "login": user["login"],
                    "full_name": repo.get("full_name", ""),
                    "created_at": repo.get("created_at", ""),
                    "stargazers_count": repo.get("stargazers_count", ""),
                    "watchers_count": repo.get("watchers_count", ""),
                    "language": repo.get("language", ""),
                    "has_projects": repo.get("has_projects", ""),
                    "has_wiki": repo.get("has_wiki", ""),
                    "license_name": repo.get("license", {}).get("name", "") if repo.get("license") else ""
                })
        else:
            print(f"Unexpected response for {user['login']}: {repos}")

   
    with open("repositories.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["login", "full_name", "created_at", "stargazers_count", "watchers_count", "language", "has_projects",
             "has_wiki", "license_name"])

        for repo in repos_data:
            writer.writerow([
                repo["login"],
                repo["full_name"],
                repo["created_at"],
                repo["stargazers_count"],
                repo["watchers_count"],
                repo["language"],
                repo["has_projects"],
                repo["has_wiki"],
                repo["license_name"]
            ])


if __name__ == "__main__":
    users = fetch_users()  
    process_and_save_users(users)  
    fetch_and_save_repositories(users)  
