#!/usr/bin/env python
"""
Simple launcher to start both Frontend and Backend
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

def start_backend():
    """Start Flask backend server"""
    print("\n" + "="*70)
    print("  🚀 STARTING BACKEND API SERVER")
    print("="*70 + "\n")
    
    try:
        backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
        subprocess.run([sys.executable, "app.py"], 
                      cwd=backend_dir)
    except KeyboardInterrupt:
        print("\n⏹️  Backend server stopped")

def start_frontend():
    """Open frontend in default browser"""
    time.sleep(2)  # Wait for backend to start
    
    print("\n" + "="*70)
    print("  🌐 OPENING FRONTEND IN BROWSER")
    print("="*70 + "\n")
    
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "index.html")
    
    if os.path.exists(frontend_path):
        webbrowser.open('file://' + frontend_path)
        print(f"✅ Opened: {frontend_path}\n")
    else:
        print(f"❌ Frontend not found at: {frontend_path}\n")

def main():
    print("\n" + "="*70)
    print("  📱 PHONE RECOMMENDATION AI - LAUNCHER")
    print("="*70)
    print("\n✅ Features:")
    print("   🔍 Search by budget, brand, specs")
    print("   👥 Recommendations by user type")
    print("   📊 Compare phones by categories")
    print("   🏪 Compare Flipkart vs Amazon")
    print("   🎉 View daily deals")
    print("\n" + "="*70 + "\n")
    
    # Start frontend in separate thread
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    
    # Start backend (blocks main thread)
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher closed")
        sys.exit(0)

if __name__ == "__main__":
    main()
