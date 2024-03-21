import requests


def download_onedrive_file(url: str, filename: str) -> bool:
    """
    Download a file from OneDrive. Works only on "public" shared links to files. Not working on directories.
    Source: https://gist.github.com/federicocunico/8b4af49383c2b2e5ac6903007dac6940

    Args:
    url (str): The URL of the file to download
    filename (str): The filename to save the file to

    Returns:
    bool: True if the file was downloaded successfully, False otherwise
    """
    url += "&download=1"
    print("Downloading to", filename, "...")
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content

        # save the content to a file
        with open(filename, "wb") as file:
            file.write(content)
        print("Saved ", len(response.content) // 1024, "MB to", filename)
        return True
    else:
        print("Failed to download", url, "status code:", response.status_code)
        return False
