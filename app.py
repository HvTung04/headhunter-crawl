from crawler.Crawler import Crawler
from sheet_manager.InputSheet import InputSheet

crawler = Crawler()
input_sheet = InputSheet()

crawler.login_linkedin()
crawler.search_linkedin_people("python developer", 1)
crawler.apply_linkedin_filters({"location": ["Hanoi"], "company": ["FPT Software"]})
print(crawler.get_people_links())