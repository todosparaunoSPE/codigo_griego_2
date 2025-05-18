# -*- coding: utf-8 -*-
"""
Created on Thu May 15 19:31:05 2025

@author: jahop
"""

import streamlit as st
import urllib.parse

# Mapeo de letras griegas a español
griego_a_espanol = {
    'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e',
    'ζ': 'z', 'η': 'h', 'θ': 'th', 'ι': 'i', 'κ': 'k',
    'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'x', 'ο': 'o',
    'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't',
    'υ': 'y', 'φ': 'ph', 'χ': 'ch', 'ψ': 'ps', 'ω': 'w',
    'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E',
    'Ζ': 'Z', 'Η': 'H', 'Θ': 'Th', 'Ι': 'I', 'Κ': 'K',
    'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'X', 'Ο': 'O',
    'Π': 'P', 'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'Y',
    'Φ': 'Ph', 'Χ': 'Ch', 'Ψ': 'Ps', 'Ω': 'W'
}

# Mapeo inverso (español a griego)
espanol_a_griego = {v: k for k, v in griego_a_espanol.items()}

def traducir_griego_a_espanol(texto):
    resultado = []
    i = 0
    n = len(texto)
    while i < n:
        for length in [2, 1]:  # Primero intentamos con 2 caracteres, luego con 1
            if i + length <= n:
                substring = texto[i:i+length]
                if substring in griego_a_espanol:
                    resultado.append(griego_a_espanol[substring])
                    i += length
                    break
        else:
            resultado.append(texto[i])
            i += 1
    return ''.join(resultado)

def traducir_espanol_a_griego(texto):
    resultado = []
    i = 0
    n = len(texto)
    while i < n:
        for length in [2, 1]:  # Primero intentamos con 2 caracteres (para dígrafos como 'ph', 'th', etc.)
            if i + length <= n:
                substring = texto[i:i+length].lower()
                if substring in espanol_a_griego:
                    # Mantenemos la capitalización original
                    if texto[i:i+length].istitle():
                        traducido = espanol_a_griego[substring].title()
                    elif texto[i:i+length].isupper():
                        traducido = espanol_a_griego[substring].upper()
                    else:
                        traducido = espanol_a_griego[substring]
                    resultado.append(traducido)
                    i += length
                    break
        else:
            resultado.append(texto[i])
            i += 1
    return ''.join(resultado)

def crear_enlace_whatsapp(mensaje):
    texto_codificado = urllib.parse.quote(mensaje)
    return f"https://wa.me/?text={texto_codificado}"

# Configuración del sidebar con emojis y estilo más juvenil
with st.sidebar:
    st.title("📌 Información")
    st.markdown("---")
    st.markdown("### 🧑‍💻 Creado por:")
    st.markdown("**irepohaj**")
    st.markdown("---")
   
    st.markdown("---")
    st.markdown("### 📝 Instrucciones:")
    st.write("""
    1. 🔘 Selecciona la operación deseada  
    2. ⌨️ Introduce tu texto  
    3. 🖱️ Haz clic en el botón correspondiente  
    4. 📋 Copia el texto generado  
    5. 📱 Comparte por WhatsApp  
    """)

# Configuración de la app principal con más estilo
st.title("🔠 CryptoChat Ultra 🏛️")
st.markdown("### Generador y Traductor de Código 🔐")
st.markdown("*¡Crea mensajes secretos con tus amigos usando CryptoChat Ultra!* 🤫✨")

# Divider con emoji
st.markdown("---")

# Opciones con emojis más grandes
opcion = st.radio("Selecciona una opción:", 
                 ("🔤 Generar código", "🔍 Traducir código a español"),
                 horizontal=True)

# Animación de carga personalizada
from time import sleep

def mostrar_animacion():
    with st.empty():
        for i in range(3):
            st.markdown("🔍 Traduciendo" + "." * (i + 1))
            sleep(0.3)
        st.markdown("✅ ¡Listo!")

