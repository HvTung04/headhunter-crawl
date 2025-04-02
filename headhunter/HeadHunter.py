from crawler.Crawler import Crawler
from sheet_manager.InputSheet import InputSheet
from sheet_manager.OutputSheet import OutputSheet

class HeadHunter:
    def __init__(self):
        self.crawler = Crawler()
        self.input_sheet = InputSheet()
        self.data = {
            "Query Job title": [],
            "Query Company": [],
            "Query Location": [],
            "People": [],
        }
    
    def run(self, job_index, num_pages=1):
        self.crawler.login_linkedin()
        job_column = self.input_sheet.sheet.iloc[job_index]

        job_title_list = job_column["Title"]
        job_company_list = job_column["Company"]
        job_location_list = job_column["Location"]

        first_search = True

        for job_title in job_title_list:
            if first_search:
                self.crawler.search_linkedin_people(job_title, num_pages)
                self.crawler.apply_linkedin_filters(
                    {"location": job_location_list, "company": job_company_list}
                )
                first_search = False
            else: 
                self.crawler.change_query(job_title)
            hrefs = self.crawler.get_people_links()
            self.data["Query Job title"].extend([job_title] * len(hrefs))
            self.data["Query Company"].extend([job_company_list] * len(hrefs))
            self.data["Query Location"].extend([job_location_list] * len(hrefs))
            self.data["People"].extend(hrefs)
    
    def save(self, file_path="output.xlsx"):
        self.output_sheet = OutputSheet(self.data)
        self.output_sheet.save(file_path)