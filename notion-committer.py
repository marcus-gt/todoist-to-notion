from notion.client import NotionClient


client = NotionClient(token_v2="39ef1ddd36f6d1df766f496a75449093fadf1aa6c4c1e3442602754bc82c918a032bc025d4c5956801b58bc88fe10d950b6e844fa24b1951a095c3dde43a37ca7a509f77169389a97a70dc74baf5")

url = 'https://www.notion.so/API-TEST-c6b9d18ec0f444928982c7c387c6013a'

page = client.get_block(url)


# Read page title
page.title

# Set page title
page.title = "API test commit"

# Blocks
page.children

for child in page.children:
    print(child.title)


# DATABASES

url_db = 'https://www.notion.so/3457774311c54092b2dc4e0693e638bd?v=430b979a9640427185c9f9a3460b2fdf'

# Access a database using the URL of the database page or the inline block
cv = client.get_collection_view(url_db)

cv.collection.get_rows()

# List all the records with "Bob" in them
for row in cv.collection.get_rows(search="Oppgave"):
    print("We estimate the value of '{}' at {}".format(row.name, row.estimated_value))




# Add a new record
row = cv.collection.add_row()
row.name = 'Oppgave 6'