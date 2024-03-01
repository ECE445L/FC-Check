import requests
import openpyxl

# The goal of this script is to use the GH API in order to check if the student has a repo
# With at least one commit

def read_excel_to_arrays(filepath):
  """
  Reads the first two columns of the first worksheet in an Excel file 
  and stores them in a pair of arrays.

  Args:
      filepath: The path to the Excel file.
  """
  # Open the workbook
  wb = openpyxl.load_workbook(filename=filepath)

  # Get the first sheet
  sheet = wb.active

  # Initialize empty arrays
  col1 = []
  col2 = []

  # Loop through rows (starting from 1 to skip headers)
  for row in sheet.iter_rows(min_row=2):
    # Append data to respective arrays
    col1.append(row[0].value)
    col2.append(row[1].value)

  return (col1, col2)




"""
r = requests.get('https://github.com/timeline.json')
print( r.json() )
"""

"""
url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
payload = open("request.json")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

r = requests.post(url, data=payload, headers=headers)

"""


if __name__ == "__main__":
	# Example usage
	filepath = "your_excel_file.xlsx"
	col1, col2 = read_excel_to_arrays(filepath)

	# Access data in the arrays
	print(f"First column: {col1}")
	print(f"Second column: {col2}")