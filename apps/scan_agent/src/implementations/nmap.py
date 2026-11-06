"""
Async Subnet Scanner using NMAP for PowerIPAM
"""

from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait

from logging import currentframe
from main import app_logger as logger
from logging_lib import clear_context, set_context, get_logger, whoami

import nmap
import json
import threading
import time

_global_results_lock = threading.Lock()

class AsyncSubnetScanner:
    """
    Async Scanner Class for managing scanner processes.
    """

    def __init__(
        self, 
        subnets,
        max_workers=4,
        poll_interval=0.5
    ):
        """
        Initialize the scanner.
        """

        self.subnets = list(subnets) if isinstance(subnets, (list, tuple)) else [subnets]

        if max_workers < 1:
            raise ValueError("max_workers must be at least 1")
        if poll_interval <= 0:
            raise ValueError("poll_interval must be greater than 0")

        # Thread-safe storage for consolidated results
        self.scan_results = {}
        self.max_workers = max_workers
        self.poll_interval = poll_interval
        self._results_lock = threading.Lock()
        self._logger = logger.getChild(whoami(currentframe()))


    def _callback_result(self, host, scan_result):
        """
        Callback function that triggers automatically whenever a host finishes scanning.
        """

        if not scan_result or host not in scan_result.get('scan', {}):
            return 
        
        host_data = scan_result['scan'][host]
        
        # Only process if the host is up
        if host_data.get('status', {}).get('state') != 'up':
            return
    
        hostnames = host_data.get('hostnames', [])
        hostname = hostnames[0].get('name', '') if hostnames else ''

        # Safely write to the global dictionary across threads
        with self._results_lock:
            self.scan_results[host] = {
                "status": "up",
                "hostname": hostname,
                "vendor": host_data.get('vendor', {})
            }
        
        self._logger.info("[+] Found active host: %s", host)

    def _scan_subnet_worker(self, subnet):
        """
        Worker function executed by each thread to scan a specific subnet range asynchronously.
        """
        self._logger.info(f"[*] Thread started for subnet: {subnet}")
        scanner = nmap.PortScannerAsync()
        
        # -sn specifies a ping scan (host discovery only)
        # The callback function handles data as soon as Nmap returns it
        scanner.scan(hosts=subnet, arguments='-sn', callback=self._callback_result)
        
        # Keep the thread alive while Nmap runs its background processes
        while scanner.still_scanning():
            time.sleep(0.5)
            
        self._logger.info(f"[-] Thread finished for subnet: {subnet}")

        # ==========================================
        # CRITICAL FIX FOR PYTHON 3.14 DEALLOCATOR
        # ==========================================
        # Safely detach the internal process tracking pointer.
        # This prevents the library's buggy __del__ method 
        # from throwing the NoneType .terminate() exception.
        if hasattr(scanner, '_process') and scanner._process is not None:
            scanner._process.terminate()
        # ==========================================

    def scan(self):
        """
        Starts scanning and orchestrates threads for multiple subnet scans.
        """
        threads = []
        start_time = time.time()

        self._logger.info(f"Starting concurrent scans across {len(self.subnets)} subnets...")

        # Spawn one thread per subnet in list
        for subnet in self.subnets:
            self._logger.debug(f"[*] Creating Thread for subnet: {subnet}")

            t = threading.Thread(target=self._scan_subnet_worker, args=(subnet,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        elapsed_time = time.time() - start_time
        self._logger.debug(f"All threads completed in {elapsed_time:.2f} seconds.")
        return self.scan_results


"""def main():
    # Example: List of target subnets to scan concurrently via threads
    subnets_to_scan = [
        "192.168.1.1",
        "10.160.0.1",
        "172.16.0.1"
    ]
    
    scanner = AsyncSubnetScanner(subnets=subnets_to_scan)
    results = scanner.scan()
    app_logger.debug(f"{results=}")

if __name__ == "__main__":
    import platform

    if platform.system() == "Windows":
        import multiprocessing
        multiprocessing.freeze_support()

    main()
"""