# ============================================================ 

# Question 5b: Multi-threaded Weather Data Collector 

# Module: ST5008CEM - Programming For Developers 

# ============================================================ 

# GUI application that: 

#   1. Fetches real-time weather for 5 Nepali cities 

#   2. Uses one thread per city (parallel fetching) 

#   3. Ensures thread-safe GUI updates via queue + after() 

#   4. Compares sequential vs parallel fetch latency 

#   5. Plots a latency bar chart in the GUI 

# 

# API: Open-Meteo (free, no API key required) 

#      https://api.open-meteo.com/ 

# 

# Synchronisation: 

#   Worker threads push results into a thread-safe queue. 

#   The main thread polls the queue every 100ms via root.after() 

#   to safely update Tkinter widgets — avoiding race conditions. 

# ============================================================ 

  

import tkinter as tk 

from tkinter import ttk, messagebox 

import threading 

import queue 

import time 

import json 

import urllib.request 

import urllib.parse 

  

# ── City Configuration ──────────────────────────────────────── 

CITIES = [ 

    {"name": "Kathmandu",  "lat": 27.7172, "lon": 85.3240}, 

    {"name": "Pokhara",    "lat": 28.2096, "lon": 83.9856}, 

    {"name": "Biratnagar", "lat": 26.4525, "lon": 87.2718}, 

    {"name": "Nepalgunj",  "lat": 28.0500, "lon": 81.6167}, 

    {"name": "Dhangadhi",  "lat": 28.6833, "lon": 80.5833}, 

] 

  

# Open-Meteo API endpoint (free, no key needed) 

API_BASE = "https://api.open-meteo.com/v1/forecast" 

  

  

# ── Weather Fetcher ─────────────────────────────────────────── 

  

def fetch_weather(city): 

    """ 

    Fetch current weather for a city from Open-Meteo API. 

    Returns a dict with weather data or an error message. 

    """ 

    params = { 

        "latitude":          city["lat"], 

        "longitude":         city["lon"], 

        "current_weather":   "true", 

        "hourly":            "relativehumidity_2m,surface_pressure", 

        "forecast_days":     1, 

        "timezone":          "Asia/Kathmandu", 

    } 

    url = API_BASE + "?" + urllib.parse.urlencode(params) 

  

    try: 

        start = time.time() 

        with urllib.request.urlopen(url, timeout=10) as resp: 

            data = json.loads(resp.read().decode()) 

        elapsed = time.time() - start 

  

        current = data.get("current_weather", {}) 

        humidity  = data.get("hourly", {}).get("relativehumidity_2m", [None])[0] 

        pressure  = data.get("hourly", {}).get("surface_pressure",    [None])[0] 

  

        return { 

            "city":        city["name"], 

            "temperature": current.get("temperature", "N/A"), 

            "windspeed":   current.get("windspeed",   "N/A"), 

            "weathercode": current.get("weathercode", "N/A"), 

            "humidity":    humidity if humidity is not None else "N/A", 

            "pressure":    pressure if pressure is not None else "N/A", 

            "latency":     round(elapsed, 3), 

            "error":       None, 

        } 

    except Exception as e: 

        return { 

            "city":        city["name"], 

            "temperature": "—", "windspeed": "—", 

            "weathercode": "—", "humidity":  "—", "pressure": "—", 

            "latency":     0, 

            "error":       str(e), 

        } 

  

  

def weather_code_desc(code): 

    """Translate WMO weather code to human-readable description.""" 

    try: 

        code = int(code) 

    except (ValueError, TypeError): 

        return "Unknown" 

    mapping = { 

        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast", 

        45: "Foggy", 48: "Icy fog", 51: "Light drizzle", 53: "Drizzle", 

        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain", 

        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow", 

        80: "Rain showers", 81: "Moderate showers", 82: "Violent showers", 

        95: "Thunderstorm", 96: "Thunderstorm + hail", 

    } 

    return mapping.get(code, f"Code {code}") 

  

  

# ── GUI Application ─────────────────────────────────────────── 

  

