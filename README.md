# g0v GitHub Repository Crawler

This project is a web crawler designed to collect and analyze contributor information from g0v GitHub repositories.

## Project Structure

- `web_crawler.py`: Main crawler script that fetches repository and contributor data from GitHub
- `repo_list.txt`: List of repositories to crawl
- `contributors.csv`: Output file containing collected contributor data
- `web_crawler.log`: Log file tracking the crawler's progress and any issues

## Features

- Fetches detailed information about repositories and their contributors
- Handles special cases for repositories with different owners
- Comprehensive logging of the crawling process
- Rate limiting to avoid GitHub API restrictions
- CSV output for easy data analysis

## Data Collection

The crawler collects the following information for each repository and contributor:

### Repository Information
- Repository name
- Owner
- URL
- Description
- Star count
- Fork count

### Contributor Information
- Basic info (login, contributions, URLs)
- Personal details (name, company, location, email, bio)
- Social links (blog, Twitter)
- Account statistics (public repos, gists, followers, following)
- Contribution statistics (commits, additions, deletions)

## Usage

1. Ensure you have Python installed
2. Install required dependencies:
   ```bash
   pip install PyGithub requests
   ```
3. Update the GitHub token in `web_crawler.py` if needed
4. Run the crawler:
   ```bash
   python web_crawler.py
   ```

## Output

The crawler generates two main output files:

1. `contributors.csv`: Contains all collected data in CSV format
2. `web_crawler.log`: Detailed log of the crawling process, including:
   - Start and end of processing
   - Repository processing progress
   - Contributor processing status
   - Any errors or warnings encountered

## Log Monitoring

To monitor the crawler's progress in real-time, you can use:
```bash
Get-Content -Path web_crawler.log -Wait
```

## Special Cases

The crawler handles special cases through the `da_list` dictionary in `web_crawler.py`, which maps repository names to their specific owners. This is necessary because some repositories are not under the main g0v organization.

## Error Handling

The crawler includes comprehensive error handling and logging for:
- Missing repositories
- API rate limits
- Missing contributor information
- Failed API calls