if opcion == "🔤 Generar código":
    # Limpiar variables de traducción si existen
    if 'texto_traducido' in st.session_state:
        del st.session_state.texto_traducido
        del st.session_state.texto_griego_original
    
    texto_original = st.text_area("✏️ Introduce el texto en español para convertir a código:", 
                                height=150, 
                                placeholder="Escribe aquí tu texto en español...",
                                help="Puedes escribir cualquier mensaje que quieras convertir a griego")

    if st.button("✨ Generar Código Griego ✨", type="primary"):
        if texto_original:
            with st.spinner('🔮 Transformando tu texto...'):
                sleep(1)
                texto_griego = traducir_espanol_a_griego(texto_original)
                st.balloons()
                
                st.subheader("🎉 Resultado:")
                st.markdown("```\n" + texto_griego + "\n```")
                st.text_area("📋 Copia el código manualmente:", texto_griego, height=100)
                
                # Guardar en session_state para WhatsApp
                st.session_state.texto_griego = texto_griego
                
                # Consejo adicional
                st.markdown("💡 *¡Ahora puedes enviar este código secreto a tus amigos!*")
        else:
            st.warning("⚠️ Por favor introduce un texto para generar el código.")
else:
    # Limpiar variables de generación si existen
    if 'texto_griego' in st.session_state:
        del st.session_state.texto_griego
    
    texto_griego = st.text_area("🔍 Introduce el código para traducir a español:", 
                              height=150, 
                              placeholder="Escribe aquí tu texto en griego...",
                              help="Pega aquí el texto en griego que recibiste")

    if st.button("🔎 Traducir a Español 🔍", type="primary"):
        if texto_griego:
            mostrar_animacion()
            texto_traducido = traducir_griego_a_espanol(texto_griego)
            
            st.subheader("🎯 Resultado:")
            st.markdown("```\n" + texto_traducido + "\n```")
            st.text_area("📋 Copia la traducción manualmente:", texto_traducido, height=100)
            
            # Guardar en session_state para WhatsApp
            st.session_state.texto_traducido = texto_traducido
            st.session_state.texto_griego_original = texto_griego
            
            # Emoji de celebración
            st.markdown("🥳 *¡Mensaje descifrado con éxito!*")
        else:
            st.warning("⚠️ Por favor introduce un código para traducir.")

# Mostrar botones de WhatsApp correspondientes a la opción actual
if opcion == "🔤 Generar código" and 'texto_griego' in st.session_state:
    mensaje1 = f"\n{st.session_state.texto_griego}"
    mensaje2 = "🤫 ¿Quieres traducir el código secreto que te ha llegado? 🏛️\nVisita:\nhttps://codigogriego2-wxw4rpy9esfx7hfe6vrbm8.streamlit.app/"
    enlace1 = crear_enlace_whatsapp(mensaje1)
    enlace2 = crear_enlace_whatsapp(mensaje2)

    st.markdown("---")
    st.subheader("📱 Compartir por WhatsApp:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<a href="{enlace1}" target="_blank"><button style="background-color:#25D366;color:white;border:none;border-radius:10px;padding:12px;width:100%;font-size:16px;">📤 1° Envía el código secreto</button></a>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<a href="{enlace2}" target="_blank"><button style="background-color:#128C7E;color:white;border:none;border-radius:10px;padding:12px;width:100%;font-size:16px;">🔗 2° Envía el enlace para descifrar</button></a>', unsafe_allow_html=True)

elif opcion == "🔍 Traducir código a español" and 'texto_traducido' in st.session_state:
    mensaje1 = f"🔓 Traducción del código secreto:\n\n🏛️ Original: {st.session_state.texto_griego_original}\n\n🇪🇸 Traducción: {st.session_state.texto_traducido}"
    mensaje2 = "🔤 ¿Quieres generar o traducir código griego? 🏛️\nVisita:\nhttps://codigogriego2-wxw4rpy9esfx7hfe6vrbm8.streamlit.app/
"
    enlace1 = crear_enlace_whatsapp(mensaje1)
    enlace2 = crear_enlace_whatsapp(mensaje2)

    st.markdown("---")
    st.subheader("📱 Compartir por WhatsApp:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<a href="{enlace1}" target="_blank"><button style="background-color:#25D366;color:white;border:none;border-radius:10px;padding:12px;width:100%;font-size:16px;">📤 Enviar Traducción</button></a>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<a href="{enlace2}" target="_blank"><button style="background-color:#128C7E;color:white;border:none;border-radius:10px;padding:12px;width:100%;font-size:16px;">🔗 Enlace para cifrar/descifrar</button></a>', unsafe_allow_html=True)

# Pie de página con más estilo
st.markdown("---")
st.markdown("### 🎮 ¡Diviértete creando mensajes secretos con tus amigos!")
st.markdown("🌟 *Pro tip: Usa este código para pasar notas en clase sin que el profesor entienda* 😉")
