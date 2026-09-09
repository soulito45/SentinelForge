import socket


def resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to unique IPv4/IPv6 addresses.
    Returns an empty list if DNS resolution fails.
    """

    try:
        results = socket.getaddrinfo(
            hostname,
            None,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM,
        )

        ips = {
            result[4][0]
            for result in results
        }

        return sorted(ips)

    except socket.gaierror:
        return []
