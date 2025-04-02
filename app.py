from headhunter import HeadHunter

if __name__ == "__main__":
    headhunter = HeadHunter()
    headhunter.run(0, 1)
    headhunter.save("output.xlsx")