# import libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
pandas      - data manipulation
matplotlib  - base plotting
seaborn     - attractive high-level plots
requests    - fetch data from GitHub API
"""

# Fetch data from GitHub API (commits from python/cpython repo)
url = "https://api.github.com/repos/python/cpython/commits"
params = {
    "since": "2025-08-01T00:00:00Z",  # commits after 1st Aug 2025
    "until": "2025-08-31T23:59:59Z",  # commits till end of Aug 2025
    "per_page": 100                   # number of commits per page
}

response = requests.get(url, params=params)
data = response.json()

# Convert API response into DataFrame
dates = [item['commit']['author']['date'] for item in data]
df = pd.DataFrame(dates, columns=["commit_date"])

# Convert string to datetime format and extract only date (not time)
df["commit_date"] = pd.to_datetime(df["commit_date"]).dt.date

# Count commits per day
commit_counts = df["commit_date"].value_counts().sort_index()

# Prepare final DataFrame
final_df = pd.DataFrame({
    "date": commit_counts.index,
    "commits": commit_counts.values
})

# Plot commits using seaborn
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(data=final_df, x="date", y="commits", marker="o")
plt.title("GitHub Python Repo - Commits in August 2025")
plt.xlabel("Date")
plt.ylabel("Number of Commits")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
