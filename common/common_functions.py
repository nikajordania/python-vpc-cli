import socket


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(('8.8.8.8', 80))

        ip_address = s.getsockname()[0] + '/32'
    except Exception as e:
        print(f"Error: {e}")
        ip_address = None
    finally:
        s.close()

    return ip_address
