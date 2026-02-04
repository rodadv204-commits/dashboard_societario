import streamlit as st

st.set_page_config(
    page_title="Simulador Jurídico – Estruturas Societárias",
    layout="wide"
)

st.title("Simulador Jurídico-Societário para Startups")

st.markdown("""
Este simulador avalia **riscos, custos e adequação jurídica**
dos modelos societários com base em parâmetros reais de mercado.
""")

# ===============================
# ENTRADAS (SIDEBAR)
# ===============================
st.sidebar.header("Parâmetros da Simulação")

modelo = st.sidebar.selectbox(
    "Modelo Societário",
    ["LTDA + Vesting", "Controladora + SPE"]
)

num_devs = st.sidebar.slider(
    "Número de desenvolvedores",
    min_value=1,
    max_value=15,
    value=5
)

percent_vesting = st.sidebar.slider(
    "Percentual total de vesting (%)",
    min_value=1,
    max_value=40,
    value=15
)

vinculo_emprego = st.sidebar.selectbox(
    "Existe vínculo empregatício?",
    ["Não", "Sim"]
)

vesting_milestone = st.sidebar.selectbox(
    "Vesting por milestones?",
    ["Sim", "Não"]
)

lei_do_bem = st.sidebar.selectbox(
    "Empresa usa Lei do Bem?",
    ["Sim", "Não"]
)

investidor = st.sidebar.selectbox(
    "Há expectativa de investimento externo?",
    ["Sim", "Não"]
)

# ===============================
# CÁLCULO DE RISCOS
# ===============================
risco_juridico = 2
risco_trabalhista = 2
atratividade = 3
custo = 2

# Impacto do número de devs
if num_devs > 5:
    risco_trabalhista += 1
    risco_juridico += 1

# Impacto do percentual de vesting
if percent_vesting > 20:
    risco_juridico += 1
    atratividade -= 1

# Vínculo empregatício
if vinculo_emprego == "Não":
    risco_trabalhista += 2
else:
    risco_trabalhista -= 1

# Vesting por milestone
if vesting_milestone == "Não":
    risco_fiscal = 2
else:
    risco_fiscal = 1

# Lei do Bem
if lei_do_bem == "Sim":
    custo -= 1
else:
    custo += 1

# Investidor
if investidor == "Sim":
    if modelo == "LTDA + Vesting":
        atratividade -= 1
    else:
        atratividade += 2

# Modelo SPE
if modelo == "Controladora + SPE":
    risco_juridico -= 1
    custo += 1
    atratividade += 1

# ===============================
# LIMITES
# ===============================
def limitar(valor):
    return max(1, min(valor, 5))

risco_juridico = limitar(risco_juridico)
risco_trabalhista = limitar(risco_trabalhista)
risco_fiscal = limitar(risco_fiscal)
atratividade = limitar(atratividade)
custo = limitar(custo)

# ===============================
# RESULTADOS
# ===============================
st.subheader("Resultado da Simulação")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Risco Jurídico", risco_juridico)
col2.metric("Risco Trabalhista", risco_trabalhista)
col3.metric("Risco Fiscal", risco_fiscal)
col4.metric("Custo Estrutural", custo)
col5.metric("Atratividade Investidor", atratividade)

# ===============================
# INTERPRETAÇÃO JURÍDICA
# ===============================
st.subheader("Análise Jurídica Automática")

if modelo == "LTDA + Vesting" and risco_trabalhista >= 4:
    st.warning("""
    Estrutura vulnerável a requalificação trabalhista.
    Recomenda-se vínculo formal ou SPE.
    """)

if investidor == "Sim" and atratividade <= 2:
    st.error("""
    Estrutura pouco atrativa para investidores institucionais.
    Possível exigência de reorganização societária futura.
    """)

if lei_do_bem == "Sim":
    st.success("""
    Estrutura compatível com incentivos da Lei nº 11.196/2005,
    desde que adotado Lucro Real e compliance técnico-contábil.
    """)

# ===============================
# CONCLUSÃO
# ===============================
st.subheader("Recomendação Final")

if modelo == "Controladora + SPE":
    st.markdown("""
    ✅ **Modelo juridicamente mais robusto**
    
    Indicado quando:
    - ativo tecnológico é central
    - há múltiplos desenvolvedores
    - existe expectativa de investimento
    - é necessário isolar riscos de IP e trabalhistas
    """)
else:
    st.markdown("""
    ⚠️ **Modelo viável, porém com riscos**
    
    Adequado apenas se:
    - poucos desenvolvedores
    - vesting bem limitado
    - forte amarração contratual
    - baixa expectativa de investimento externo
    """)
