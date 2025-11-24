#!/usr/bin/env python3
import ollama
import reportlab
import mysql.connector

print("🧪 Probando instalaciones...")

# Probar Ollama
try:
    response = ollama.chat(
        model='llama3.1:8b',
        messages=[{'role': 'user', 'content': 'Responde "Sistema TEA OK"'}]
    )
    print("✅ Ollama funcionando:", response['message']['content'][:50] + "...")
except Exception as e:
    print("❌ Ollama error:", e)

# Probar reportlab
try:
    from reportlab.lib.pagesizes import A4
    print("✅ ReportLab funcionando")
except Exception as e:
    print("❌ ReportLab error:", e)

# Probar MySQL
try:
    conn = mysql.connector.connect(host='localhost', user='root')
    print("✅ MySQL conectado")
    conn.close()
except Exception as e:
    print("⚠️  MySQL no conectado (normal si no está configurado):", e)

print("🎯 Pruebas completadas!")

