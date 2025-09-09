from ftplib import FTP

def ftp_operations():
    ftp_server = 'ftp.dlptest.com'   # Public test FTP server
    ftp_user = 'dlpuser'
    ftp_password = 'rNrKYTX9g7z3RgJRmxWuGHbeu'

    filename = 'test_upload.txt'

    # Create a test file to upload
    with open(filename, 'w') as f:
        f.write('This is a test file for FTP upload.')

    try:
        ftp = FTP(ftp_server)
        ftp.login(user=ftp_user, passwd=ftp_password)
        print("Connected to FTP server.")

        # Upload file
        with open(filename, 'rb') as f:
            ftp.storbinary(f'STOR {filename}', f)
        print(f"Uploaded {filename} successfully.")

        # List directory contents
        print("Directory contents:")
        ftp.retrlines('LIST')

        # Download file
        downloaded_file = 'downloaded_test.txt'
        with open(downloaded_file, 'wb') as f:
            ftp.retrbinary(f'RETR {filename}', f.write)
        print(f"Downloaded {filename} successfully.")

        # Verify content
        with open(downloaded_file, 'r') as f:
            content = f.read()
            print(f"Downloaded file content:\n{content}")

        ftp.quit()

    except Exception as e:
        print(f"FTP error: {e}")

if __name__ == '__main__':
    ftp_operations()
