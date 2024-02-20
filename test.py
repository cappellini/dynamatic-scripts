#!/usr/bin/env python3

from dhls_utils import *
from pathlib import Path

if __name__ == "__main__":
    benchmark_directory = Path("./dynamatic/integration-test")
    benchmark = "fir"

    dfg = DFG(
        AGraph(
            benchmark_directory
            / benchmark
            / "out"
            / "comp"
            / (benchmark + ".dot"),
            strict=False,
            directed=True,
        )
    )

    for unit in dfg:
        print("the latency of ", unit, "is", dfg.get_latency(unit))

    for i, cfc in enumerate(dfg.generate_cfdfcs()):
        for unit in cfc:
            print("the", i + 1, "-th extracted cfdfc has node:", unit)
        for pred, succ in cfc.edges():
            print(
                "the",
                i + 1,
                "-th extracted cfdfc has edge:",
                f"{pred}-->{succ}",
            )
