from pygraphviz import AGraph
from networkx import (
    MultiDiGraph,
    DiGraph,
    simple_cycles,
    nx_agraph,
)


class CFG(DiGraph):
    pass


class DFG(MultiDiGraph):

    def to_dot(self, name: str = "test.dot"):
        nx_agraph.to_agraph(self).write(f"./{name}")

    def get_latency(self, node: str) -> int:
        return int(self.nodes[node].get("latency", 0))

    """
    this class method takes an edge as input, and finds the original
    predecessor and successor in the non-buffered circuit
    """

    def get_original_edge(self, edge: tuple) -> (str, str, dict): # type: ignore
        if edge not in self.edges:
            raise ValueError

        # Types that are inserted by either FPGA'20/FPL'22 buffer, our my
        # ad-hoc buffer (i.e., not in the original program)
        _SKIPPED_TYPES = (
            "Buffer",
            "OEHB",
            "TEHB",
        )
        pred = edge[0]
        succ = edge[1]
        from_ = self.edges[pred, succ, 0]["from"]
        to_ = self.edges[pred, succ, 0]["to"]
        while self.nodes[pred]["type"] in _SKIPPED_TYPES:
            in_edges = list(self.in_edges(pred))
            if len(in_edges) > 1:
                raise ValueError(
                    f"buffer unit {pred} has more than one input edge, which is impossible!"
                )
            from_ = self.edges[in_edges[0][0], pred, 0]["from"]
            pred = in_edges[0][0]

        while self.nodes[succ]["type"] in _SKIPPED_TYPES:
            out_edges = list(self.out_edges(succ))
            if len(out_edges) > 1:
                raise ValueError(
                    f"buffer unit {pred} has more than one output edge, which is impossible!"
                )
            to_ = self.edges[succ, out_edges[0][1], 0]["to"]
            succ = out_edges[0][1]
        return (pred, succ, {"from": from_, "to": "to_"})

    def get_cfg_edges(self) -> set:
        set_of_cfg_edges = set()
        for branch, v in self.edges():
            # get the original edge
            _, next_, _ = self.get_original_edge((branch, v))
            bb_prev = int(self.nodes[branch]["bbID"])
            bb_next = int(self.nodes[next_]["bbID"])
            # bbID=0 indicates that the unit is either a source or a memory
            # controller
            if self.nodes[branch]["type"] == "Branch" or bb_prev != bb_next:
                if not (bb_prev == 0 or bb_next == 0):
                    set_of_cfg_edges.add((bb_prev, bb_next))
        return set_of_cfg_edges

    """
    this class method extract all CFDFCs from the DFG, based on 
    information from CFG.
    """

    def generate_cfdfcs(self) -> list:
        cfg = DiGraph()
        cfg.add_edges_from(self.get_cfg_edges())
        cfdfcs = []

        for bbcycle in simple_cycles(cfg):
            cycle_edges = list(
                zip(
                    (bbcycle + [bbcycle[0]])[0:-1], (bbcycle + [bbcycle[0]])[1:]
                )
            )
            cfc = MG(self.copy())
            # remove control flow edges that are not part of the BB cycle
            edges_to_remove = []
            nodes_to_remove = []
            for u, v, eattr in cfc.edges(data=True):
                u_original, v_original, eattr_original = self.get_original_edge(
                    (u, v)
                )

                # check if the edge is an inter BB edge
                if not (
                    self.nodes[u_original]["type"] == "Branch"
                    or self.nodes[v_original]["type"] in ("Merge", "CntrlMerge")
                    or (
                        self.nodes[v_original]["type"] == "Mux"
                        and eattr_original["to"] in ("in2", "in3")
                    )
                ):
                    continue

                id_u = int(self.nodes[u_original]["bbID"])
                id_v = int(self.nodes[v_original]["bbID"])

                if (id_u, id_v) not in cycle_edges:
                    edges_to_remove.append((u, v))
            # to generate MG, the edges that are not in CFDFC is removed (branch and phi)
            cfc.remove_edges_from(edges_to_remove)
            for node, nattr in cfc.nodes(data=True):
                if int(nattr["bbID"]) not in bbcycle:
                    nodes_to_remove.append(node)
            cfc.remove_nodes_from(nodes_to_remove)
            cfdfcs.append(cfc)

        return cfdfcs


class MG(DFG):
    pass
