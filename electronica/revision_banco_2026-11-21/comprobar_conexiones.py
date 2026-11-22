"""Comprueba el contrato eléctrico exportando el esquema guardado con KiCad."""

from pathlib import Path
import shutil
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET


def main():
    project = Path(__file__).resolve().parents[1] / "cross_v8_raspberry"
    cli = shutil.which("kicad-cli") or "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
    with tempfile.TemporaryDirectory(prefix="cruz-netlist-") as directory:
        output = Path(directory) / "redes.xml"
        subprocess.run(
            [cli, "sch", "export", "netlist", "--format", "kicadxml", "-o", str(output),
             str(project / "cross_v8_draft.kicad_sch")], check=True,
        )
        root = ET.parse(output).getroot()

    nets = {
        (node.get("ref"), node.get("pin")): net.get("name")
        for net in root.findall("nets/net") for node in net.findall("node")
    }
    components = {part.get("ref"): part for part in root.findall("components/comp")}
    assert not any(re.fullmatch(r"W\d+", ref) for ref in components)
    assert not any("__WIRE_" in name for name in nets.values())
    original = ET.parse(project.parent / "cierre_pcb_2026-11-21/redes.xml").getroot()
    original_nets = {
        (node.get("ref"), node.get("pin")): net.get("name")
        for net in original.findall("nets/net") for node in net.findall("node")
    }
    removed = {
        "U10", "U7", "K1", "F2", "Q2", "Q6", "R11", "R12", "D1", "D6",
        "U9", "Q10", "R30", "R31", "R32", "C7", "R25", "R33", "R34", "R35",
        "U11", "C10", "U13", "U15", "C13", "C14", "C17", "R28", "R29",
        "D4", "D5", "Q5", "R18", "R19", "U8",
    }
    assert removed.isdisjoint(components)
    renamed = {
        "/3V3_SENS": "/3V3_PI", "/3V3_AON": "/5V_AON",
        "/VBAT_RAW": "/SYS_IN", "/VBAT_FUSED": "/SYS_FUSED", "/VBAT_SW": "/SYS_SW",
        "/HAL_BUF": "/HAL_EN", "/BLUE_BUF": "/BLUE_EN",
        "/ORANGE_BUF": "/ORANGE_EN", "/IR_BUF": "/IR_EN",
        "/SDA_SENS": "/SDA", "/SDA_EC_ISO": "/SDA",
        "/SCL_SENS": "/SCL", "/SCL_EC_ISO": "/SCL",
        "/TEMP_SENS": "/TEMP_1WIRE", "/3V3_EC_ISO": "/3V3_PI", "/GND_EC_ISO": "/GND",
        "/MAG_N": "/BUTTON_N", "/SW_SENSE": "/SHUTDOWN_REQ_N", "/HOLD_PI": "/POWER_OFF_ACK",
    }
    original_nets = {
        pin: renamed.get(name, name)
        for pin, name in original_nets.items() if pin[0] not in removed
    }
    for pin in (("J1", "18"), ("J1", "40"), ("J18", "1"), ("J18", "2")):
        assert nets[pin].startswith("unconnected-")
        original_nets[pin] = nets[pin]
    original_nets.update({
        ("U16", "1"): "/GND", ("U16", "2"): "/POWER_OFF_ACK",
        ("U16", "3"): "/GND", ("U16", "4"): "/CUT_ACK_5V",
        ("U16", "5"): "/5V_AON", ("C22", "1"): "/5V_AON", ("C22", "2"): "/GND",
    })
    supervisor_pins = {
        "U17": {
            "1": "5V_AON", "14": "GND", "10": "UPDI", "11": "BUTTON_N",
            "12": "WAKE_N", "13": "POWER_ON", "2": "SHUTDOWN_REQ_N", "3": "CUT_ACK_5V",
        },
        "J29": {"1": "5V_AON", "2": "UPDI", "3": "GND"},
    }
    for ref, pins in supervisor_pins.items():
        for pin, name in pins.items():
            original_nets[ref, pin] = "/" + name
    for pin in ("4", "5", "6", "7", "8", "9"):
        assert nets["U17", pin].startswith("unconnected-")
        original_nets["U17", pin] = nets["U17", pin]
    # Al quitar etiquetas internas, KiCad asigna nombres automáticos a esas redes.
    # La identidad eléctrica se comprueba mediante el conjunto completo de pines.
    current_groups = {}
    original_groups = {}
    for pin, name in nets.items():
        current_groups.setdefault(name, set()).add(pin)
    for pin, name in original_nets.items():
        original_groups.setdefault(name, set()).add(pin)
    original_names = {frozenset(pins): name for name, pins in original_groups.items()}
    assert {frozenset(pins) for pins in current_groups.values()} == set(original_names), \
        "Cambió la conectividad original del esquema"
    aliases = {name: original_names[frozenset(pins)] for name, pins in current_groups.items()}
    nets = {pin: aliases[name] for pin, name in nets.items()}
    expected = {
        ("J1", "15"): "HAL_EN", ("J1", "16"): "BLUE_EN",
        ("J1", "36"): "ORANGE_EN", ("J1", "38"): "IR_EN",
        ("R5", "1"): "HAL_EN", ("R36", "1"): "BLUE_EN",
        ("R38", "1"): "ORANGE_EN", ("R40", "1"): "IR_EN",
        ("J1", "37"): "POWER_OFF_ACK", ("J24", "5"): "WAKE_N",
        ("J1", "29"): "SHUTDOWN_REQ_N", ("J25", "1"): "BUTTON_N",
        ("J1", "11"): "M_STEP", ("J1", "12"): "M_DIR",
        ("J1", "13"): "M_ENABLE_N", ("J1", "7"): "TEMP_1WIRE",
        ("J8", "1"): "3V3_PI", ("J8", "3"): "SDA", ("J8", "4"): "SCL",
        ("J10", "1"): "3V3_PI", ("J10", "3"): "TEMP_1WIRE", ("R10", "2"): "3V3_PI",
        ("U12", "1"): "SDA", ("U12", "3"): "3V3_PI", ("U12", "6"): "GND",
        ("U12", "8"): "SCL", ("U12", "4"): "EC_PROBE",
        ("U12", "5"): "EC_PROBE_RETURN", ("J28", "1"): "EC_PROBE",
        ("J28", "2"): "EC_PROBE_RETURN", ("R47", "1"): "12V_OPT",
        ("R47", "2"): "IR_A",
    }
    for pin, name in expected.items():
        assert nets.get(pin) == "/" + name, (pin, nets.get(pin), name)
    for gate, pulldown, channel in (("R5", "R6", "HAL"), ("R36", "R37", "BLUE"),
                                    ("R38", "R39", "ORANGE"), ("R40", "R41", "IR")):
        assert nets[gate, "2"] == nets[pulldown, "1"] == f"/{channel}_GATE"
        assert nets[pulldown, "2"] == "/GND"
    for ref, prefix in (("Q1", "HAL"), ("Q7", "BLUE"), ("Q8", "ORANGE"), ("Q9", "IR")):
        assert [nets[ref, str(pin)] for pin in (1, 2, 3)] == [
            f"/{prefix}_GATE", f"/{prefix}_LOW", "/GND",
        ]
    for refs, output, anode in ((["R4", "R42", "R43"], "BLUE_REG_OUT", "BLUE_A"),
                                 (["R44", "R45", "R46"], "ORANGE_REG_OUT", "ORANGE_A")):
        for ref in refs:
            assert (nets[ref, "1"], nets[ref, "2"]) == ("/" + output, "/" + anode)
        resistance = 1 / sum(1 / float(components[ref].findtext("value").split("R")[0]) for ref in refs)
        assert abs(resistance - 10.4) < 0.001
    assert {"J9", "D8"}.isdisjoint(components)
    assert nets["U12", "6"] == nets["U4", "2"]
    assert nets["U12", "5"] not in ("/GND", "/GND_EC_ISO")
    assert all(nets["U12", pin].startswith("unconnected-") for pin in ("2", "7", "9", "10"))
    for ref, mapping in {
        "U4": {"1": "SYS_FUSED", "2": "GND", "3": "5V_AON"},
        "U5": {"1": "SYS_SW", "2": "GND", "3": "5V_PI", "4": "GND"},
        "U6": {"1": "SYS_SW", "2": "GND", "3": "12V_OPT", "4": "GND"},
    }.items():
        for pin, name in mapping.items():
            assert nets[ref, pin] == "/" + name, (ref, pin, nets[ref, pin])
    assert nets["J8", "1"] == nets["J10", "1"] == nets["J1", "1"]
    assert nets["U12", "3"] == nets["J8", "1"]
    assert nets["U12", "1"] == nets["J8", "3"] == nets["J1", "3"]
    assert nets["U12", "8"] == nets["J8", "4"] == nets["J1", "5"]
    assert "DS3231" in components["J24"].findtext("value")
    assert nets["J24", "1"] == nets["U17", "1"] == "/5V_AON"
    assert nets["J25", "2"] == "/GND"
    assert nets["J26", "1"] == nets["U17", "13"] == "/POWER_ON"
    assert nets["U16", "4"] == nets["U17", "3"] == "/CUT_ACK_5V"
    assert nets["J13", "1"] == nets["F1", "1"] == "/SYS_IN"
    assert nets["J14", "1"] == nets["F1", "2"] == "/SYS_FUSED"
    assert nets["J11", "1"] == nets["U1", "16"] == "/SYS_SW"
    assert nets["J1", "22"] == "/PILOT_SENSE"
    assert "3V3_AON" not in {name.lstrip("/") for name in nets.values()}
    assert len(components) == 91
    assert all("TerminalBlock_Phoenix" in components[ref].findtext("footprint")
               for ref in ("U5", "U6", "J23"))
    assert components["J1"].findtext("footprint") in (
        "Connector_IDC:IDC-Header_2x20_P2.54mm_Vertical",
        "Cross:CNC_Connector_IDC_IDC-Header_2x20_P2_54mm_Vertical",
    )
    assert all(nets["J1", pin].startswith("unconnected-") for pin in ("2", "4"))
    board = (project / "cross_v8_draft.kicad_pcb").read_text()
    assert not re.search(r'^\t\((segment|via|arc|zone)\b', board, re.MULTILINE)
    assert not re.search(r'"Reference" "W\d+"', board)
    assert "__WIRE_" not in board
    print("OK: pulsador, supervisor, GPIO de apagado, alarma RTC, mando óptico e I²C.")


if __name__ == "__main__":
    main()
