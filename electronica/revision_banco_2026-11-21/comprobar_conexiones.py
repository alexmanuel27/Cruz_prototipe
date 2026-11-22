"""Comprueba el contrato eléctrico exportando el esquema guardado con KiCad."""

from pathlib import Path
import shutil
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
    # Los puentes soldados conectan sus terminales sin crear una segunda cara de cobre.
    bridges = {}
    for ref, part in components.items():
        if not part.find("libsource").get("part", "").startswith("WireBridge_"):
            continue
        terminals = {name for (node_ref, _), name in nets.items() if node_ref == ref}
        logical = {name.split("__WIRE_", 1)[0] for name in terminals}
        assert len(terminals) >= 2 and len(logical) == 1, (ref, terminals)
        bridges.update({name: next(iter(logical)) for name in terminals})
    nets = {pin: bridges.get(name, name) for pin, name in nets.items()}
    expected = {
        ("J1", "15"): "HAL_EN", ("J1", "16"): "BLUE_EN",
        ("J1", "36"): "ORANGE_EN", ("J1", "38"): "IR_EN",
        ("J1", "40"): "OPT_ARM", ("J1", "37"): "HOLD_PI",
        ("J1", "11"): "M_STEP", ("J1", "12"): "M_DIR",
        ("J1", "13"): "M_ENABLE_N", ("J1", "7"): "TEMP_1WIRE",
        ("U6", "3"): "12V_OPT", ("U10", "1"): "5V_PI",
        ("U10", "3"): "3V3_PI", ("U10", "5"): "3V3_SENS",
        ("J8", "1"): "3V3_SENS", ("J8", "3"): "SDA_SENS",
        ("J8", "4"): "SCL_SENS", ("J10", "1"): "3V3_SENS",
        ("J10", "3"): "TEMP_SENS", ("R10", "2"): "3V3_SENS",
        ("U11", "14"): "3V3_PI", ("U11", "2"): "SDA",
        ("U11", "3"): "SDA_SENS", ("U11", "5"): "SCL",
        ("U11", "6"): "SCL_SENS", ("U11", "9"): "TEMP_1WIRE",
        ("U11", "8"): "TEMP_SENS", ("U12", "1"): "SDA_EC_ISO",
        ("U12", "3"): "3V3_EC_ISO", ("U12", "6"): "GND_EC_ISO",
        ("U12", "8"): "SCL_EC_ISO", ("U12", "4"): "EC_PROBE",
        ("U12", "5"): "EC_PROBE_RETURN", ("J28", "1"): "EC_PROBE",
        ("J28", "2"): "EC_PROBE_RETURN", ("R47", "1"): "12V_OPT",
        ("R47", "2"): "IR_A", ("U9", "14"): "5V_PI",
        ("U9", "2"): "HAL_EN", ("U9", "5"): "BLUE_EN",
        ("U9", "9"): "ORANGE_EN", ("U9", "12"): "IR_EN",
        ("Q10", "3"): "OPT_OE_N", ("R30", "1"): "5V_PI",
        ("R30", "2"): "OPT_OE_N", ("R32", "2"): "GND",
    }
    for pin, name in expected.items():
        assert nets.get(pin) == "/" + name, (pin, nets.get(pin), name)
    for pin in ("1", "4", "10", "13"):
        assert nets["U9", pin] == "/OPT_OE_N"
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
    assert nets["U12", "6"] != nets["U4", "2"]
    assert nets["U12", "5"] not in ("/GND", "/GND_EC_ISO")
    assert all(nets["U12", pin].startswith("unconnected-") for pin in ("2", "7", "9", "10"))
    assert components["U13"].findtext("footprint") == "Cross:R05CT05S"
    for ref, mapping in {
        "U13": {"1": "3V3_PI", "2": "GND", "3": "5V_PI", "4": "GND",
                "9": "GND_EC_ISO", "13": "GND_EC_ISO", "14": "3V3_EC_ISO",
                "15": "GND_EC_ISO", "16": "GND_EC_ISO"},
        "U15": {"1": "3V3_EC_ISO", "2": "SDA_EC_ISO", "3": "SCL_EC_ISO",
                "4": "GND_EC_ISO", "5": "GND", "6": "SCL_SENS",
                "7": "SDA_SENS", "8": "3V3_SENS"},
        "U4": {"1": "VBAT_FUSED", "2": "GND", "3": "5V_AON"},
        "U5": {"1": "VBAT_SW", "2": "GND", "3": "5V_PI", "4": "GND"},
        "U6": {"1": "VBAT_SW", "2": "GND", "3": "12V_OPT", "4": "GND"},
    }.items():
        for pin, name in mapping.items():
            assert nets[ref, pin] == "/" + name, (ref, pin, nets[ref, pin])
    assert components["U15"].findtext("footprint") == "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
    assert all("TerminalBlock_Phoenix" in components[ref].findtext("footprint")
               for ref in ("U5", "U6", "J23"))
    assert components["J1"].findtext("footprint") in (
        "Connector_IDC:IDC-Header_2x20_P2.54mm_Vertical",
        "Cross:CNC_Connector_IDC_IDC-Header_2x20_P2_54mm_Vertical",
    )
    assert all(nets["J1", pin].startswith("unconnected-") for pin in ("2", "4"))
    print("OK: señales, cuatro canales activos altos, resistencias, rama de sensores y separación EC.")


if __name__ == "__main__":
    main()
