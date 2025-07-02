import json
import os
import subprocess
import platform
import re
import time

try:
    from simple_active_discovery import simple_discover_all
    USE_SIMPLE_DISCOVERY = True
    USE_ENHANCED_DISCOVERY = False
    USE_SMART_DISCOVERY = False
except ImportError:
    USE_SIMPLE_DISCOVERY = False
    try:
        from enhanced_discovery import enhanced_discover_all
        USE_ENHANCED_DISCOVERY = True
        USE_SMART_DISCOVERY = False
    except ImportError:
        USE_ENHANCED_DISCOVERY = False
        try:
            from smart_log_discovery import discover_all_comfyui_logs
            USE_SMART_DISCOVERY = True
        except ImportError:
            try:
                from advanced_log_discovery import discover_all_comfyui_logs
                USE_SMART_DISCOVERY = True
            except ImportError:
                from log_discovery import discover_comfyui_logs
                USE_SMART_DISCOVERY = False

class ComfyUILogDebugger:
    def __init__(self):
        self.error_patterns = self._load_error_patterns()

    def _load_error_patterns(self):
        """Loads error patterns from error_patterns.json."""
        script_dir = os.path.dirname(__file__)
        patterns_file = os.path.join(script_dir, 'error_patterns.json')
        if os.path.exists(patterns_file):
            with open(patterns_file, 'r') as f:
                return json.load(f)
        return {}

    def get_logs(self):
        """Discovers and returns a list of ComfyUI log files."""
        if USE_SIMPLE_DISCOVERY:
            result = simple_discover_all()
            return {
                "log_files": result['log_files'],
                "installations": result['installations'],
                "discovery_method": result.get('discovery_method', 'simple'),
                "discovery_time": result.get('discovery_time', 0),
                "known_count": result.get('known_count', 0),
                "active_count": result.get('active_count', 0)
            }
        elif USE_ENHANCED_DISCOVERY:
            result = enhanced_discover_all()
            return {
                "log_files": result['log_files'],
                "installations": result['installations'],
                "discovery_method": "enhanced",
                "discovery_time": result.get('discovery_time', 0),
                "cached_count": result.get('cached_count', 0),
                "active_count": result.get('active_count', 0),
                "discovered_count": result.get('discovered_count', 0)
            }
        elif USE_SMART_DISCOVERY:
            result = discover_all_comfyui_logs()
            return {
                "log_files": result['log_files'],
                "installations": result['installations'],
                "discovery_method": "smart",
                "discovery_time": result.get('discovery_time', 0),
                "system_info": result.get('system_info', {})
            }
        else:
            logs = discover_comfyui_logs()
            return {
                "log_files": logs,
                "discovery_method": "basic"
            }

    def tail_log(self, path: str):
        """Tails a specified log file in real-time."""
        if not os.path.exists(path):
            return {"error": f"Log file not found: {path}"}

        system = platform.system()
        command = []
        if system == "Linux" or system == "Darwin":
            command = ["tail", "-f", path]
        elif system == "Windows":
            # PowerShell command to tail a file
            command = ["powershell.exe", "Get-Content", "-Path", path, "-Wait", "-Encoding", "UTF8"]
        else:
            return {"error": f"Unsupported operating system for tailing: {system}"}

        try:
            # Start the subprocess in a non-blocking way
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
            print(f"Tailing log file: {path}. Press Ctrl+C to stop.")
            for line in iter(process.stdout.readline, ''):
                print(line, end='')
            process.wait()
            return {"message": f"Stopped tailing {path}"}
        except Exception as e:
            return {"error": f"Failed to tail log: {e}"}

    def find_errors(self, log_path: str, last_minutes: int = None, context_lines: int = 5):
        """Finds errors in a log file based on defined patterns, with contextual lines.
        If last_minutes is provided, only searches within that timeframe.
        context_lines specifies how many lines before and after the error to include.
        """
        if not os.path.exists(log_path):
            return {"error": f"Log file not found: {log_path}"}

        found_errors = []
        current_time = time.time()

        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if last_minutes:
                # This is a very basic timestamp check. Real-world logs might need more robust parsing.
                # Assuming log lines might start with a timestamp that can be parsed.
                # For now, we'll just check if the file modification time is within the last_minutes.
                # A more accurate approach would involve parsing timestamps from each log line.
                log_mtime = os.path.getmtime(log_path)
                if (current_time - log_mtime) > (last_minutes * 60):
                    continue # Skip lines older than the specified timeframe

            for error_type, patterns in self.error_patterns.items():
                for pattern_str in patterns:
                    if re.search(pattern_str, line, re.IGNORECASE):
                        start_index = max(0, i - context_lines)
                        end_index = min(len(lines), i + context_lines + 1)
                        context = "".join(lines[start_index:end_index]).strip()

                        found_errors.append({
                            "type": error_type,
                            "line_number": i + 1,
                            "error_line": line.strip(),
                            "context": context,
                            "log_file": log_path
                        })
                        break # Found a match for this line, move to next line
        return {"errors": found_errors}

    # Placeholder for future features
    def monitor_gpu_memory_warnings(self, log_path: str):
        """Monitors a log for GPU memory warnings."""
        return {"message": "GPU memory warning monitoring not yet implemented."}

    def find_workflow_by_id(self, workflow_id: str, log_path: str):
        """Finds workflow execution details by ID."""
        return {"message": "Workflow ID search not yet implemented."}