class WeatherApp: 

    def __init__(self, root): 

        self.root = root 

        self.root.title("Multi-threaded Weather Collector – Nepal") 

        self.root.geometry("900x680") 

        self.root.configure(bg="#0d1b2a") 

        self.root.resizable(True, True) 

  

        # Thread-safe queue for worker→GUI communication 

        self.result_queue  = queue.Queue() 

        self.results_store = {}          # city name → result dict 

        self._poll_job     = None 

  

        self._build_ui() 

  

    # ── UI Construction ─────────────────────────────────────── 

  

    def _build_ui(self): 

        # Header 

        hdr = tk.Frame(self.root, bg="#1b2a40", pady=10) 

        hdr.pack(fill="x") 

        tk.Label(hdr, text="🌤  Nepal Weather Dashboard", 

                 font=("Helvetica", 16, "bold"), fg="white", bg="#1b2a40").pack() 

        tk.Label(hdr, text="Multi-threaded Real-Time Fetcher  |  ST5008CEM", 

                 font=("Helvetica", 9), fg="#7fb3d3", bg="#1b2a40").pack() 

  

        # Control bar 

        ctrl = tk.Frame(self.root, bg="#0d1b2a", pady=8) 

        ctrl.pack(fill="x", padx=12) 

  

        self.fetch_btn = tk.Button(ctrl, text="⚡  Fetch Weather (Parallel)", 

                                   command=self._fetch_parallel, 

                                   bg="#2e86c1", fg="white", 

                                   font=("Helvetica", 11, "bold"), 

                                   relief="flat", padx=14, pady=6) 

        self.fetch_btn.pack(side="left", padx=4) 

  

        self.seq_btn = tk.Button(ctrl, text="⏱  Fetch Sequential (Compare)", 

                                 command=self._fetch_sequential, 

                                 bg="#117a65", fg="white", 

                                 font=("Helvetica", 10, "bold"), 

                                 relief="flat", padx=12, pady=6) 

        self.seq_btn.pack(side="left", padx=4) 

  

        self.clear_btn = tk.Button(ctrl, text="🗑  Clear", 

                                   command=self._clear, 

                                   bg="#6c757d", fg="white", 

                                   font=("Helvetica", 10), 

                                   relief="flat", padx=10, pady=6) 

        self.clear_btn.pack(side="left", padx=4) 

  

        self.status_var = tk.StringVar(value="Ready. Press 'Fetch Weather' to start.") 

        tk.Label(ctrl, textvariable=self.status_var, 

                 bg="#0d1b2a", fg="#aed6f1", 

                 font=("Helvetica", 9)).pack(side="left", padx=14) 

  

        # Weather table 

        tbl_frm = tk.LabelFrame(self.root, text=" Live Weather Data ", 

                                 font=("Helvetica", 10, "bold"), 

                                 bg="#0d1b2a", fg="#aed6f1", pady=4) 

        tbl_frm.pack(fill="x", padx=12, pady=4) 

  

        style = ttk.Style() 

        style.theme_use("clam") 

        style.configure("Weather.Treeview", 

                         background="#1b2a40", fieldbackground="#1b2a40", 

                         foreground="white", rowheight=26, 

                         font=("Helvetica", 10)) 

        style.configure("Weather.Treeview.Heading", 

                         background="#2e86c1", foreground="white", 

                         font=("Helvetica", 10, "bold")) 

        style.map("Weather.Treeview", background=[("selected", "#2980b9")]) 

  

        cols = ("city", "temp", "humidity", "pressure", "wind", "condition", "latency") 

        self.table = ttk.Treeview(tbl_frm, columns=cols, show="headings", 

                                   height=7, style="Weather.Treeview") 

        headers = { 

            "city":     ("City",           130), 

            "temp":     ("Temp (°C)",       90), 

            "humidity": ("Humidity (%)",   100), 

            "pressure": ("Pressure (hPa)", 110), 

            "wind":     ("Wind (km/h)",     90), 

            "condition":("Condition",       160), 

            "latency":  ("Latency (s)",      90), 

        } 

        for col, (label, width) in headers.items(): 

            self.table.heading(col, text=label) 

            self.table.column(col, width=width, anchor="center") 

        self.table.pack(fill="x", padx=6, pady=4) 

  

        # City status indicators 

        ind_frm = tk.Frame(self.root, bg="#0d1b2a") 