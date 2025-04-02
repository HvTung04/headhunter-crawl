import pandas as pd
import os


class InputSheet:
    def __init__(
        self,
        file_path=os.getenv("INPUT_SHEET"),
        sheet_name=os.getenv("INPUT_SHEET_NAME"),
    ):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.sheet = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        self.reformat()

    def reformat(self):
        """
        Reformat the sheet.
        """
        new_sheet = pd.DataFrame()

        # Handle titles
        title_column = self.sheet[
            "Title liên quan\n(the same với title job đang tuyển)"
        ].values.tolist()

        for i, titles in enumerate(title_column):
            if "/" in str(titles):
                title_column[i] = [title.strip() for title in str(titles).split("/")]
            else:
                title_column[i] = [title.strip() for title in str(titles).split("\n")]
            title_column[i].append(str(self.sheet["Title job"].values[i]).strip())
        new_sheet["Title"] = title_column

        # Handle keywords
        # Not handle yet
        new_sheet["Keywords"] = self.sheet["Keywords liên quan\n(skill, công nghệ, ...)"].values

        # Handle companies
        company_column = self.sheet["Công ty "].values.tolist()
        for i, companies in enumerate(company_column):
            companies = str(companies).strip()
            if "," in companies:
                companies = companies.replace(",", "\n")
            if "/" in companies:
                companies = companies.replace("/", "\n")
            company_column[i] = [company.strip() for company in companies.split("\n")]
        new_sheet["Company"] = company_column

        # Handle locations
        location_column = self.sheet["Địa điểm"].values.tolist()
        for i, locations in enumerate(location_column):
            if "," in str(locations):
                location_column[i] = [location.strip() for location in str(locations).split(",")]
            else:
                location_column[i] = [str(locations).strip()]
        new_sheet["Location"] = location_column
        
        self.sheet = new_sheet

    def get_cell(self, row_index, column_name):
        return self.sheet[column_name].iloc[row_index]