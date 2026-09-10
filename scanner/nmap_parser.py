import xml.etree.ElementTree as ET


def parse_nmap_xml(xml_output: str) -> list[dict]:
    """
    Parse Nmap XML output into structured port information.
    """

    root = ET.fromstring(xml_output)

    ports = []

    for host in root.findall("host"):
        address_element = host.find("address")

        ip = (
            address_element.get("addr")
            if address_element is not None
            else None
        )

        ports_element = host.find("ports")

        if ports_element is None:
            continue

        for port in ports_element.findall("port"):
            state_element = port.find("state")
            service_element = port.find("service")

            state = (
                state_element.get("state")
                if state_element is not None
                else None
            )

            service_name = None
            product = None
            version = None

            if service_element is not None:
                service_name = service_element.get("name")
                product = service_element.get("product")
                version = service_element.get("version")

            ports.append(
                {
                    "ip": ip,
                    "port": int(port.get("portid")),
                    "protocol": port.get("protocol"),
                    "state": state,
                    "service_name": service_name,
                    "product": product,
                    "version": version,
                }
            )

    return ports
