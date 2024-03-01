import requests
import openpyxl
import time

APP_ID    = "846098"
CLIENT_ID = "Iv1.f82874f4aab1a1f8"

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

def write_data_to_excel(data_arrays, filename):
  """
  Writes four arrays of data as strings to the columns of a new Excel file.

  Args:
      data_arrays: A list containing four arrays of data to be written.
      filename: The desired name of the output Excel file.
  """
  # Create a new workbook
  wb = Workbook()
  
  # Get the worksheet
  ws = wb.active

  ws.append(["Name", "EID", "Has Repo", "Did Commit"])

  # Write data to rows
  for row_index, row_data in enumerate(zip(*data_arrays)):
    ws.append(list(row_data))

  # Save the workbook
  wb.save(filename)


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

def get_gh_auth():
  """
  Attempts to get and return a Github user token
  """

  #Request a token to identify ourself
  url = 'https://github.com/login/device/code' + f'?client_id={CLIENT_ID}'
  r = requests.post(url)

  fields = {elem.split("=")[0]: elem.split("=")[1] for elem in str(r.content)[2:-1].split("&")}

  token = fields["device_code"]
  user_code = fields["user_code"]

  print(f"")
  print(f"------------------------------------")
  print(f"You must login to github to continue")
  print(f"Enter the code '{user_code}' at:")
  print(f"https://github.com/login/device")
  print(f"------------------------------------")
  input("Press Enter to continue...\n")

  while(1):
    #Check that the toekn has been acessed
    url = 'https://github.com/login/device/code' 
    paramaters = f'?client_id={CLIENT_ID}&device_code={token}&grant_type=urn:ietf:params:oauth:grant-type:device_code'
    r = requests.post(url)
    
    print(r.content)
    
    time.sleep(1)
  input()


  return token


if __name__ == "__main__":
	
  get_gh_auth()