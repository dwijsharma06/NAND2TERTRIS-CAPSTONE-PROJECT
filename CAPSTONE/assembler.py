import sys
from pathlib import Path

COMP = {
    "0":"0101010", "1":"0111111",
    "-1":"0111010", "D":"0001100",
    "A":"0110000", "M":"1110000",
    "!D":"0001101", "!A":"0110001",
    "!M":"1110001", "-D":"0001111",
    "-A":"0110011", "-M":"1110011",
    "D+1":"0011111", "A+1":"0110111",
    "M+1":"1110111", "D-1":"0001110",
    "A-1":"0110010", "M-1":"1110010",
    "D+A":"0000010", "D+M":"1000010",
    "D-A":"0010011", "D-M":"1010011",
    "A-D":"0000111", "M-D":"1000111",
    "D&A":"0000000", "D&M":"1000000",
    "D|A":"0010101", "D|M":"1010101"
}

JUMP = {
    "":"000", "JGT":"001", "JEQ":"010",
    "JGE":"011", "JLT":"100", "JNE":"101",
    "JLE":"110", "JMP":"111"
}

def assemble(filename):
    symbols = {
        "SP":0, "LCL":1, "ARG":2,
        "THIS":3, "THAT":4,
        "SCREEN":16384, "KBD":24576
    }

    for i in range(16):
        symbols["R"+str(i)] = i

    user_symbols = {}
    instructions = []

    with open(filename) as f:
        lines = [
            "".join(line.split("//")[0].split())
            for line in f
        ]

    # First pass: identify labels
    rom = 0

    for line in lines:
        if not line:
            continue

        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            symbols[label] = rom
            user_symbols[label] = rom
        else:
            instructions.append(line)
            rom += 1

    # Second pass: generate binary
    next_ram = 16
    output = []

    for line in instructions:
        if line.startswith("@"):
            value = line[1:]

            if value.isdigit():
                address = int(value)
            else:
                if value not in symbols:
                    symbols[value] = next_ram
                    user_symbols[value] = next_ram
                    next_ram += 1

                address = symbols[value]

            if not 0 <= address <= 32767:
                raise ValueError("Invalid address")

            output.append(format(address, "016b"))

        else:
            dest = ""
            jump = ""
            comp = line

            if "=" in comp:
                dest, comp = comp.split("=")

            if ";" in comp:
                comp, jump = comp.split(";")

            dest_bits = "".join(
                str(int(x in dest)) for x in "ADM"
            )

            output.append(
                "111" + COMP[comp] +
                dest_bits + JUMP[jump]
            )

    output_file = Path(filename).with_suffix(".hack")
    output_file.write_text("\n".join(output)+"\n")

    # Extra feature: K = 12, K mod 3 = 0
    symbol_file = output_file.parent / "symbols.txt"

    with open(symbol_file, "w") as f:
        for name, address in user_symbols.items():
            f.write(f"{name} = {address}\n")

    print("Assembly successful!")
    print("Generated:", output_file)
    print("Generated:", symbol_file)

if __name__ == "__main__":
    assemble(sys.argv[1])
