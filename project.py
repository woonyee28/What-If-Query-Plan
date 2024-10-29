import os
import signal
import sys

def signal_handler(sig, frame):
    print("\nExiting gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        os.system('streamlit run interface.py')
    except KeyboardInterrupt:
        signal_handler(None, None)
