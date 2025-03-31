class CPU:
    def __init__(self, registers, cache_kb, frequency_ghz):
        self.registers = registers
        self.cache_kb = cache_kb
        self.frequency_ghz = frequency_ghz

    def __str__(self):
        return f"CPU: {self.registers} regs, {self.cache_kb}KB cache @ {self.frequency_ghz}GHz"


class Memory:
    def __init__(self, size_mb, mem_type):
        self.size_mb = size_mb
        self.mem_type = mem_type

    def __str__(self):
        return f"Memory: {self.size_mb}MB ({self.mem_type})"


class Bus:
    def __init__(self, bus_type, width_bits):
        self.bus_type = bus_type
        self.width_bits = width_bits

    def __str__(self):
        return f"Bus: {self.bus_type}, {self.width_bits}-bit"

