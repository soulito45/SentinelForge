from scanner.httpx_parser import parse_httpx_output


sample_output = """
{"url":"http://test.sentinelforge.local","status_code":404,"webserver":"uvicorn","tech":["Python","Uvicorn"],"host":"test.sentinelforge.local","host_ip":"127.0.0.1","scheme":"http","content_type":"application/json"}
"""


results = parse_httpx_output(sample_output)

assert len(results) == 1

result = results[0]

assert result["url"] == "http://test.sentinelforge.local"
assert result["status_code"] == 404
assert result["webserver"] == "uvicorn"
assert result["technologies"] == ["Python", "Uvicorn"]

print("HTTPX parser test passed.")
print(result)
