#!/usr/bin/env python3
"""
Quick script to check if Hugging Face Space is running
Usage: python check_hf.py
"""
import requests
import sys

# Replace with your actual Hugging Face Space URL
HF_SPACE_URL = "https://yandri918-agrisensa-api.hf.space"

def check_space():
    print(f"🔍 Checking Hugging Face Space: {HF_SPACE_URL}")
    print("-" * 60)
    
    try:
        # Check health endpoint
        print("1. Checking /health endpoint...")
        response = requests.get(f"{HF_SPACE_URL}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
            print("   ✅ Health check passed!")
        else:
            print(f"   ❌ Health check failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection Error - Space might still be building")
        return False
    except requests.exceptions.Timeout:
        print("   ❌ Timeout - Space is too slow to respond")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    try:
        # Check home page
        print("\n2. Checking / (home) endpoint...")
        response = requests.get(HF_SPACE_URL, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Home page accessible!")
        else:
            print(f"   ❌ Home page failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    try:
        # Check a module
        print("\n3. Checking /modules/chatbot endpoint...")
        response = requests.get(f"{HF_SPACE_URL}/modules/chatbot", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Module page accessible!")
        else:
            print(f"   ❌ Module page failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Space appears to be running!")
    return True

if __name__ == "__main__":
    success = check_space()
    sys.exit(0 if success else 1)
