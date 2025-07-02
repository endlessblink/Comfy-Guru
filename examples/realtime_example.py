#!/usr/bin/env python3
"""
Example of real-time ComfyUI debugging with the MCP server
"""
from debugger_server import ComfyUILogDebugger
import threading
import time
import os

def simulate_comfyui_activity(log_path):
    """Simulate ComfyUI writing to log file"""
    print("\n🎮 Simulating ComfyUI Activity...")
    
    # Simulate various ComfyUI events
    events = [
        "[2025-07-01 14:05:00.123] Prompt execution started",
        "[2025-07-01 14:05:00.456] Loading checkpoint: sd_xl_base_1.0.safetensors",
        "[2025-07-01 14:05:05.789] Checkpoint loaded successfully",
        "[2025-07-01 14:05:06.123] Executing node: CLIPTextEncode (id: 6)",
        "[2025-07-01 14:05:06.456] ERROR: CLIPTextEncode: 'NoneType' object has no attribute 'encode'",
        "[2025-07-01 14:05:06.789] Traceback (most recent call last):",
        "[2025-07-01 14:05:07.123]   File 'execution.py', line 123, in execute_node",
        "[2025-07-01 14:05:07.456] RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB",
        "[2025-07-01 14:05:07.789] Prompt execution failed",
        "[2025-07-01 14:05:10.123] Clearing GPU cache...",
        "[2025-07-01 14:05:10.456] GPU memory freed: 4.2 GB",
        "[2025-07-01 14:05:15.789] Prompt execution started (retry)",
        "[2025-07-01 14:05:20.123] KSampler: 5/20 steps",
        "[2025-07-01 14:05:25.456] KSampler: 10/20 steps",
        "[2025-07-01 14:05:30.789] KSampler: 15/20 steps",
        "[2025-07-01 14:05:35.123] KSampler: 20/20 steps",
        "[2025-07-01 14:05:35.456] Saving image: ComfyUI_00143.png",
        "[2025-07-01 14:05:35.789] Prompt execution completed successfully"
    ]
    
    # Append events to log file
    with open(log_path, 'a') as f:
        for event in events:
            f.write(event + '\n')
            f.flush()  # Ensure immediate write
            time.sleep(0.5)  # Simulate time between events
            print(f"  📝 Written: {event}")

def monitor_with_mcp(log_path):
    """Show how MCP would analyze in real-time"""
    debugger = ComfyUILogDebugger()
    
    print("\n🔍 MCP Real-time Analysis:")
    print("="*60)
    
    # Wait a bit for some logs to be written
    time.sleep(3)
    
    # Continuously analyze the log
    last_size = 0
    while True:
        try:
            current_size = os.path.getsize(log_path)
            if current_size > last_size:
                # New content detected
                result = debugger.find_errors(log_path, context_lines=2, last_minutes=1)
                errors = result.get('errors', [])
                
                if errors:
                    print(f"\n⚠️  MCP DETECTED {len(errors)} ERRORS:")
                    for error in errors:
                        print(f"  • {error['type']}: Line {error['line_number']}")
                        print(f"    {error['error_line'][:80]}...")
                        
                        # Provide helpful suggestions based on error type
                        if error['type'] == 'CudaError':
                            print("    💡 Suggestion: Reduce batch size or use --lowvram")
                        elif error['type'] == 'NodeError':
                            print("    💡 Suggestion: Check node connections and inputs")
                
                last_size = current_size
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Monitor error: {e}")
            break

if __name__ == "__main__":
    # Create a temporary log file for demo
    test_log = "/tmp/comfyui_demo.log"
    
    print("ComfyUI Real-time Monitoring Demo")
    print("="*60)
    print(f"Demo log: {test_log}")
    
    # Clear/create the log file
    with open(test_log, 'w') as f:
        f.write("[2025-07-01 14:04:00.000] ComfyUI Started\n")
    
    # Start simulation in a thread
    sim_thread = threading.Thread(target=simulate_comfyui_activity, args=(test_log,))
    sim_thread.daemon = True
    sim_thread.start()
    
    # Monitor with MCP
    try:
        monitor_with_mcp(test_log)
    except KeyboardInterrupt:
        print("\n\nDemo stopped.")
    
    # Show final analysis
    print("\n📊 Final Analysis:")
    debugger = ComfyUILogDebugger()
    result = debugger.find_errors(test_log)
    print(f"Total errors found: {len(result.get('errors', []))}")
    
    # Cleanup
    if os.path.exists(test_log):
        os.remove(test_log)