import re
import requests


class UpdateChangeLog:
    API_COMMITS_URL = "https://api.github.com/repos/graymattermetrics/config/commits"
    COMMIT_URL = (
        "https://github.com/graymattermetrics/config/commit/{sha}"
        "#diff-d8d0422389f03d783e32e627250fe29834bd09c6361640d1ff00661dd6820034"
    )

    def __init__(self) -> None:
        self.version_to_commit_sha = {}

    def fetch_commit_versions(self) -> None:
        """
        Fetches all commits, reads the version and writes
        the commit sha to the version_to_commit_sha dictionary.
        """
        request = requests.get(self.API_COMMITS_URL)
        for commit in request.json():
            commit_message = commit["commit"]["message"]
            if match := re.match(r"(\[.*?\])", commit_message):
                # If the commit follows the [0.0.1] versioning scheme
                self.version_to_commit_sha[match.group(1)] = commit["sha"]

    def get_version_headers(self, content: str) -> list[str]:
        """
        Get all the version headers in the CHANGELOG using
        regex and return them in reverse order.
        """
        version_headers = re.findall(r"## (\[.*?\])", content)
        return version_headers[::-1]

    def write_to_changelog(self) -> None:
        """
        Writes to the CHANGELOG with the correct links
        For example, a header change of [0.1.0]
        would have
        [0.1.0]: https://github.com/...
        appended to the end to render the change
        """
        self.fetch_commit_versions()
        with open("CHANGELOG.md", "r", encoding="utf-8") as changelog:
            content = changelog.read()

        version_numbers = self.get_version_headers(content)
        links = [
            [version, self.COMMIT_URL.format(sha=self.version_to_commit_sha[version])]
            for version in version_numbers
        ]
        formatted_links = "\n".join(f"{version}: {link}" for version, link in links)
        content_before_links = re.split(r"\n*\[.*?\]: ", content)[0]
        with open("CHANGELOG.md", "w", encoding="utf-8") as changelog:
            changelog.write(f"{content_before_links}\n\n{formatted_links}")


if __name__ == "__main__":
    UpdateChangeLog().write_to_changelog()
