from scanner.subfinder_scanner import parse_subfinder_output


sample_output = """
API.Example.com
www.example.com
api.example.com
mail.example.com.
WWW.EXAMPLE.COM
"""


results = parse_subfinder_output(sample_output)

print(f"Unique subdomains: {len(results)}")

for subdomain in results:
    print(subdomain)
