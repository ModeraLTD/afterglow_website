import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

class PayPalClient: 
    def __init__(self):
        self.client_id = "AVZ1D0Qx5d8HRtIoMTcjgcQxAoz581PCB1L0EH8TVAbqKHCY_is-wOUotvxbMUGfTjM7mqnaxoLki1b0"
        self.client_secret = "ENKyHBNxqBkvSZBsFkJgV8FBX4uRyb_jVDPuBjNILCeTCMEOTOVdwe5FD71VNG34z_g3Em0qWelR9eWE"
        self.environment = SandboxEnvironment(client_id = self.client_id, client_secret = self.client_secret)
        self.client = PayPalHttpClient(self.environment)