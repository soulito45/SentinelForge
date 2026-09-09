from scanner.dns_resolver import resolve_hostname


test_hosts = [
    "example.com",
    "www.example.com",
    "api.example.com",
]


for hostname in test_hosts:
    ips = resolve_hostname(hostname)

    print(f"\n{hostname}")

    if ips:
        for ip in ips:
            print(f"  -> {ip}")
    else:
        print("  -> DNS resolution failed")
