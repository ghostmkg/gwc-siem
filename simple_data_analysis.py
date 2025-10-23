# File name: simple_data_analysis.py

"""
Simple Data Analysis Script

This script demonstrates basic statistical analysis on numerical data such as
sensor readings or event counts.

It calculates mean, median, and mode as foundational analytics useful in many SIEM or monitoring systems.
"""

from statistics import mean, median, mode

def analyze_data(data):
    analysis = {
        "mean": mean(data),
        "median": median(data),
        "mode": mode(data),
    }
    return analysis

if __name__ == "__main__":
    sample_data = [15, 22, 22, 20, 30, 20, 22, 18, 20, 20]
    results = analyze_data(sample_data)
    print("Data Analysis Results:")
    for key, value in results.items():
        print(f"{key.capitalize()}: {value}")
