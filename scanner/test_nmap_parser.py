from scanner.nmap_parser import parse_nmap_xml


sample_xml = """
<nmaprun>
    <host>
        <address addr="192.168.1.10" addrtype="ipv4"/>
        <ports>

            <port protocol="tcp" portid="22">
                <state state="open"/>
                <service
                    name="ssh"
                    product="OpenSSH"
                    version="9.6"
                />
            </port>

            <port protocol="tcp" portid="443">
                <state state="open"/>
                <service
                    name="https"
                    product="nginx"
                    version="1.24.0"
                />
            </port>

        </ports>
    </host>
</nmaprun>
"""


results = parse_nmap_xml(sample_xml)

print(f"Ports found: {len(results)}")

for result in results:
    print(result)
