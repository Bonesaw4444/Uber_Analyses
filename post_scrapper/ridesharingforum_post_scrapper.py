from data_source import linkprocessing

main_url = 'https://www.ridesharingforum.com/t/how-much-do-uber-drivers-make-show-your-weekly-pay-stubs/580'
soup = linkprocessing(main_url)

setlist = []

textset = soup.find_all('div', {'class': 'post'})
for set in textset:
    setlist.append(set.get_text(strip=True))

print(setlist)
print(len(setlist))