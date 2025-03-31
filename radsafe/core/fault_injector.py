import csv
import random

class FaultInjector:
    def __init__(self, system):
        self.system = system
        self.log = []  # Store fault history

    def inject_seu_in_cpu_register(self):
        cpu = self.system.cpu

        if not hasattr(cpu, 'register_values'):
            print("[!] CPU registers not initialized.")
            return

        reg_index = random.randint(0, len(cpu.register_values) - 1)
        original_value = cpu.register_values[reg_index]
        bit_position = random.randint(0, 31)
        flipped_value = original_value ^ (1 << bit_position)
        cpu.register_values[reg_index] = flipped_value

        entry = {
            "register": reg_index,
            "bit_flipped": bit_position,
            "before": bin(original_value),
            "after": bin(flipped_value)
        }
        self.log.append(entry)

        print(f"[⚠️] Fault injected in CPU Register {reg_index}: bit {bit_position} flipped")
        print(f"     Before: {entry['before']}")
        print(f"     After : {entry['after']}")

    def inject_multiple_faults(self, count=5):
        print(f"\n[🚀] Injecting {count} simulated radiation faults...\n")
        for _ in range(count):
            self.inject_seu_in_cpu_register()

    def print_log(self):
        print("\n📜 Fault Injection Log:")
        for i, entry in enumerate(self.log):
            print(f"  #{i+1}: Register {entry['register']}, Bit {entry['bit_flipped']}, {entry['before']} → {entry['after']}")

    def export_log_to_csv(self, filepath="fault_log.csv"):
        print(f"\n💾 Exporting log to {filepath}...")
        with open(filepath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["register", "bit_flipped", "before", "after"])
            writer.writeheader()
            writer.writerows(self.log)
        print("✅ Log exported successfully.")
