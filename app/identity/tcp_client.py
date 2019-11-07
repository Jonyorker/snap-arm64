import socket
import zipfile
import os

host = '10.10.10.1'  # get local machine name
port = 8624  # Make sure it's within the > 1024 $$ <65535 range


class ReceiveFile:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((host, port))

    def __init__(self):

        # we connect with the server script via socket, and send a short message to as a handshake and initiate
        # all the work on the server script. We then receive a zipfile containing a text file with uuid and associated
        # certificates and extract them.

        message = 'uuid'
        self.sock.send(message.encode('utf-8'))
        data = self.sock.recv(1024)

        # Create variable with snap path

        zip_path = os.environ['SNAP_COMMON'] + '/serial_certs.zip'
        zip_extract_path = os.environ['SNAP_COMMON'] + '/serial_certs'

        file = open(zip_path, 'wb+')
        while data != bytes(''.encode()):
            file.write(data)
            data = self.sock.recv(1024)

        self.sock.close()

        file.close()

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall((zip_extract_path))

        print('Zip file received and extracted')


if __name__ == '__main__':

    # Check if cert zip file exists, and if so don't run

    if not os.path.exists(os.environ['SNAP_COMMON'] + '/serial_certs'):
        ReceiveFile()
    exit()

