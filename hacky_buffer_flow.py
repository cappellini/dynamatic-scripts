#!/usr/bin/env python3
from pathlib import Path
from sys import stdout
from subprocess import run
from sys import argv
from subprocess import PIPE
import re


def shell(*args, **kwargs):
    stdout.flush()
    return run(*args, **kwargs, check=True)


def generate_initial_design(dynamatic_path, kernel_name):
    script = f"set-dynamatic-path {dynamatic_path}; set-src {dynamatic_path}/integration-test/{kernel_name}/{kernel_name}.c; compile --simple-buffers; exit"
    shell(dynamatic_path / "bin" / "dynamatic", input=str.encode(script))


def simulate_design(dynamatic_path, kernel_name) -> int:
    script = f"set-dynamatic-path {dynamatic_path}; set-src {dynamatic_path}/integration-test/{kernel_name}/{kernel_name}.c; write-hdl --experimental; simulate --experimental; exit"
    shell(dynamatic_path / "bin" / "dynamatic", input=str.encode(script))

    with open(
        dynamatic_path
        / "integration-test"
        / kernel_name
        / "out"
        / "sim"
        / "report.txt",
        "r",
    ) as f:
        lines = f.read()

        time = re.findall(r"Time: (\d+) ns\s+Iteration:", lines)[-1]

    return int(time)


def list_transp_buffers(dynamatic_path, kernel_name) -> list:
    transp_buffers = []
    with open(
        dynamatic_path
        / "integration-test"
        / kernel_name
        / "out"
        / "comp"
        / "handshake_export.mlir",
        "r",
    ) as f:
        for line in f.read().split("\n"):
            m = re.search(
                r"\%(\d+) = tehb \[(\d+)\] (\S+).*handshake.name = \"(\w+)\"",
                line,
            )
            if m:
                transp_buffers.append(m.group(4))
    return transp_buffers


def remove_buffer(dynamatic_path, kernel_name, buffer_name):
    handshake_export = (
        dynamatic_path
        / "integration-test"
        / kernel_name
        / "out"
        / "comp"
        / "handshake_export.mlir"
    )
    lines = []
    with open(
        handshake_export,
        "r",
    ) as f:
        for line in f.read().split("\n"):
            m = re.search(
                r"(\S+) = tehb \[(\d+)\] (\S+).*handshake.name = \"(\w+)\"",
                line,
            )
            if m and m.group(4) == buffer_name:
                substituted = m.group(1)
                by = m.group(3)
            else:
                lines.append(line)

    joined_lines = "\n".join(lines)

    with open(handshake_export, "w") as f:
        f.write(
            re.sub(
                r"([^0-9a-zA-Z_#%])("
                + re.escape(substituted)
                + r")([^0-9a-zA-Z_#%])",
                r"\1" + by + r"\3",
                joined_lines,
            )
        )


def generate_hw(dynamatic_path, kernel_name):
    handshake_export = (
        dynamatic_path
        / "integration-test"
        / kernel_name
        / "out"
        / "comp"
        / "handshake_export.mlir"
    )
    hw = (
        dynamatic_path
        / "integration-test"
        / kernel_name
        / "out"
        / "comp"
        / "hw.mlir"
    )
    with open(hw, "w") as fs:
        capture = shell(
            [
                dynamatic_path / "bin" / "dynamatic-opt",
                handshake_export,
                "--lower-handshake-to-hw",
            ],
            stdout=PIPE,
        )
        fs.write(capture.stdout.decode())


def synthesize(dynamatic_path, kernel_name) -> int:
    print("Running synthesis!")
    script = f"set-dynamatic-path {dynamatic_path}; set-src {dynamatic_path}/integration-test/{kernel_name}/{kernel_name}.c; write-hdl --experimental; synthesize; exit"
    shell(dynamatic_path / "bin" / "dynamatic", input=str.encode(script))


def main():
    dynamatic_path = Path(argv[1])
    kernel_name = argv[2]
    generate_initial_design(dynamatic_path, kernel_name)
    tbuffers = list_transp_buffers(dynamatic_path, kernel_name)
    print("Total number of transparent buffers:", len(tbuffers))
    for b in tbuffers:
        print(b)
    handshake_export = (
        dynamatic_path
        / "integration-test"
        / kernel_name
        / "out"
        / "comp"
        / "handshake_export.mlir"
    )
    handshake_export_bak = (
        dynamatic_path
        / "integration-test"
        / kernel_name
        / "out"
        / "comp"
        / "handshake_export_export.mlir"
    )
    # exit()
    initial_latency = simulate_design(dynamatic_path, kernel_name)
    for buffer_name in tbuffers:
        shell(["cp", "-f", handshake_export, handshake_export_bak])
        remove_buffer(dynamatic_path, kernel_name, buffer_name)
        generate_hw(dynamatic_path, kernel_name)
        current_latency = simulate_design(dynamatic_path, kernel_name)
        if current_latency > initial_latency:
            print(
                buffer_name,
                "cannot be removed!",
            )
            shell(["mv", handshake_export_bak, handshake_export])
        else:
            print(
                "Successfully removed",
                buffer_name,
                "without a performance penalty",
            )

    print("current latency:", current_latency)
    synthesize(dynamatic_path, kernel_name)


if __name__ == "__main__":
    main()
