"""Pluggable AI backends. Each module exposes one function:

    analyze(image_bytes: bytes, mime_type: str, language: str) -> CropAnalysis

ai/analyzer.py picks which module to call based on the KISANLENS_PROVIDER
environment variable, so app.py and the UI never need to know which AI
backend is actually running.
"""
