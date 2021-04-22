import pytket
import pytket.cirq

from cirq.contrib.qasm_import import circuit_from_qasm

from pytket.circuit import Node
from pytket.predicates import CompilationUnit, ConnectivityPredicate
from pytket.routing import GraphPlacement
from pytket.passes import SequencePass, RoutingPass, DecomposeSwapsToCXs, PlacementPass

def read_qasm_circuit(path):
    qasm_string = open(path, 'r').read()
    try:
        return circuit_from_qasm(qasm_string)
    except:
        print('wrong circuit format')

def _device_connection_list_to_tket_device(device_connection_list):
    arc = pytket.routing.Architecture(device_connection_list)
    return pytket.device.Device({}, {}, arc)
    
circuit = read_qasm_circuit('QUEKO-benchmark/BSS/53QBT_700CYC_QSE_9.qasm')

device_connection_list = [(0, 1),
 (1, 2),
 (2, 3),
 (3, 4),
 (4, 5),
 (5, 6),
 (6, 7),
 (7, 8),
 (0, 9),
 (4, 10),
 (8, 11),
 (9, 14),
 (10, 18),
 (11, 22),
 (12, 13),
 (13, 14),
 (14, 15),
 (15, 16),
 (16, 17),
 (17, 18),
 (18, 19),
 (19, 20),
 (20, 21),
 (21, 22),
 (12, 23),
 (16, 24),
 (20, 25),
 (23, 26),
 (24, 30),
 (25, 34),
 (26, 27),
 (27, 28),
 (28, 29),
 (29, 30),
 (30, 31),
 (31, 32),
 (32, 33),
 (33, 34),
 (34, 35),
 (35, 36),
 (28, 37),
 (32, 38),
 (36, 39),
 (37, 42),
 (38, 46),
 (39, 50),
 (40, 41),
 (41, 42),
 (42, 43),
 (43, 44),
 (44, 45),
 (45, 46),
 (46, 47),
 (47, 48),
 (48, 49),
 (49, 50),
 (40, 51),
 (44, 52),
 (48, 53),
 (51, 54),
 (52, 58),
 (53, 62),
 (54, 55),
 (55, 56),
 (56, 57),
 (57, 58),
 (58, 59),
 (59, 60),
 (60, 61),
 (61, 62),
 (62, 63),
 (63, 64),
 (56, 65),
 (60, 66),
 (64, 67),
 (65, 70),
 (66, 74),
 (67, 78),
 (68, 69),
 (69, 70),
 (70, 71),
 (71, 72),
 (72, 73),
 (73, 74),
 (74, 75),
 (75, 76),
 (76, 77),
 (77, 78),
 (68, 79),
 (72, 80),
 (76, 81)]

tk_circuit = pytket.cirq.cirq_to_tk(circuit)
tk_device = _device_connection_list_to_tket_device(device_connection_list)

unit = CompilationUnit(tk_circuit, [ConnectivityPredicate(tk_device)])

passes = SequencePass([
    PlacementPass(GraphPlacement(tk_device)),
    RoutingPass(tk_device, bridge_lookahead=0, bridge_interactions=0)]) # NO BRIDGE
passes.apply(unit)
valid = unit.check_all_predicates()

assert valid

routed_circuit = pytket.cirq.tk_to_cirq(unit.circuit)