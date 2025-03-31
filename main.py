from radsafe.core.system_loader import load_system_from_json
from radsafe.core.fault_injector import FaultInjector

def main():
    # Load system configuration from JSON
    system = load_system_from_json("config/sample_system.json")
    system.summary()

    # Initialize fault injector
    injector = FaultInjector(system)

    print("\n[🔥] Simulating Multiple Radiation Faults...")
    injector.inject_multiple_faults(count=5)

    # Print fault injection log
    injector.print_log()

    # Export the fault log to a CSV file
    injector.export_log_to_csv("fault_log.csv")

if __name__ == "__main__":
    main()
