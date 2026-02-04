import streamlit as st
import pandas as pd
import numpy as np

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Dashboard Societário – Simulador Jurídico",
    layout="wide"
)

st.title("Dashboard Comparativo – Tipos Societários e Benefícios Legais")
st.markdown("""
Este simulador avalia **riscos, custos, receita e adequação jurídica**
dos modelos societários para startups brasileiras.
""")

# ===============================
# FUNÇÃO PARA COLORIR COM BOLINHA
# ===============================
def color_ball(val):
    if isinstance(val, str):
        val_lower = val.lower()
        if "alto" in val_lower or "muito" in val_lower:
            return f"🔴 {val}"
        elif "médio" in val_lower:
            return f"🟠 {val}"
        elif "baixo" in val_lower or "sim" in val_lower:
            return f"🟢 {val}"
        else:
            return f"⚪ {val}"
    elif isinstance(val, (int, float)):
        if val >= 5: return f"🔴 {val}"
        elif val == 4: return f"🟠 {val}"
        elif val == 3: return f"🟡 {val}"
        elif val == 2: return f"🟢 {val}"
        else: return f"⚪ {val}"
    else:
        return val

# ===============================
# DADOS BASE (INTEGRAÇÃO TOTAL)
# ===============================
# Adicionando S.A. explicitamente na comparação inicial
df_modelos = pd.DataFrame({
    "Modelo": ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única", "S.A. (Sociedade Anônima)"],
    "Custo Inicial": ["Baixo", "Alto", "Alto", "Muito Alto"],
    "Risco Jurídico": ["Médio", "Alto", "Alto", "Baixo"],
    "Atratividade Investidor": ["Médio", "Alto", "Baixo", "Muito Alto"],
    "Prazo (dias)": ["30-60", "60-120", "90-150", "90+"],
    "Receita Mínima Recomendada": ["0", "R$ 50.000", "R$ 100.000", "R$ 250.000"]
})

tabela_custos_base = pd.DataFrame({
    "Modelo": ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única", "S.A."],
    "Custo abertura": ["Baixo", "Alto", "Muito Alto", "Muito Alto"],
    "Custo manutenção mensal": ["Baixo", "Alto", "Médio/Alto", "Muito Alto"],
    "Custo legal/consultivo": ["Baixo", "Alto", "Muito Alto", "Muito Alto"],
    "Custo contábil": ["Baixo", "Médio/Alto", "Médio/Alto", "Alto"]
})

tabela_manutencao_financeira = pd.DataFrame({
    "Item de Custo": ["Honorários Contábeis (Mensal)", "Taxas Junta Comercial", "Publicações Legais (Anual)", "Certificado Digital (Anual)", "Compliance Societário"],
    "LTDA (Limitada)": ["R$ 350 - R$ 2.000", "R$ 450", "Isento", "R$ 250", "Baixo"],
    "S.A. (Anônima)": ["R$ 2.000 - R$ 10.000", "R$ 1.200", "R$ 5.000+", "R$ 500", "Muito Alto"]
})

tabela_riscos_legais = pd.DataFrame({
    "Tipo de risco": ["Trabalhista", "Tributário", "Societário", "Investidor", "Operacional"],
    "LTDA + Vesting": ["Alto","Médio/Alto","Médio","Médio","Baixo"],
    "Controladora + SPE": ["Médio","Médio","Alto","Médio","Médio"],
    "Nova Sociedade Única": ["Alto","Médio","Alto","Alto","Alto"]
})

tabela_modelos = pd.DataFrame({
    "Critério": [
        "Estrutura", "Entrada dos desenvolvedores", "Titularidade do IP", "Prazo de implementação",
        "Complexidade jurídica", "Custo societário inicial", "Custo mensal recorrente",
        "Flexibilidade para investidores", "Governança", "Controle dos fundadores",
        "Risco trabalhista", "Risco tributário", "Risco societário",
        "Risco para investidor (red flags)", "Facilidade de dissolução", 
        "Custo de reorganização futura", "Adequação a startup early stage", "Vinculação ao Inova Simples"
    ],
    "LTDA + Vesting": [
        "Uma LTDA existente + contratos", "Posterior, via vesting", "LTDA principal desde o início", "Curto (30–60 dias)",
        "Média", "Baixo", "Baixo", "Média", "Mais simples", "Alto",
        "Alto (vesting x vínculo)", "Médio/Alto (requalificação do vesting)", "Médio (entrada futura de sócio)",
        "Vesting mal redigido", "Alta", "Médio", "Boa", "Sim (fase inicial)"
    ],
    "Controladora + SPE": [
        "LTDA controladora + SPE", "Desde o início na SPE (minoritários)", "Inicialmente da SPE, depois transferido", "Médio (60–120 dias)",
        "Alta", "Médio/Alto", "Alto (2 CNPJs)", "Alta", "Mais robusta", "Muito alto",
        "Médio", "Médio", "Alto (conflitos SPE/IP)", "Transferência de IP", "Média", "Alto", "Muito boa", "Sim"
    ],
    "Nova Sociedade Única": [
        "Nova LTDA substituindo a atual", "Desde o início como sócios", "Da nova sociedade", "Longo (90–150 dias)",
        "Alta", "Médio", "Médio", "Média", "Complexa (muitos sócios)", "Médio",
        "Alto", "Médio", "Alto (conflitos diretos)", "Cap table pulverizado", "Baixa", "Muito alto", "Ruim", "Não recomendado"
    ]
})

