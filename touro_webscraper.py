import requests
from bs4 import BeautifulSoup
import csv

alph = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
alphabet = alph.split(" ")

dictionary = {}

file = r"C:\Users\ga201\Desktop\Touro.csv"

# create a csv file to store scraped data
with open(file, "w", newline='', encoding='utf-8') as f:
    f.write = csv.writer(f)

    # Write column headings
    f.write.writerow(['Name', 'Email'])

    # This for loop goes thriugh each page of the directory in alphabetical order
    for letter in alphabet:
        url = f"https://www.touro.edu/directory/?alpha={letter}"
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        
        # gets total pages in a specific alphabet directory
        page_text = doc.find(class_='audio')

        if page_text != None:
            pagelist = page_text.find_all(['li'])
            total_pages = int(pagelist[-3].text)
        else:
            total_pages = 1
       
        print(f"\nTotal Pages in {letter}: {total_pages}")

        # Loop through each page of the alphabet
        for page in range(1, total_pages+1):
            url = f"https://www.touro.edu/directory/?alpha={letter}&page={page}"
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser") # create a BS4 object
            
            # gets the block containing all data of one person (in this case, we only scrape the name and email)
            block = doc.find_all(class_='staff')

            print(f"Letter {letter} | Page {page} of {total_pages}")

            for i in block:
                childs = list(i.children)
                name = str(childs[0].text).strip() # Name of faculty

                # Error handling in case email address does not exist
                try:
                    email = str(childs[4].text).strip() # email address of faculty
                except IndexError:
                    email = ''

                # Store all values in a dictionary
                dictionary[name] = email

    # Write dictionary into csv file
    for k, v in dictionary.items():
        f.write.writerow([k, v])