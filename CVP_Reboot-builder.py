from cvplibrary import CVPGlobalVariables, GlobalVariableNames, Device, RestClient
import json
import ssl
import os

# Ignore untrusted/self-signed certificates.
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    device_ip = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_IP) # Get Device IP
    device = Device(device_ip) # Create eAPI session to device via Device library.
    reboot = device.runCmds(['enable','write','reload now']) # Write config and Reboot device
if __name__ == "__main__":
    main()