tabela_tributacao_detalhada = pd.DataFrame({
    "Aspecto": [
        "Custo contábil adicional", "Custo jurídico/consultivo", "Custo compliance",
        "Benefício financeiro potencial", "Risco fiscal", "Segregação de despesas",
        "Compatível com vesting", "Compatível com SPE", "Redução de responsabilidade investidor",
        "Facilidade captação", "Atração investidor-anjo", "Adequação ao regime societário"
    ],
    "Impacto LTDA + Vesting": ["Baixo", "Baixo", "Médio", "Médio", "Alto", "Sim", "Sim", "Não", "Baixa", "Média", "Média", "Boa"],
    "Impacto Controladora + SPE": ["Médio", "Médio", "Alto", "Alto", "Médio", "Sim", "Sim", "Sim", "Alta", "Alta", "Alta", "Excelente"]
})

tabela_lei_bem = pd.DataFrame({
    "Aspecto": ["Regime tributário exigido", "Custo contábil adicional", "Custo jurídico/consultivo",
                "Custo compliance", "Benefício financeiro potencial", "Risco fiscal",
                "Segregação de despesas", "Adequação à SPE", "Adequação à LTDA única"],
    "Impacto": ["Lucro Real", "Alto", "Médio", "Médio", "Alto", "Médio", "Sim", "Excelente", "Boa"]
})

tabela_lc182 = pd.DataFrame({
    "Aspecto": ["Custo direto", "Custo indireto (adequação contratual)", "Redução de risco jurídico",
                "Facilidade para captação", "Compatibilidade com vesting", "Compatibilidade com SPE",
                "Atração de investidor-anjo", "Redução de responsabilidade do investidor"],
    "Impacto": ["Nenhum", "Baixo", "Alta", "Alta", "Alta", "Muito alta", "Alta", "Alta"]
})

tabela_inova = pd.DataFrame({
    "Critério": ["Natureza", "Estágio ideal", "Regime tributário", "Benefício principal", "Foco",
                 "Exige faturamento", "Compatível com vesting", "Compatível com SPE", 
                 "Atração de investidor", "Pode coexistir"],
    "Inova Simples": ["Regime simplificado de abertura", "Pré-receita / MVP", "Simples Nacional",
                      "Redução de burocracia", "Experimentação", "Não", "Sim", "Não recomendado", "Baixa (fase inicial)", "❌ com Lei do Bem"],
    "Lei do Bem (11.196/05)": ["Incentivo fiscal", "Empresa estruturada", "Lucro Real obrigatório",
                               "Redução de IRPJ/CSLL", "Pesquisa e inovação", "Sim", "Indiretamente",
                               "Sim", "Média", "❌ com Inova Simples"],
    "LC 182/21": ["Regime jurídico estrutural", "Todos os estágios", "Indiferente", "Segurança jurídica",
                  "Investimento e governança", "Não", "Sim", "Sim", "Alta", "✅ com ambos"]
})

tabela_sa = pd.DataFrame({
    "Critério": ["Proteção acionistas", "Complexidade jurídica", "Custo inicial", "Custo mensal",
                 "Risco trabalhista", "Risco tributário", "Governança", "Controle fundadores"],
    "LTDA + Vesting": ["Médio","Baixo","Baixo","Baixo","Alto","Médio","Baixo","Muito Alto"],
    "Controladora + SPE": ["Alto","Alto","Médio/Alto","Alto","Médio","Médio","Alto","Médio"],
    "S.A.": ["Muito Alto","Muito Alto","Alto","Alto","Baixo","Baixo","Muito Alto","Baixo"]
})

# DADOS SALARIAIS PARA CÁLCULO DE ROI
salary_df = pd.DataFrame([('Estágio', 1743.4), ('Júnior', 4154.21), ('Pleno', 7840.74), ('Sênior', 15635.35), ('Outro', 19290.08)], columns=['Level', 'Average Salary (R$)'])
programmer_distribution_df = pd.DataFrame([('Pleno', 33.75), ('Sênior', 24.92), ('Júnior', 24.47), ('Outro', 11.76), ('Estágio', 5.1)], columns=['Level', 'Percentage (%)'])

