from msal import ConfidentialClientApplication
import requests
import pandas as pd
import io

CLIENT_ID = "client-id"
TENANT_ID = "tenant-id"
CLIENT_SECRET = "client-secret"
SHAREPOINT_SITE = "sitename"
SHAREPOINT_HOST = "domain.sharepoint.com"
EXCEL_PATH = "../calendar.xlsx" #relateive path

def get_access_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = ConfidentialClientApplication(CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET)
    scope = ["https://graph.microsoft.com/.default"]
    token_reponse = app.acquire_token_for_client(scopes=scope)
    return token_reponse["access_token"]

def fetch_excel_from_sharepoint():
    token = get_access_token()

    # Get Site ID
    site_url = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_HOST}:/sites/{SHAREPOINT_SITE}"
    site_resp = requests.get(site_url, headers={"Authorization": f"Bearer {token}"})
    site_id = site_resp.json()["id"]

    # Get file contents
    file_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{EXCEL_PATH}:/content"
    file_resp = requests.get(site_url, headers={"Authorization": f"Bearer {token}"})

    df = pd.read_excel(io.BytesIO(file_resp.content))
    return df