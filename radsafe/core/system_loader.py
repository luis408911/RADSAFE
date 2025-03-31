import json
from radsafe.core.components import CPU, Memory, Bus

class EmbeddedSystem:
    def __init__(self, name, cpu, memory, bus):
        self.name = name
        self.cpu = cpu
        self.memory = memory
        self.bus = bus

    def summary(self):
        print(f"System: {self.name}")
        print(self.cpu)
        print(self.memory)
        print(self.bus)


def load_system_from_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    cpu = CPU(**data["cpu"])
    memory = Memory(size_mb=data["memory"]["size_mb"], mem_type=data["memory"]["type"])
    bus = Bus(bus_type=data["bus"]["type"], width_bits=data["bus"]["width_bits"])

    return EmbeddedSystem(name=data["system_name"], cpu=cpu, memory=memory, bus=bus)
