from scanner.subfinder_scanner import discover_subdomains


domain = "YOUR_AUTHORIZED_DOMAIN"

results = discover_subdomains(domain)

print(f"Discovered {len(results)} subdomains:")

for subdomain in results:
    print(subdomain)
