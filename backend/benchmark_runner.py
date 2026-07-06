import argparse
import json
import time
import requests
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Run benchmarks against CodeLens AI API")
    parser.add_argument("--target", choices=["local", "prod"], default="prod", help="Target environment")
    args = parser.parse_args()

    if args.target == "local":
        base_url = "http://127.0.0.1:8000/api/review"
    else:
        base_url = "https://codelens-ai-ixqc.onrender.com/api/review"
    
    dataset_path = os.path.join(os.path.dirname(__file__), "benchmarks/dataset.json")
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        sys.exit(1)
        
    with open(dataset_path, "r") as f:
        dataset = json.load(f)
        
    results = []
    
    print(f"Starting benchmarks against {base_url}...")
    print("-" * 50)
    
    for i, item in enumerate(dataset):
        print(f"Running Test {i+1}: {item['name']}")
        start_time = time.time()
        
        payload = {
            "code": item["code"],
            "language": item["language"]
        }
        
        try:
            resp = requests.post(base_url, json=payload)
            elapsed = time.time() - start_time
            time.sleep(5) # Prevent 429 rate limiting on Free Tier
            
            if resp.status_code == 200:
                data = resp.json()
                print(f"  [SUCCESS] Time: {elapsed:.2f}s")
                results.append({
                    "test": item["name"],
                    "status": "Success",
                    "time_seconds": elapsed,
                    "response": data
                })
            else:
                print(f"  [FAILED] Status {resp.status_code}. Time: {elapsed:.2f}s")
                print(f"  Response: {resp.text}")
                results.append({
                    "test": item["name"],
                    "status": f"Failed ({resp.status_code})",
                    "time_seconds": elapsed,
                    "response": resp.text
                })
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"  [ERROR] {str(e)}")
            results.append({
                "test": item["name"],
                "status": "Error",
                "time_seconds": elapsed,
                "response": str(e)
            })
            
    print("-" * 50)
    
    with open("benchmark_results_raw.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print("Done! Results saved to benchmark_results_raw.json")

if __name__ == "__main__":
    main()
