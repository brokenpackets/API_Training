from cvplibrary import CVPGlobalVariables, GlobalVariableNames, Device, RestClient
import json
import ssl
import os

# Ignore untrusted/self-signed certificates.
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    device_ip = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_IP) # Get Device IP
    device = Device(device_ip) # Create eAPI session to device via Device library.
    profileLoad = device.runCmds(['enable','copy file:/persist/secure/capi.pem flash:/cert.pem', 'copy file:/persist/secure/capikey.pem flash:/key.pem', 'copy flash:cert.pem certificate:', 'copy flash:key.pem sslkey:'])
    print("""management security
   ssl profile test
   certificate cert.pem key key.pem
   tls versions 1.2

management api http-commands
   protocol https ssl profile test""")
if __name__ == "__main__":
    main()
