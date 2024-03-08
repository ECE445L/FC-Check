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
  print(f"Note: UC = {user_code}")
  print(f"------------------------------------")
  input("Press Enter to continue...\n")

  while(1):
    #Check that the toekn has been acessed
    url = 'https://github.com/login/oauth/access_token' 
    paramaters = {"client_id": CLIENT_ID, "device_code": token, "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}
    r = requests.post(url, paramaters)
    
    if r.status_code == 200:
      if "authorization_pending" in str(r.content):
        print("Waiting for authorization...")
      else:
        print("Got token!")
        break
    else:
      print(f"Invalid status seen? See content/status_code: {r.content}, {r.status_code}")
    time.sleep(5)

  fields = {elem.split("=")[0]: elem.split("=")[1] for elem in str(r.content)[2:-1].split("&")}
  print(fields)
  print(fields["access_token"])

  return fields["access_token"], fields

def get_gh_classroom(token:str):
  """
  Shows the user all github classrooms they are a part of to have them select one 
  """

  url = f'https://api.github.com/classrooms' 
  paramaters = {"page":1, "per_page":100}
  headers = {"Accept":"application/vnd.github+json", "Authorization": f"Bearer {token}", "X-GitHub-Api-Version":"2022-11-28"}
  r = requests.get(url, paramaters, headers=headers)

  if(r.status_code != 200):
    print("Error:", r.content, r.status_code)
    exit()

  rjson = r.json()

  print(f"#\tID\tName")
  for i, rdict in enumerate(rjson):
    print(f"{i}.\t{rdict['id']}\t{rdict['name']}")
  idx = int(input("Select index: "))

  return rjson[idx]['id']

def get_gh_assignment(token:str, classroom_id : str):
  """
  Shows the user all github assignments a classrooms has to select one 
  """

  url = f'https://api.github.com/classrooms/{classroom_id}/assignments' 
  paramaters = {"page":1, "per_page":100}
  headers = {"Accept":"application/vnd.github+json", "Authorization": f"Bearer {token}", "X-GitHub-Api-Version":"2022-11-28"}
  r = requests.get(url, paramaters, headers=headers)

  if(r.status_code != 200):
    print("Error:", r.content, r.status_code)
    exit()

  rjson = r.json()

  print(f"#\tID\tName")
  for i, rdict in enumerate(rjson):
    print(f"{i}.\t{rdict['id']}\t{rdict['title']}")
  idx = int(input("Select index: "))

  print(rjson[idx]['id'])

  return rjson[idx]['id']

def get_gh_assignment_json(token: str, assignment_id: str):
  """
  Attempts to load an assignment by id
  """

  url = f'https://api.github.com/assignments/{assignment_id}' 
  paramaters = {"page":1, "per_page":100}
  headers = {"Accept":"application/vnd.github+json", "Authorization": f"Bearer {token}", "X-GitHub-Api-Version":"2022-11-28"}
  r = requests.get(url, paramaters, headers=headers)

  print(r.content, r.status_code, r.json())

  url = f'https://api.github.com/assignments/{assignment_id}/accepted_assignments' 
  paramaters = {"page":1, "per_page":100}
  headers = {"Accept":"application/vnd.github+json", "Authorization": f"token {token}", "X-GitHub-Api-Version":"2022-11-28"}
  r = requests.get(url, paramaters, headers=headers)

  print(r.content, r.status_code, r.json())

if __name__ == "__main__":
	
  ghu_token, ghu_res = get_gh_auth()

  gh_c_id = get_gh_classroom(ghu_token)

  gh_a_id = get_gh_assignment(ghu_token, gh_c_id)

  get_gh_assignment_json(ghu_token, gh_a_id)