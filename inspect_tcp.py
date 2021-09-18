import socket

def create_connection(
    address,
    timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
    source_address=None,
    socket_options=None,
):

    host, port = address
    if host.startswith("["):
        host = host.strip("[]")
    err = None
    family = socket.AF_INET

    try:
        host.encode("idna")
    except UnicodeError:
        raise LocationParseError(f"'{host}', label empty or too long") from None

    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            sock = socket.socket(af, socktype, proto)


            if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                sock.settimeout(timeout)
            if source_address:
                sock.bind(source_address)
            sock.connect(sa)
            return sock

        except OSError as e:
            err = e
            if sock is not None:
                sock.close()
                sock = None

    if err is not None:
        raise err

    raise OSError("getaddrinfo returns an empty list")

if __name__ == '__main__':
    for i in range(10000):
        sock = create_connection(('your host.com', 80))
        print(sock, i)
        sock.close()

# Then use tcpdump or netstat inspect the dst host.
