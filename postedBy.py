# postedBy.py
import requests
from bs4 import BeautifulSoup

# Function to get the full content of a URL
def get_content(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

# Function to extract 'posted by' names from a BeautifulSoup object
def extract_posted_by(soup):
    posted_by = []
    post_footer_divs = soup.find_all('div', class_='post-footer-line post-footer-line-1')
    for post_footer_div in post_footer_divs:
        span_tag = post_footer_div.find('span', class_='fn')
        if span_tag:
            posted_by_name = span_tag.text.strip()
            posted_by.append(posted_by_name)
    return posted_by

# Function to extract authors from the content after the last occurrence of "release team,"
def extract_authors_from_content(content):
    extracted_phrases = []
    found_release_team = False

    # Find all occurrences of "release team," in the content
    release_team_positions = [pos for pos in range(len(content)) if content.lower().find('release team,', pos) == pos]
    
    # Check if there are any occurrences
    if release_team_positions:
        # Get the starting position of the last occurrence
        pos = release_team_positions[-1] + len('release team,')
        # Extract text after the last "release team,"
        after_release_team = content[pos:].strip()
        if after_release_team:
            # Split the text into lines based on new lines
            lines = after_release_team.split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    # Append the stripped line content to extracted_phrases
                    extracted_phrases.append(line)

    if extracted_phrases:
        # Join all elements in extracted_phrases into a single string with commas between new lines
        return ', '.join(extracted_phrases)
    return None

# Function to extract authors from a BeautifulSoup object
def extract_authors(soup):
    authors_list = []
    post_body_divs = soup.find_all('div', class_='post-body entry-content')
    for post_body_div in post_body_divs:
        # Extract text from the entire div
        content = post_body_div.get_text(separator='\n', strip=True)
        # Extract and process text after the last "release team,"
        authors = extract_authors_from_content(content)
        if authors:
            # Append the authors to the authors_list
            authors_list.append(authors)
    return authors_list

# Function to find the URL of the "Older Posts" button
def get_older_posts_url(soup):
    older_posts_link = soup.find('a', class_='blog-pager-older-link')
    return older_posts_link['href'] if older_posts_link else None

# Function to fetch and return the data
def your_function_that_returns_data():
    base_url = 'https://blog.python.org/'

    # Lists to store data
    posted_by_list = []
    author_list = []
    date_list = []
    pythonVersionsBlogs = []
    pythonVersionsBlogLinks = []
    version_href_list = []

    # Start with the base URL
    current_url = base_url

    # Keep track of the number of blogs processed
    blogs_processed = 0
    max_blogs = 50

    while blogs_processed < max_blogs:
        # Get the content of the current page
        soup = get_content(current_url)
        
        # Extract the 'posted by' names and add them to the list
        posted_by = extract_posted_by(soup)
        posted_by_list.extend(posted_by)
        
        # Extract the authors and add them to the list
        authors = extract_authors(soup)
        author_list.extend(authors)
        
        # Extract dates, blog titles, and links
        data = soup.find_all('div', attrs={'class': 'date-outer'})
        for section in data:
            date_header = section.find('h2', class_='date-header')
            if date_header:
                date = date_header.text.strip()
            else:
                date = "No date"
            
            posts = section.find_all('div', class_='post hentry')
            for post in posts:
                date_list.append(date)
                pythonVersionsBlog = post.find('h3', class_='post-title entry-title').text.strip()
                pythonVersionsBlogs.append(pythonVersionsBlog)
                pythonVersionsBlogLinkTag = post.find('h3', class_='post-title entry-title').find('a', href=True)
                pythonVersionsBlogLink = pythonVersionsBlogLinkTag['href']
                pythonVersionsBlogLinks.append(pythonVersionsBlogLink)
        
        # Extract version links from the body content
        elements = soup.find_all(class_='post-body entry-content')
        for element in elements:
            links = element.find_all('a', href=True)
            filtered_links = []
            for link in links:
                href = link['href']
                if href.startswith('https://www.python.org/downloads/release/python'):
                    filtered_links.append(href)
            if filtered_links:
                version_href_list.append(','.join(filtered_links))
            else:
                version_href_list.append("No links found")
        
        # Update the number of blogs processed
        blogs_processed += min(len(posted_by), len(authors), len(date_list), len(pythonVersionsBlogs), len(pythonVersionsBlogLinks), len(version_href_list))
        
        # If we have enough blogs, stop
        if blogs_processed >= max_blogs:
            break
        
        # Find the URL for the "Older Posts" button
        current_url = get_older_posts_url(soup)
        if not current_url:
            break

    # Truncate lists to the required number of blogs
    posted_by_list = posted_by_list[:max_blogs]
    author_list = author_list[:max_blogs]
    date_list = date_list[:max_blogs]
    pythonVersionsBlogs = pythonVersionsBlogs[:max_blogs]
    pythonVersionsBlogLinks = pythonVersionsBlogLinks[:max_blogs]
    version_href_list = version_href_list[:max_blogs]

    # Return the collected data
    return date_list, pythonVersionsBlogs, pythonVersionsBlogLinks, version_href_list, author_list, posted_by_list
