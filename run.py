from fpl import draft

x = draft.ApiScraper(41747,34)
print(x.get_live_score_pdf())
print(x.get_live_score_pdf_formatted())