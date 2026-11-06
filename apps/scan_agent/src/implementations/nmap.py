"""
Async Subnet Scanner using NMAP for PowerIPAM
"""

from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait

from logging import currentframe
from main import app_logger as logger
from main import settings
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
        max_workers: int = 4,
    ):
        """
        Initialize the scanner.
        """

        self.subnets = list(subnets) if isinstance(subnets, (list, tuple)) else [subnets]

        if max_workers < 1:
            raise ValueError("max_workers must be at least 1")

        # Thread-safe storage for consolidated results
        self.scan_results = {}
        self.max_workers = max_workers
        self._logger = logger.getChild('async-scanner')


    @staticmethod
    def _hostname(host_data: dict) -> str:
        """Extract the hostname from host data."""
        hostnames = host_data.get('hostnames', [])

        if isinstance(hostnames, list) and hostnames:
            first = hostnames[0]
            if isinstance(first, dict):
                return first.get('name', '')

        if isinstance(hostnames, dict):
            return hostnames.get('name', '')

        return ''
    

    def _scan_subnet_worker(self, subnet: str) -> dict:
        """
        Synchronous worker function to scan a specific subnet.
        """
        self._logger.info("[*] Thread started for subnet: %s", subnet)
        #scanner = nmap.PortScannerAsync()
        scanner = nmap.PortScanner()
        
        # -sn specifies a ping scan (host discovery only)
        # The callback function handles data as soon as Nmap returns it
        result = scanner.scan(
            hosts=subnet, 
            arguments=settings.NMAP_ARGUMENTS.get("pingScan", "-sn")
        )
        
        # Keep the thread alive while Nmap runs its background processes
        #while scanner.still_scanning():
        #    time.sleep(0.5)

        active_hosts = {}
        for host, host_data in result.get('scan', {}).items():
            if host_data.get('status', {}).get('state') != 'up':
                continue

            active_hosts[host] = {
                "status": "up",
                "hostname": self._hostname(host_data),
                "vendor": host_data.get('vendor', {})
            }
            
        self._logger.info("[-] Thread finished for subnet: %s", subnet)

        # ==========================================
        # CRITICAL FIX FOR PYTHON 3.14 DEALLOCATOR
        # ==========================================
        # Safely detach the internal process tracking pointer.
        # This prevents the library's buggy __del__ method 
        # from throwing the NoneType .terminate() exception.
        #if hasattr(scanner, '_process') and scanner._process is not None:
        #    scanner._process.terminate()
        # ==========================================

        return active_hosts

    def scan(self):
        """
        Starts scanning and orchestrates threads for multiple subnet scans.
        """
        start_time = time.time()
        subnet_iter = iter(self.subnets)
        pending = {}
        results = {}

        self._logger.info(
            "Starting %d concurrent scans across %d subnets...", 
            self.max_workers, 
            len(self.subnets)
        )

        """
        # Spawn one thread per subnet in list
        for subnet in self.subnets:
            self._logger.debug(f"[*] Creating Thread for subnet: {subnet}")

            t = threading.Thread(target=self._scan_subnet_worker, args=(subnet,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        """

        with ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix="nmap-scan"
        ) as executer:

            def submit_next() -> bool:
                try:
                    subnet = next(subnet_iter)
                except StopIteration:
                    return False

                pending[executer.submit(self._scan_subnet_worker, subnet)] = subnet
                return True

            for _ in range(min(self.max_workers, len(self.subnets))):
                submit_next()

            while pending:
                completed, _ = wait(pending, return_when=FIRST_COMPLETED)

                for future in completed:
                    subnet = pending.pop(future)
                    try:
                        results.update(future.result())
                    except Exception as e:
                        self._logger.exception("Error occurred while scanning subnet %s: %s", subnet, e)

                    submit_next()

        elapsed_time = time.time() - start_time
        self.scan_results = results
        self._logger.debug("All threads completed in %.2f seconds.", elapsed_time)
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