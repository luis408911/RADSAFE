from radsafe.core.system_loader import load_system_from_json
from radsafe.core.fault_injector import FaultInjector

def main():
    system = load_system_from_json("config/sample_system.json")
    system.summary()

    injector = FaultInjector(system)

    print("\n[🔥] Simulating Multiple Radiation Faults...")
    injector.inject_multiple_faults(count=5)

    injector.print_log()

if __name__ == "__main__":
    main()
