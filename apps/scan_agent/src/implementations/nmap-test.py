import nmap
import json
import threading
import time

class AsyncSubnetScanner:
    def __init__(self, subnets, output_file="scan_results.json"):
        """
        Initialize the scanner with a list of target subnets and output destination.
        """
        self.subnets = subnets if isinstance(subnets, list) else [subnets]
        self.output_file = output_file
        
        # Thread-safe storage for consolidated results
        self.scan_results = {}
        self.results_lock = threading.Lock()
        
    def _callback_result(self, host, scan_result):
        """
        Internal callback executed by PortScannerAsync when a host responds.
        """
        if not scan_result or host not in scan_result.get('scan', {}):
            return
            
        host_data = scan_result['scan'][host]
        
        # Only parse the host details if it is confirmed active
        if host_data.get('status', {}).get('state') == 'up':
            hostname = ""
            if host_data.get('hostnames'):
                hostname = host_data['hostnames'].get('name', '')
                
            vendor = host_data.get('vendor', {})
            
            # Secure the lock before modifying shared memory
            with self.results_lock:
                self.scan_results[host] = {
                    "status": "up",
                    "hostname": hostname,
                    "vendor": vendor
                }
                print(f"[+] Found active host: {host}")

    def _scan_worker(self, subnet):
        """
        Internal worker method handled by each individual thread.
        """
        print(f"[*] Starting background scanner for: {subnet}")
        nma = nmap.PortScannerAsync()
        
        # Trigger the async Nmap scan with our internal callback
        nma.scan(hosts=subnet, arguments='-sn', callback=self._callback_result)
        
        # Keep the worker thread alive while the subprocess runs
        while nma.still_scanning():
            time.sleep(0.5)
            
        print(f"[-] Scanner finished for: {subnet}")

    def save_results(self):
        """
        Exports the scanned dataset to a formatted JSON file.
        """
        with open(self.output_file, 'w') as f:
            json.dump(self.scan_results, f, indent=4)
        print(f"[!] Saved consolidated results to {self.output_file}")

    def run(self):
        """
        Orchestrates thread creation, execution, and final data output.
        """
        threads = []
        start_time = time.time()
        
        print(f"Launching concurrent scan for {len(self.subnets)} targets...")
        
        # Spawn one thread per subnet
        for subnet in self.subnets:
            t = threading.Thread(target=self._scan_worker, args=(subnet,))
            threads.append(t)
            t.start()
            
        # Join all threads back into the main application timeline
        for t in threads:
            t.join()
            
        # Write results out to disk
        self.save_results()
        
        elapsed_time = time.time() - start_time
        print(f"All operations finished in {elapsed_time:.2f} seconds.")
        return self.scan_results

# Example Usage
if __name__ == "__main__":
    targets = [
        "192.168.1.0/24",
        "10.0.0.0/24"
    ]
    
    # Instantiate the class
    scanner = AsyncSubnetScanner(subnets=targets, output_file="network_report.json")
    
    # Execute the scan
    results = scanner.run()
