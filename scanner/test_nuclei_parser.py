from scanner.nuclei_parser import parse_nuclei_output


sample_output = """
{"template-id":"http-missing-security-headers","info":{"name":"Missing Security Headers","severity":"medium"},"matched-at":"http://test.sentinelforge.local:8000","host":"test.sentinelforge.local","type":"http","matcher-name":"x-frame-options"}
"""

results = parse_nuclei_output(sample_output)

assert len(results) == 1

result = results[0]

assert result["template_id"] == "http-missing-security-headers"
assert result["name"] == "Missing Security Headers"
assert result["severity"] == "medium"
assert result["host"] == "test.sentinelforge.local"

print("Nuclei parser test passed.")
print(result)
