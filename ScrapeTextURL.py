"""
Copyright (C) Edward Alan Lockhart 2021

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/.
"""

def scrape_text_url(url, ask_permission = True):    
    def scrape(url):
        # Scrape the URL contents
        from bs4 import BeautifulSoup
        try:
            # Spoof user agent
            # https://www.whatismybrowser.com/detect/what-is-my-user-agent
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
            with requests.get(url, headers = headers) as page:
                soup = BeautifulSoup(page.content, 'html.parser') 
                # Remove all javascript and stylesheet code
                for s in soup.find_all(['script', 'style']): 
                    s.decompose() # Remove 
                # Get visible text, join with a new sentence and strip extra whitespace
                return soup.get_text('. ', strip = True)
        except:
            return 'scrape error'
    
    # Try to visit the URL
    import requests
    try:
        # Get HTTP status code
        url_code = int(str(requests.get(url, timeout = 5).status_code)[:1])
        if url_code != 2 and url_code != 3:
            raise Exception
    except:
        return 'url connection failed'
    # Check for restrictions
    if ask_permission:
        # Create /robots.txt
        from urllib.parse import urlparse
        robot_url = "http://" + urlparse(url).netloc + "/robots.txt"
        # Try to visit /robots.txt
        try:
            # Get HTTP status code
            robot_code = int(str(requests.get(robot_url, timeout = 5).status_code)[:1])
            # https://developers.google.com/search/docs/advanced/robots/robots_txt#handling-http-result-codes
            # Check for server error
            if robot_code == 5:
                raise Exception
        except:
            return 'robots.txt connection failed'
        # Check if robots.txt exists, client error
        if robot_code == 4:
            return scrape(url)
        # Read the restrictions
        try:
            from protego import Protego
            rp = Protego.parse(requests.get(robot_url).text)
        except:
            return 'robots.txt read error'
        # Check if the URL is scrapable
        if rp.can_fetch('*', url):
            return scrape(url)
        else:
            return 'disallowed'
    # Ignore any restrictions
    else:
        return scrape(url)

text = scrape_text_url("https://www.test.co.uk",
                       ask_permission = True)
