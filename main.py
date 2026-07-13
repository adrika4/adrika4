import requests
import re

USERNAME = "adrika4"

url = f"https://api.github.com/search/issues?q=is:pr+author:{USERNAME}+is:merged&sort=updated&order=desc"

response = requests.get(url)
data = response.json()

prs = data.get("items", [])

emojis = ["🥳","🎉","🎊","🥂","🙌🏼","🚀","✨","🔥","💯","🌟"]

merged = ""

for i, pr in enumerate(prs[:10]):
    emoji = emojis[i % len(emojis)]
    repo = "/".join(pr["repository_url"].split("/")[-2:])
    number = pr["number"]

    merged += f"{i+1}. {emoji} Merged PR [{number}]({pr['html_url']}) - [{repo}](https://github.com/{repo})\n"

with open("README.md","r",encoding="utf-8") as f:
    readme=f.read()

readme = re.sub(
    r"<!--Start Count Merged PRs-->.*?<!--Finish Count Merged PRs-->",
    f"""<!--Start Count Merged PRs-->
<span><img src="https://img.shields.io/badge/Total_Merged_PRs-{len(prs)}-1877F2?style=for-the-badge"></span>
<!--Finish Count Merged PRs-->""",
    readme,
    flags=re.DOTALL
)

readme = re.sub(
    r"<!--Start Merged PRs-->.*?<!--Finish Merged PRs-->",
    f"""<!--Start Merged PRs-->
{merged}
<!--Finish Merged PRs-->""",
    readme,
    flags=re.DOTALL
)

with open("README.md","w",encoding="utf-8") as f:
    f.write(readme)