merged_salary_dist_df = pd.merge(salary_df, programmer_distribution_df, on='Level', how='inner')
merged_salary_dist_df['Weighted Salary'] = merged_salary_dist_df['Average Salary (R$)'] * (merged_salary_dist_df['Percentage (%)'] / 100)
overall_average_salary = merged_salary_dist_df['Weighted Salary'].sum()

# ===============================
# ABAS DO DASHBOARD
# ===============================
abas = [
    "Dashboard Geral", "Definições Gerais", "Simulação & ROI",
    "Custos", "Riscos Legais", "Tributação / Benefícios",
    "S.A.", "Conclusão Jurídica", "Pesquisa Salarial DEV"
]
aba_selecionada = st.tabs(abas)

# --- ABA 0: DASHBOARD GERAL ---
with aba_selecionada[0]:
    st.subheader("Comparação Geral dos Modelos Societários")
    st.dataframe(df_modelos.applymap(color_ball), use_container_width=True)

# --- ABA 1: DEFINIÇÕES ---
with aba_selecionada[1]:
    st.subheader("1. Visão Geral da TattooPop")
    st.markdown("""
**Contexto:** Startup SaaS para artistas de tatuagem.  
**Ativos:** IP (Software), Base de Clientes, Contratos de Vesting.
""")
    st.subheader("Tabela Comparativa Detalhada")
    st.dataframe(tabela_modelos.applymap(color_ball), use_container_width=True)

# --- ABA 2: SIMULAÇÃO & ROI (AQUI ESTÁ A NOVA LÓGICA) ---
with aba_selecionada[2]:
    st.subheader("Simulador Interativo de ROI e Viabilidade Jurídica")
    
    col1, col2 = st.columns(2)
    with col1:
        modelo = st.selectbox("Modelo Societário:", ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única", "S.A."])
        num_devs = st.slider("Quantidade de DEVs no projeto:", 1, 30, 5)
        investidor = st.selectbox("Expectativa de Investimento Externo?", ["Não", "Sim"])
    
    with col2:
        lei_do_bem = st.selectbox("Habilitar Benefícios da Lei do Bem?", ["Não", "Sim"])
        aporte = st.number_input("Valor do Aporte Estimado (R$):", value=500000 if investidor == "Sim" else 0)
        custo_gov_sa = st.slider("Custo de Manutenção S.A. (R$/Ano):", 20000, 100000, 45000)

    # Lógica de Cálculo
    folha_anual = (num_devs * overall_average_salary) * 13.3
    economia_lei_bem = (folha_anual * 0.204) if lei_do_bem == "Sim" else 0
    val_premium = aporte * 0.15 if (modelo == "S.A." or modelo == "Controladora + SPE") else 0
    
    custo_base = custo_gov_sa if modelo == "S.A." else (30000 if modelo == "Controladora + SPE" else 12000)
    roi_estimado = ((economia_lei_bem + val_premium - custo_base) / custo_base * 100) if custo_base > 0 else 0

    st.markdown("---")
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Economia (Lei do Bem)", f"R$ {economia_lei_bem:,.0f}")
    res2.metric("Prêmio Governança", f"R$ {val_premium:,.0f}")
    res3.metric("ROI da Estrutura", f"{roi_estimado:.1f}%")
    res4.metric("Atratividade", "⭐⭐⭐⭐⭐" if modelo == "S.A." else "⭐⭐⭐")

# --- ABA 3 A 8: MANTENDO TODAS AS TABELAS ORIGINAIS ---
with aba_selecionada[3]:
    st.subheader("Análise de Custos de Manutenção")
    st.dataframe(tabela_manutencao_financeira.applymap(color_ball), use_container_width=True)
    st.dataframe(tabela_custos_base.applymap(color_ball), use_container_width=True)

with aba_selecionada[4]:
    st.subheader("Matriz de Riscos")
    st.dataframe(tabela_riscos_legais.applymap(color_ball), use_container_width=True)

with aba_selecionada[5]:
    st.subheader("Benefícios Legais e Fiscais")
    st.markdown("### Lei do Bem")
    st.dataframe(tabela_lei_bem.applymap(color_ball), use_container_width=True)
    st.markdown("### Marco Legal das Startups")
    st.dataframe(tabela_lc182.applymap(color_ball), use_container_width=True)

with aba_selecionada[6]:
    st.subheader("Aprofundamento: S.A.")
    st.dataframe(tabela_sa.applymap(color_ball), use_container_width=True)

with aba_selecionada[7]:
    st.subheader("Parecer Final")
    st.success("Recomendação: Iniciar como LTDA, planejar migração para S.A. no primeiro aporte Series A.")

with aba_selecionada[8]:
    st.subheader("Pesquisa Salarial")
    st.markdown(f"**Salário Médio Ponderado:** R$ {overall_average_salary:,.2f}")
    st.dataframe(salary_df, use_container_width=True)