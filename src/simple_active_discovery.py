"""
Simple Active Discovery for ComfyUI
Focuses on finding active ComfyUI installations and known paths
"""
import os
import json
import subprocess
import platform
from pathlib import Path
from typing import List, Set, Dict
import time

class SimpleActiveDiscovery:
    def __init__(self):
        # Load known paths from .env
        self.known_paths = self._load_known_paths()
        
    def _load_known_paths(self) -> List[str]:
        """Load known paths from .env file"""
        paths = []
        env_file = Path(__file__).parent.parent / '.env'
        
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.strip().startswith('COMFYUI_PATHS='):
                            paths_str = line.split('=', 1)[1].strip()
                            paths = [p.strip() for p in paths_str.split(',') if p.strip()]
                            break
            except:
                pass
                
        return paths
    
    def find_active_comfyui(self) -> Set[str]:
        """Find actively running ComfyUI processes"""
        active = set()
        
        try:
            if platform.system() == "Windows":
                # Use tasklist to find Python processes (skip /V for speed)
                cmd = ['tasklist', '/FO', 'CSV']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                
                # Also try wmic for more detail
                wmic_cmd = 'wmic process where "name=\'python.exe\'" get ProcessId,CommandLine /format:csv'
                wmic_result = subprocess.run(wmic_cmd, shell=True, capture_output=True, text=True, timeout=5)
                
                # Parse wmic output
                for line in wmic_result.stdout.splitlines():
                    if 'main.py' in line and ('--listen' in line or '--port' in line):
                        # This is likely ComfyUI
                        # Extract the directory
                        parts = line.split('"')
                        for i, part in enumerate(parts):
                            if 'python.exe' in part.lower() and i+1 < len(parts):
                                # Next part might be the script
                                script = parts[i+1].strip()
                                if 'main.py' in script:
                                    path = Path(script).parent
                                    if path.exists():
                                        active.add(str(path.resolve()))
                                        print(f"   [ACTIVE] Found running ComfyUI: {path}")
                                        break
            else:
                # Unix-like systems
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                for line in result.stdout.splitlines():
                    if 'python' in line and 'main.py' in line and ('--listen' in line or '--port' in line):
                        parts = line.split()
                        for part in parts:
                            if 'main.py' in part:
                                path = Path(part).parent
                                if path.exists():
                                    active.add(str(path.resolve()))
                                    print(f"   [ACTIVE] Found running ComfyUI: {path}")
                                    break
        except Exception as e:
            print(f"   Error checking processes: {e}")
            
        return active
    
    def verify_installation(self, path: str) -> bool:
        """Verify if a path is a valid ComfyUI installation"""
        required_files = ['main.py', 'nodes.py', 'execution.py']
        path_obj = Path(path)
        
        if not path_obj.exists():
            return False
            
        found = 0
        for file in required_files:
            if (path_obj / file).exists():
                found += 1
                
        return found >= 2  # At least 2 out of 3 required files
    
    def find_log_files(self, installation: str) -> List[str]:
        """Find log files in a ComfyUI installation"""
        logs = []
        path = Path(installation)
        
        # Common log patterns
        patterns = ['*.log', 'console.txt', 'output.txt', 'stderr.txt', 'stdout.txt']
        
        for pattern in patterns:
            for log in path.glob(pattern):
                if log.is_file():
                    logs.append(str(log))
                    
        # Also check logs subdirectory
        logs_dir = path / 'logs'
        if logs_dir.exists():
            for pattern in patterns:
                for log in logs_dir.glob(pattern):
                    if log.is_file():
                        logs.append(str(log))
                        
        return logs
    
    def discover(self) -> Dict:
        """Simple discovery focusing on active and known installations"""
        print("Simple Active ComfyUI Discovery")
        print("-" * 40)
        
        start_time = time.time()
        all_installations = set()
        
        # 1. Check known paths from .env
        print("1. Checking known paths...")
        for path in self.known_paths:
            if self.verify_installation(path):
                all_installations.add(path)
                print(f"   [KNOWN] {path}")
            else:
                print(f"   [INVALID] {path} - not found or incomplete")
        
        # 2. Find active processes
        print("\n2. Checking for running ComfyUI processes...")
        active = self.find_active_comfyui()
        all_installations.update(active)
        
        if not active:
            print("   No active ComfyUI processes found")
            print("   TIP: Start ComfyUI to automatically discover new installations")
        
        # 3. Collect all log files
        print("\n3. Collecting log files...")
        all_logs = []
        
        for installation in all_installations:
            logs = self.find_log_files(installation)
            all_logs.extend(logs)
            if logs:
                print(f"   {installation}: {len(logs)} logs")
        
        # Sort by modification time
        all_logs.sort(key=lambda x: os.path.getmtime(x) if os.path.exists(x) else 0, reverse=True)
        
        elapsed = time.time() - start_time
        
        print(f"\nDiscovery completed in {elapsed:.2f} seconds")
        print(f"Found {len(all_installations)} installations")
        print(f"Found {len(all_logs)} log files")
        
        return {
            'installations': sorted(list(all_installations)),
            'log_files': all_logs,
            'discovery_time': elapsed,
            'known_count': len([p for p in self.known_paths if p in all_installations]),
            'active_count': len(active),
            'discovery_method': 'simple_active'
        }


def simple_discover_all() -> Dict:
    """Main entry point for simple discovery"""
    discovery = SimpleActiveDiscovery()
    return discovery.discover()


if __name__ == '__main__':
    # Test the discovery
    results = simple_discover_all()
    
    print("\n" + "="*50)
    print("RESULTS")
    print("="*50)
    
    if results['installations']:
        print(f"\nInstallations ({len(results['installations'])}):")
        for inst in results['installations']:
            print(f"  - {inst}")
    else:
        print("\nNo ComfyUI installations found!")
        print("\nTips:")
        print("1. Add your ComfyUI path to .env file")
        print("2. Start ComfyUI to enable automatic discovery")
    
    if results['log_files']:
        print(f"\nRecent logs (showing first 5):")
        for log in results['log_files'][:5]:
            print(f"  - {os.path.basename(log)}")