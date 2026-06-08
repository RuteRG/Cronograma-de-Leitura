import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import base64

st.set_page_config(page_title="Cronograma de Leitura - ALCHEMISED 🧠", layout="wide")

# =========================
# DADOS
# =========================

parte2 = [
    "06/06/2026 - Capítulo 22 a 25, páginas 267 até 304",
    "07/06/2026 - Capítulo 25 a 29, páginas 305 até 341",
    "08/06/2026 - Capítulo 29 a 32, páginas 342 até 370",
    "09/06/2026 - Capítulo 32 a 35, páginas 371 até 409",
    "10/06/2026 - Capítulo 35 a 39, páginas 410 até 442",
    "11/06/2026 - Capítulo 39 a 43, páginas 443 até 476",
    "12/06/2026 - Capítulo 43 a 46, páginas 477 até 510",
    "13/06/2026 - Capítulo 46 a 48, páginas 511 até 540",
    "14/06/2026 - Capítulo 48 a 50, páginas 541 até 576",
    "15/06/2026 - Capítulo 50 a 51, páginas 577 até 601",
    "16/06/2026 - Capítulo 51 a 53, páginas 602 até 629",
    "17/06/2026 - Capítulo 53 a 56, páginas 630 até 660",
    "18/06/2026 - Capítulo 56 a 59, páginas 661 até 687",
    "19/06/2026 - Capítulo 59 a 61, páginas 688 até 715",
    "20/06/2026 - Capítulo 61 a 64, páginas 716 até 759",
    "21/06/2026 - Capítulo 64 a 65, páginas 760 até 795",
]

parte1 = [
    "22/06/2026 - Capítulo 01 a 03, páginas 11 até 41",
    "23/06/2026 - Capítulo 03 a 05, páginas 42 até 76",
    "24/06/2026 - Capítulo 05 a 08, páginas 77 até 110",
    "25/06/2026 - Capítulo 08 a 12, páginas 111 até 157",
    "26/06/2026 - Capítulo 12 a 14, páginas 158 até 188",
    "27/06/2026 - Capítulo 14 a 18, páginas 189 até 224",
]

parte3 = [
    "28/06/2026 - Capítulo 66 a 69, páginas 799 até 831",
    "29/06/2026 - Capítulo 69 a 72, páginas 832 até 867",
    "30/06/2026 - Capítulo 72 a 75, páginas 868 até 900",
    "01/07/2026 - Capítulo 75 a 77, páginas 901 até 928",
    "02/07/2026 - Capítulo 77 a Epílogo, páginas 929 até 955",
]

partes = {
    "Parte 2 (06/06 a 21/06)": parte2,
    "Parte 1 (22/06 a 27/06)": parte1,
    "Parte 3 (28/06 a 02/07)": parte3,
}

st.title("📚 Cronograma de Leitura - ALCHEMISED 🧠")

# =========================
# TABELAS INTERATIVAS
# =========================

for nome, leituras in partes.items():
    chave = f"df_{nome}"

    if chave not in st.session_state:
        st.session_state[chave] = pd.DataFrame({
            "Leitura": leituras,
            "Concluído": [False] * len(leituras)
        })

    st.subheader(nome)

    df = st.data_editor(
        st.session_state[chave],
        hide_index=True,
        use_container_width=True,
        key=f"editor_{nome}"
    )

    st.session_state[chave] = df

    concluidos = int(df["Concluído"].sum())
    total = len(df)
    percentual = concluidos / total

    st.progress(percentual)
    st.write(f"{concluidos} de {total} leituras concluídas ({percentual*100:.1f}%)")

# =========================
# PROGRESSO GERAL
# =========================

todos = pd.concat(
    [st.session_state[f"df_{nome}"] for nome in partes.keys()],
    ignore_index=True
)

geral_concluidos = int(todos["Concluído"].sum())
geral_total = len(todos)

st.header("📊 Progresso Geral")
st.progress(geral_concluidos / geral_total)
st.write(
    f"{geral_concluidos} de {geral_total} leituras concluídas "
    f"({(geral_concluidos/geral_total)*100:.1f}%)"
)

# =========================
# PDF COM FUNDO + RETÂNGULO CLARO
# =========================

def add_page_with_bg(pdf, bg_path):
    pdf.add_page()
    pdf.image(bg_path, x=0, y=0, w=210, h=297)  # fundo em cada página

pdf = FPDF()

# Capa
add_page_with_bg(pdf, "img/alchemised.png")
pdf.set_y(60)
pdf.set_font("Arial", "B", 20)
pdf.set_text_color(200, 0, 0)  # vermelho escuro
pdf.cell(190, 12, "ALCHEMISED", ln=1, align="C")

pdf.set_font("Arial", "", 14)
pdf.set_text_color(50, 50, 50)  # cinza escuro
pdf.cell(190, 10, "Cronograma de Leitura", ln=1, align="C")
pdf.ln(10)

pdf.set_text_color(0, 0, 0)  # preto
pdf.cell(190, 10, f"Progresso Geral: {geral_concluidos}/{geral_total}", ln=1, align="C")

# Partes
for nome in partes.keys():
    add_page_with_bg(pdf, "img/alchemised.png")
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(200, 0, 0)  # vermelho escuro para título da parte
    pdf.cell(190, 10, nome, ln=1, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(255, 255, 255)  # branco para cabeçalho da tabela
    pdf.cell(160, 10, "Leitura", border=1)
    pdf.cell(30, 10, "Status", border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(0, 0, 0)  # preto para conteúdo
    for _, row in st.session_state[f"df_{nome}"].iterrows():
        status = "[X]" if row["Concluído"] else "[ ]"
        pdf.cell(160, 8, str(row["Leitura"])[:75], border=1)
        pdf.cell(30, 8, status, border=1, align="C")
        pdf.ln()

# Exportar PDF
buffer = BytesIO()
pdf_bytes = pdf.output(dest="S").encode("latin-1")  # converte para bytes
buffer.write(pdf_bytes)
buffer.seek(0)

st.download_button(
    label="📥 Baixar PDF com fundo",
    data=buffer,
    file_name="cronograma.pdf",
    mime="application/pdf"
)

# =========================
# FUNDO NA APLICAÇÃO STREAMLIT
# =========================

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: 
                linear-gradient(
                    rgba(255,255,255,0.4),
                    rgba(255,255,255,0.4)
                ),
                url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        h1, h2, h3, p, label {{
            color: black !important;
            text-shadow: 1px 1px 4px white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_local("img/alchemised.png")
