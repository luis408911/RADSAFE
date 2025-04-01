import pandas as pd

def check_for_critical_faults():
    try:
        df = pd.read_csv('fault_logs.csv')
        critical_faults = df[df['severity'] == 'CRITICAL']
        if not critical_faults.empty:
            latest_fault = critical_faults.iloc[-1]
            return f"{latest_fault['component']} failed at {latest_fault['timestamp']}"
        return None
    except Exception as e:
        return f"Alert engine error: {e}"
