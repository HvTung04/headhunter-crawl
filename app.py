from crawler.crawler import Crawler

crawler = Crawler()

crawler.login_linkedin()
crawler.search_linkedin_people("python developer", 1)
print(crawler.get_people_links())