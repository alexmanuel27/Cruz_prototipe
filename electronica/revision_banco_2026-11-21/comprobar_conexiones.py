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
    assert components["U13"].find("property[@name='exclude_from_board']") is not None
    assert components["J1"].findtext("footprint") == "Connector_IDC:IDC-Header_2x20_P2.54mm_Vertical"
    assert all(nets["J1", pin].startswith("unconnected-") for pin in ("2", "4"))
    print("OK: señales, cuatro canales activos altos, resistencias, rama de sensores y separación EC.")


if __name__ == "__main__":
    main()
