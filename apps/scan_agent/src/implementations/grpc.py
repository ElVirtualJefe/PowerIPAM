"""
gRPC implementation for the scan agent.

- A gRPC Stream will feed data back to the core-service

- The scan-agent will pull the list of networks to scan 
from the core-service at the configured scan interval.

- The scan-agent will need an incoming gRPC stream for
receiving configuration updates from the core-service.
"""

import grpc
from concurrent import futures

