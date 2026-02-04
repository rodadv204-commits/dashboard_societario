import streamlit as st
import pandas as pd

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


def limitar(valor):
    """Função para limitar valores entre 1 e 5"""
    return max(1, min(valor, 5))


def parse_and_fill_salaries(salaries_str, num_devs_for_level, average_salary):
    parsed_salaries = []
    if salaries_str:
        raw_salaries = salaries_str.replace(' ', '').replace('.', '').replace(',', '.').split(',')
        for s in raw_salaries:
            try:
                parsed_salaries.append(float(s))
            except ValueError:
                continue

    while len(parsed_salaries) < num_devs_for_level:
        parsed_salaries.append(average_salary)

    return parsed_salaries[:num_devs_for_level]

# ===============================
# DADOS BASE
# ===============================

df_modelos = pd.DataFrame({
    "Modelo": ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única"],
    "Custo Inicial": ["Baixo", "Alto", "Alto"],
    "Risco Jurídico": ["Médio", "Alto", "Alto"],
    "Atratividade Investidor": ["Médio", "Alto", "Baixo"],
    "Prazo (dias)": ["Curto (30–60)", "Médio (60–120)", "Longo (90–150)"],
    "Receita Mínima Recomendada": ["0", "R$ 50.000", "R$ 100.000"]
})

# Aplicar color_ball ao df_modelos
df_modelos_display = df_modelos.copy()
for col in df_modelos_display.columns:
    if col != "Modelo":
        df_modelos_display[col] = df_modelos_display[col].apply(color_ball)

tabela_custos_base = pd.DataFrame({
    "Modelo": ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única"],
    "Custo abertura": ["Baixo", "Alto", "Muito Alto"],
    "Custo manutenção mensal": ["Baixo", "Alto", "Médio/Alto"],
    "Custo legal/consultivo": ["Baixo", "Alto", "Muito Alto"],
    "Custo contábil": ["Baixo", "Médio/Alto", "Médio/Alto"]
})

tabela_custos_base_display = tabela_custos_base.copy()
for col in tabela_custos_base_display.columns:
    if col != "Modelo":
        tabela_custos_base_display[col] = tabela_custos_base_display[col].apply(color_ball)

tabela_manutencao_financeira = pd.DataFrame({
    "Item de Custo": ["Honorários Contábeis (Mensal)", "Taxas Junta Comercial", "Publicações Legais (Anual)", "Certificado Digital (Anual)", "Compliance Societário"],
    "LTDA (Limitada)": ["R$ 350 - R$ 2.000", "R$ 450", "Isento", "R$ 250", "Baixo"],
    "S.A. (Anônima)": ["R$ 2.000 - R$ 10.000", "R$ 1.200", "R$ 5.000+", "R$ 500", "Muito Alto"]
})

tabela_manutencao_display = tabela_manutencao_financeira.copy()
for col in tabela_manutencao_display.columns:
    if col != "Item de Custo":
        tabela_manutencao_display[col] = tabela_manutencao_display[col].apply(color_ball)

tabela_riscos_legais = pd.DataFrame({
    "Tipo de risco": ["Trabalhista", "Tributário", "Societário", "Investidor", "Operacional"],
    "LTDA + Vesting": ["Alto","Médio/Alto","Médio","Médio","Baixo"],
    "Controladora + SPE": ["Médio","Médio","Alto","Médio","Médio"],
    "Nova Sociedade Única": ["Alto","Médio","Alto","Alto","Alto"]
})

tabela_riscos_display = tabela_riscos_legais.copy()
for col in tabela_riscos_display.columns:
    if col != "Tipo de risco":
        tabela_riscos_display[col] = tabela_riscos_display[col].apply(color_ball)

tabela_modelos_completa = pd.DataFrame({
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

tabela_modelos_display = tabela_modelos_completa.copy()
for col in tabela_modelos_display.columns:
    if col != "Critério":
        tabela_modelos_display[col] = tabela_modelos_display[col].apply(color_ball)

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

tabela_tributacao_display = tabela_tributacao_detalhada.copy()
for col in tabela_tributacao_display.columns:
    if col != "Aspecto":
        tabela_tributacao_display[col] = tabela_tributacao_display[col].apply(color_ball)

tabela_lei_bem = pd.DataFrame({
    "Aspecto": ["Regime tributário exigido", "Custo contábil adicional", "Custo jurídico/consultivo",
                "Custo compliance", "Benefício financeiro potencial", "Risco fiscal",
                "Segregação de despesas", "Adequação à SPE", "Adequação à LTDA única"],
    "Impacto": ["Lucro Real", "Alto", "Médio", "Médio", "Alto", "Médio", "Sim", "Excelente", "Boa"]
})

tabela_lei_bem_display = tabela_lei_bem.copy()
for col in tabela_lei_bem_display.columns:
    if col != "Aspecto":
        tabela_lei_bem_display[col] = tabela_lei_bem_display[col].apply(color_ball)

tabela_lc182 = pd.DataFrame({
    "Aspecto": ["Custo direto", "Custo indireto (adequação contratual)", "Redução de risco jurídico",
                "Facilidade para captação", "Compatibilidade com vesting", "Compatibilidade com SPE",
                "Atração de investidor-anjo", "Redução de responsabilidade do investidor"],
    "Impacto": ["Nenhum", "Baixo", "Alta", "Alta", "Alta", "Muito alta", "Alta", "Alta"]
})

tabela_lc182_display = tabela_lc182.copy()
for col in tabela_lc182_display.columns:
    if col != "Aspecto":
        tabela_lc182_display[col] = tabela_lc182_display[col].apply(color_ball)

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

tabela_inova_display = tabela_inova.copy()
for col in tabela_inova_display.columns:
    if col != "Critério":
        tabela_inova_display[col] = tabela_inova_display[col].apply(color_ball)

tabela_sa = pd.DataFrame({
    "Critério": ["Proteção acionistas", "Complexidade jurídica", "Custo inicial", "Custo mensal",
                 "Risco trabalhista", "Risco tributário", "Governança", "Controle fundadores"],
    "LTDA + Vesting": ["Médio","Baixo","Baixo","Baixo","Alto","Médio","Baixo","Muito Alto"],
    "Controladora + SPE": ["Alto","Alto","Médio/Alto","Alto","Médio","Médio","Alto","Médio"],
    "S.A.": ["Muito Alto","Muito Alto","Alto","Alto","Baixo","Baixo","Muito Alto","Baixo"]
})

tabela_sa_display = tabela_sa.copy()
for col in tabela_sa_display.columns:
    if col != "Critério":
        tabela_sa_display[col] = tabela_sa_display[col].apply(color_ball)

salary_df = pd.DataFrame([('Estágio', 1743.4), ('Júnior', 4154.21), ('Pleno', 7840.74), ('Sênior', 15635.35), ('Outro (Especialista, Tech Lead, Principal)', 19290.08)], columns=['Level', 'Average Salary (R$)'])
programmer_distribution_df = pd.DataFrame([('Pleno', 33.75), ('Sênior', 24.92), ('Júnior', 24.47), ('Outro (Especialista, Tech Lead, Principal)', 11.76), ('Estágio', 5.1)], columns=['Level', 'Percentage (%)'])
area_distribution_df = pd.DataFrame([('Full-Stack', 37.42), ('Back-End', 30.06), ('Front-End', 9.06), ('Dados (BI, Data Science)', 5.45), ('Mobile', 5.4)], columns=['Area', 'Percentage (%)'])

merged_salary_dist_df = pd.merge(salary_df, programmer_distribution_df, on='Level', how='inner')
merged_salary_dist_df['Weighted Salary'] = merged_salary_dist_df['Average Salary (R$)'] * (merged_salary_dist_df['Percentage (%)'] / 100)
overall_average_salary = merged_salary_dist_df['Weighted Salary'].sum()

# Ensure overall_average_salary has a valid default
if overall_average_salary == 0 or pd.isna(overall_average_salary):
    overall_average_salary = 8500.00


# ===============================
# ABAS DO DASHBOARD
# ===============================
abas = [
    "Dashboard Geral", "Definições Gerais", "Simulação & ROI",
    "Custos", "Riscos Legais", "Tributação / Benefícios",
    "S.A.", "Conclusão Jurídica", "Pesquisa Salarial DEV"
]
aba_selecionada = st.tabs(abas)

st.markdown("---")

# --- 0. DASHBOARD GERAL ---
with aba_selecionada[0]:
    st.header("📊 Matriz Comparativa de Modelos")
    st.info("""
    A tabela abaixo cruza **18 critérios técnicos** para determinar qual estrutura 
    suporta melhor o crescimento da TattooPop sem gerar passivos ocultos.
    """)

    # Filtro opcional por modelo
    col_filter1, col_filter2, col_filter3 = st.columns([1, 1, 2])
    with col_filter1:
        filtro_modelo = st.multiselect(
            "Filtrar por modelo:",
            ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única"],
            default=["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única"],
            key="filtro_modelos"
        )

    with col_filter2:
        filtro_criterio = st.text_input(
            "Buscar critério:",
            placeholder="ex: Risco, Custo...",
            key="filtro_criterio_input"
        )

    with col_filter3:
        st.write("")  # Espaço em branco para alinhamento

    # Aplicar filtros
    tabela_filtrada = tabela_modelos_display.copy()

    if filtro_criterio:
        tabela_filtrada = tabela_filtrada[
            tabela_filtrada["Critério"].str.contains(filtro_criterio, case=False, na=False)
        ]

    # Reordenar colunas com base na seleção
    colunas = ["Critério"]
    colunas.extend(filtro_modelo)
    tabela_filtrada = tabela_filtrada[colunas] if all(col in tabela_filtrada.columns for col in colunas) else tabela_filtrada

    # Garantia de segurança

if len(filtro_modelo) == 0:
    st.warning("Selecione ao menos um modelo para exibição.")

else:
    column_cfg = {
        "Critério": st.column_config.TextColumn(width="large")
    }

    for modelo in filtro_modelo:
        if modelo in tabela_filtrada.columns:
            column_cfg[modelo] = st.column_config.TextColumn(width="medium")


    for modelo in filtro_modelo:
        if modelo in tabela_filtrada.columns:
            column_cfg[modelo] = st.column_config.TextColumn(width="medium")

    st.dataframe(
        tabela_filtrada,
        use_container_width=True,
        column_config=column_cfg,
        hide_index=True,
        height=500
    )


    # Adicionar resumo visual
    st.markdown("---")
    st.subheader("📈 Legenda de Riscos")

    legenda_col1, legenda_col2, legenda_col3, legenda_col4, legenda_col5 = st.columns(5)
    with legenda_col1:
        st.markdown("**🔴 Alto/Muito**\nAlto risco")
    with legenda_col2:
        st.markdown("**🟠 Médio**\nRisco moderado")
    with legenda_col3:
        st.markdown("**🟡 3/Neutral**\nNeutro")
    with legenda_col4:
        st.markdown("**🟢 Baixo/Sim**\nBaixa/Sim")
    with legenda_col5:
        st.markdown("**⚪ Outro**\nNão aplicável")

    st.markdown("""
    > **Nota Técnica:** Os critérios de **Risco Trabalhista** e **Tributário** consideram a jurisprudência atual do TST e CARF sobre contratos de Vesting e Stock Options.
    """)

    # Adicionar export
    col_export1, col_export2 = st.columns(2)
    with col_export1:
        csv_data = tabela_filtrada.to_csv(index=False)
        st.download_button(
            label="⬇️ Exportar Tabela (CSV)",
            data=csv_data,
            file_name="matriz_comparativa_modelos.csv",
            mime="text/csv"
        )

    with col_export2:
        st.info("💡 **Dica:** Use os filtros acima para focar em critérios específicos ou comparar apenas alguns modelos.")

# --- 1. DEFINIÇÕES GERAIS ---
with aba_selecionada[1]:
    st.header("📖 Sumário Executivo e Teses Jurídicas")
    
    col_negocio, col_juridico = st.columns([1, 1])
    
    with col_negocio:
        st.subheader("🚀 O Negócio: TattooPop")
        st.markdown("""
        A **TattooPop** opera como um ecossistema digital para o mercado de *body art*, 
        focada em desintermediar a relação entre artistas e clientes via tecnologia.
        
        **Pilares de Valor:**
        * **SaaS B2B:** Gestão completa para tatuadores (finanças e CRM).
        * **Marketplace B2C:** Experiência de agendamento para o usuário final.
        * **IP-Centric:** O valor da empresa reside no software e na base de dados.
        """)
    
    with col_juridico:
        st.subheader("⚖️ Teses Societárias")
        st.markdown("""
        O desafio jurídico reside em equilibrar a **retenção de talentos (DEVs)** com a **proteção da Propriedade Intelectual (IP)**, preparando a casa 
        para rodadas de investimento (Angel/Seed).
        
        **Premissas Adotadas:**
        * Mitigação de risco trabalhista em contratos de Vesting.
        * Eficiência tributária via enquadramento estratégico.
        * Segurança contratual para fundadores e minoritários.
        """)

# --- 2. SIMULAÇÃO & ROI INTERATIVO ---
with aba_selecionada[2]:
    st.subheader("Simulador Interativo de ROI Societário")

    st.markdown("""
    Ajuste os parâmetros abaixo para simular **riscos, custos e atratividade** dos modelos societários.
    """)

    col1, col2 = st.columns(2)

    # Define all input variables in the appropriate scope
    with col1:
        modelo = st.selectbox(
            "Escolha o modelo societário:",
            ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única", "S.A."]
        )

        num_devs = st.slider(
            "Número de desenvolvedores",
            min_value=1,
            max_value=15,
            value=5
        )

        percent_vesting = st.slider(
            "Percentual total de vesting (%)",
            min_value=1,
            max_value=40,
            value=15
        )

        vinculo_emprego = st.selectbox(
            "Existe vínculo empregatício?",
            ["Não", "Sim"]
        )

    with col2:
        vesting_milestone = st.selectbox(
            "Vesting por milestones?",
            ["Sim", "Não"]
        )

        lei_do_bem = st.selectbox(
            "Empresa usa Lei do Bem?",
            ["Sim", "Não"]
        )

        investidor = st.selectbox(
            "Há expectativa de investimento externo?",
            ["Sim", "Não"]
        )

        aporte = st.number_input(
            "Valor do aporte do investidor (R$)",
            value=500_000
        )
        custo_anual_Sa = st.number_input(
            "Custo anual da estrutura S.A. (R$)",
            value=1100_000
        )

    risco_juridico = 2
    risco_trabalhista = 2
    risco_fiscal = 2
    atratividade = 3
    custo = 2

    if num_devs > 5:
        risco_trabalhista += 1
        risco_juridico += 1

    if percent_vesting > 20:
        risco_juridico += 1
        atratividade -= 1

    if vinculo_emprego == "Não":
        risco_trabalhista += 2
    else:
        risco_trabalhista -= 1

    if vesting_milestone == "Não":
        risco_fiscal += 1

    if lei_do_bem == "Sim":
        custo -= 1
    else:
        custo += 1

    if investidor == "Sim":
        if modelo == "LTDA + Vesting":
            atratividade -= 1
        else:
            atratividade += 2

    if modelo == "Controladora + SPE":
        risco_juridico -= 1
        custo += 1
        atratividade += 1

    risco_juridico = limitar(risco_juridico)
    risco_trabalhista = limitar(risco_trabalhista)
    risco_fiscal = limitar(risco_fiscal)
    atratividade = limitar(atratividade)
    custo = limitar(custo)

    custo_folha_anual = (num_devs * overall_average_salary) * 13.3
    if lei_do_bem == "Sim":
        ganho_fiscal_anual = custo_folha_anual * 0.204
    else:
        ganho_fiscal_anual = 0

    if modelo == "Controladora + SPE":
        ganho_seguranca = 150000 * 0.80
    else:
        ganho_seguranca = 150000 * 0.20

    if investidor == "Sim":
        premio_gov = aporte * 0.15
    else:
        premio_gov = 0

    ganho_total = ganho_fiscal_anual + ganho_seguranca + premio_gov
    custo_operacional = custo_anual_Sa if modelo != "LTDA + Vesting" else 5000
    
    roi_global = ((ganho_total - custo_operacional) / custo_operacional * 100) if custo_operacional > 0 else 0

    st.subheader("Resultados da Simulação")
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Risco Jurídico", limitar(risco_juridico))
    m2.metric("Risco Trabalhista", limitar(risco_trabalhista))
    m3.metric("Risco Fiscal", limitar(risco_fiscal))
    m4.metric("Custo Estrutural", limitar(custo))
    m5.metric("Atratividade", limitar(atratividade))

    st.markdown("---")
    f1, f2, f3 = st.columns(3)
    f1.metric("Economia Fiscal (Ano)", f"R$ {ganho_fiscal_anual:,.2f}")
    f2.metric("Mitigação de Passivo", f"R$ {ganho_seguranca:,.2f}")
    f3.metric("ROI Global do Modelo", f"{roi_global:.1f}%")

    st.subheader("Análise Jurídica Automática")

    if modelo == "LTDA + Vesting" and risco_trabalhista >= 4:
        st.warning("⚠️ **Alerta:** Estrutura vulnerável a requalificação trabalhista. Recomenda-se vínculo formal ou SPE.")

    if investidor == "Sim" and atratividade <= 2:
        st.error("❌ **Alerta:** Estrutura pouco atrativa para investidores institucionais. Risco de exigência de 'Flip' ou reorganização cara.")

    if lei_do_bem == "Sim":
        st.success("✅ **Oportunidade:** Estrutura compatível com incentivos da Lei nº 11.196/2005 via Lucro Real.")
   
    st.subheader("Recomendação Final")
    if modelo == "Controladora + SPE":
        st.info("💡 **Modelo Recomendado:** Garante o isolamento do IP (Ativo Intelectual) e reduz o risco de confusão patrimonial com os desenvolvedores.")
    else:
        st.write("Considere a migração para SPE caso o número de desenvolvedores ultrapasse 5 ou o aporte supere R$ 500k.")

    st.markdown("""
    > **Nota Técnica:** Os critérios de **Risco Trabalhista** e **Tributário** consideram a jurisprudência atual do TST e CARF sobre contratos de Vesting e Stock Options.
    """)

# --- 3. CUSTOS ---
with aba_selecionada[3]:
    st.header("💰 Análise de Custos de Manutenção")
    
    st.markdown("""
    Compare os **custos operacionais e administrativos** dos diferentes modelos societários.
    """)
    
    # Tabs para diferentes análises de custo
    tab_manutencao, tab_abertura, tab_comparativo = st.tabs(["Manutenção Mensal", "Custo de Abertura", "Comparativo Anual"])
    
    with tab_manutencao:
        st.subheader("Custos de Manutenção por Tipo")
        st.info("Custos recorrentes **mensais** para manter a estrutura societária operacional.")
        
        # Filtro por modelo
        modelos_custo = st.multiselect(
            "Selecionar modelos para comparação:",
            ["LTDA (Limitada)", "S.A. (Anônima)"],
            default=["LTDA (Limitada)", "S.A. (Anônima)"],
            key="modelos_manutencao"
        )
        
        df_manut_filtrado = tabela_manutencao_display[["Item de Custo"] + modelos_custo]
        
        st.dataframe(
            df_manut_filtrado,
            use_container_width=True,
            column_config={
                "Item de Custo": st.column_config.TextColumn(width="large"),
                **{modelo: st.column_config.TextColumn(width="medium") for modelo in modelos_custo}
            },
            hide_index=True
        )
        
        # Resumo de custos estimados
        st.markdown("---")
        st.subheader("📊 Estimativa de Custo Mensal")
        
        custo_col1, custo_col2 = st.columns(2)
        
        with custo_col1:
            st.metric(
                "LTDA (Estimado)",
                "R$ 600 - R$ 2.700",
                "Manutenção baixa",
                delta_color="off"
            )
        
        with custo_col2:
            st.metric(
                "S.A. (Estimado)",
                "R$ 3.700 - R$ 11.700",
                "Manutenção alta",
                delta_color="off"
            )
    
    with tab_abertura:
        st.subheader("Custos de Abertura e Constituição")
        st.info("Custos **únicos** para estabelecer a estrutura societária.")
        
        st.dataframe(
            tabela_custos_base_display,
            use_container_width=True,
            column_config={
                "Modelo": st.column_config.TextColumn(width="large"),
                **{col: st.column_config.TextColumn(width="medium") 
                   for col in tabela_custos_base_display.columns if col != "Modelo"}
            },
            hide_index=True
        )
        
        # Detalhamento
        st.markdown("---")
        st.subheader("🔍 Detalhamento por Tipo de Custo")
        
        custo_detalhes = {
            "Abertura": {
                "LTDA + Vesting": "R$ 800 - R$ 1.500",
                "Controladora + SPE": "R$ 2.500 - R$ 4.000",
                "Nova Sociedade Única": "R$ 3.000 - R$ 5.000"
            },
            "Consultoria Legal": {
                "LTDA + Vesting": "R$ 1.000 - R$ 3.000",
                "Controladora + SPE": "R$ 5.000 - R$ 15.000",
                "Nova Sociedade Única": "R$ 3.000 - R$ 8.000"
            },
            "Contabilidade Inicial": {
                "LTDA + Vesting": "R$ 500 - R$ 1.000",
                "Controladora + SPE": "R$ 1.500 - R$ 3.000",
                "Nova Sociedade Única": "R$ 1.000 - R$ 2.000"
            }
        }
        
        for tipo_custo, valores in custo_detalhes.items():
            with st.expander(f"💵 {tipo_custo}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("LTDA + Vesting", valores["LTDA + Vesting"])
                with col2:
                    st.metric("Controladora + SPE", valores["Controladora + SPE"])
                with col3:
                    st.metric("Nova Sociedade Única", valores["Nova Sociedade Única"])
    
    with tab_comparativo:
        st.subheader("Projeção Anual de Custos")
        st.info("Estimativa de **custo total anual** para manutenção da estrutura.")
        
        # Slider para anos
        anos_projecao = st.slider("Projetar para quantos anos?", 1, 5, 3, key="anos_custos")
        
        # Dados de projeção
        projecao_data = {
            "Ano": list(range(1, anos_projecao + 1)),
            "LTDA + Vesting": [7_200 + (i * 500) for i in range(anos_projecao)],
            "Controladora + SPE": [18_000 + (i * 1_500) for i in range(anos_projecao)],
            "Nova Sociedade Única": [12_000 + (i * 1_000) for i in range(anos_projecao)]
        }
        
        df_projecao = pd.DataFrame(projecao_data)
        
        st.dataframe(
            df_projecao,
            use_container_width=True,
            column_config={
                "Ano": st.column_config.NumberColumn(format="Ano %d"),
                **{col: st.column_config.NumberColumn(format="R$ %,.0f") 
                   for col in df_projecao.columns if col != "Ano"}
            },
            hide_index=True
        )
        
        # Gráfico de comparação
        st.line_chart(
            df_projecao.set_index("Ano"),
            use_container_width=True,
            height=400
        )
        
        st.markdown("---")
        st.warning("""
        ⚠️ **Nota Importante:** Estas estimativas são baseadas em valores médios de mercado em 2025. 
        Consulte um contador para valores específicos da sua jurisdição.
        """)

# --- 4. RISCOS LEGAIS ---
with aba_selecionada[4]:
    st.header("⚖️ Matriz de Riscos Legais")
    
    st.markdown("""
    Análise dos **principais riscos jurídicos** associados a cada modelo societário.
    """)
    
    # Filtro por tipo de risco
    col_risk1, col_risk2 = st.columns(2)
    
    with col_risk1:
        tipos_risco = st.multiselect(
            "Filtrar por tipo de risco:",
            tabela_riscos_legais["Tipo de risco"].tolist(),
            default=tabela_riscos_legais["Tipo de risco"].tolist(),
            key="filtro_tipo_risco"
        )
    
    with col_risk2:
        st.write("")  # Espaço para alinhamento
    
    # Tabela filtrada
    tabela_risco_filtrada = tabela_riscos_display[
        tabela_riscos_display["Tipo de risco"].isin(tipos_risco)
    ]
    
    st.dataframe(
        tabela_risco_filtrada,
        use_container_width=True,
        column_config={
            "Tipo de risco": st.column_config.TextColumn(width="large"),
            **{col: st.column_config.TextColumn(width="medium") 
               for col in tabela_risco_filtrada.columns if col != "Tipo de risco"}
        },
        hide_index=True,
        height=300
    )
    
    st.markdown("---")
    st.subheader("📋 Análise Detalhada por Tipo de Risco")
    
    riscos_detalhes = {
        "Trabalhista": """
        **LTDA + Vesting:** Alto - Risco de requalificação de vesting como vínculo empregatício
        
        **Controladora + SPE:** Médio - Estrutura reduz confusão patrimonial
        
        **Nova Sociedade Única:** Alto - Múltiplos sócios aumentam conflitos trabalhistas
        """,
        
        "Tributário": """
        **LTDA + Vesting:** Médio/Alto - Requalificação de benefícios fiscais
        
        **Controladora + SPE:** Médio - Compatível com Lei do Bem via SPE
        
        **Nova Sociedade Única:** Médio - Restruturação pode gerar impostos sobre transmissão
        """,
        
        "Societário": """
        **LTDA + Vesting:** Médio - Entrada futura de sócios via vesting mal estruturado
        
        **Controladora + SPE:** Alto - Conflitos de governança entre holding e operacional
        
        **Nova Sociedade Única:** Alto - Conflitos diretos entre múltiplos sócios
        """,
        
        "Investidor": """
        **LTDA + Vesting:** Médio - Documentação fraca de direitos de minoritários
        
        **Controladora + SPE:** Médio - Transferência de IP pode ser questionada
        
        **Nova Sociedade Única:** Alto - Cap table pulverizado desestimula investimento
        """,
        
        "Operacional": """
        **LTDA + Vesting:** Baixo - Operação simplificada
        
        **Controladora + SPE:** Médio - Gestão de duas entidades aumenta complexidade
        
        **Nova Sociedade Única:** Alto - Múltiplas deliberações e aprovações necessárias
        """
    }
    
    for tipo_risco, descricao in riscos_detalhes.items():
        with st.expander(f"🔴 {tipo_risco}"):
            st.markdown(descricao)

# --- 5. TRIBUTAÇÃO / BENEFÍCIOS ---
with aba_selecionada[5]:
    st.header("🏛️ Tributação e Benefícios Fiscais")
    
    st.markdown("""
    Análise comparativa de **regimes tributários, incentivos fiscais e benefícios legais** 
    para startups e empresas de tecnologia.
    """)
    
    # Abas para diferentes aspectos tributários
    tab_tributacao, tab_lei_bem, tab_lc182, tab_inova = st.tabs([
        "Tributação Detalhada",
        "Lei do Bem (P&D)",
        "LC 182/21 (Marco Legal)",
        "Comparativo de Regimes"
    ])
    
    with tab_tributacao:
        st.subheader("Impactos Tributários por Modelo")
        st.info("""
        Análise de custos e benefícios **contábeis e tributários** de cada estrutura.
        """)
        
        # Filtro por aspecto
        aspectos_filtro = st.multiselect(
            "Selecionar aspectos:",
            tabela_tributacao_detalhada["Aspecto"].tolist(),
            default=tabela_tributacao_detalhada["Aspecto"].tolist()[:6],
            key="aspectos_tributacao"
        )
        
        df_tributacao_filtrada = tabela_tributacao_display[
            tabela_tributacao_display["Aspecto"].isin(aspectos_filtro)
        ]
        
        st.dataframe(
            df_tributacao_filtrada,
            use_container_width=True,
            column_config={
                "Aspecto": st.column_config.TextColumn(width="large"),
                **{col: st.column_config.TextColumn(width="medium") 
                   for col in df_tributacao_filtrada.columns if col != "Aspecto"}
            },
            hide_index=True
        )
    
    with tab_lei_bem:
        st.subheader("Lei do Bem (Lei nº 11.196/2005)")
        st.success("""
        Incentivo fiscal para **P&D em tecnologia**. Reduz IRPJ e CSLL via dedução de despesas.
        """)
        
        st.dataframe(
            tabela_lei_bem_display,
            use_container_width=True,
            column_config={
                "Aspecto": st.column_config.TextColumn(width="large"),
                "Impacto": st.column_config.TextColumn(width="large")
            },
            hide_index=True
        )
        
        st.markdown("---")
        st.warning("""
        ⚠️ **Pré-requisitos:**
        - Empresa em Lucro Real (obrigatório)
        - Pesquisa e Desenvolvimento de software genuíno
        - Documentação técnica e contábil segregada
        """)
    
    with tab_lc182:
        st.subheader("Marco Legal das Startups (LC 182/21)")
        st.info("""
        Regime jurídico especial para startups. **Compatível com LC 182/21** garante segurança legal para investidores.
        """)
        
        st.dataframe(
            tabela_lc182_display,
            use_container_width=True,
            column_config={
                "Aspecto": st.column_config.TextColumn(width="large"),
                "Impacto": st.column_config.TextColumn(width="large")
            },
            hide_index=True
        )
        
        st.markdown("---")
        st.success("""
        ✅ **Benefícios da LC 182/21:**
        - Contrato de investimento com investor-friendly terms
        - Proteção legal para opções e vesting
        - Facilita rodadas futuras
        """)
    
    with tab_inova:
        st.subheader("Comparativo de Regimes e Benefícios")
        
        st.dataframe(
            tabela_inova_display,
            use_container_width=True,
            column_config={
                "Critério": st.column_config.TextColumn(width="large"),
                **{col: st.column_config.TextColumn(width="medium") 
                   for col in tabela_inova_display.columns if col != "Critério"}
            },
            hide_index=True,
            height=400
        )
        
        st.markdown("---")
        st.subheader("🎯 Recomendação de Regime")
        
        rec_col1, rec_col2, rec_col3 = st.columns(3)
        
        with rec_col1:
            st.markdown("""
            **Inova Simples**
            
            Ideal para:
            - MVP / Validação
            - Sem faturamento
            - Baixo custo
            
            ❌ Incompatível com Lei do Bem
            """)
        
        with rec_col2:
            st.markdown("""
            **Lei do Bem**
            
            Ideal para:
            - Empresa estruturada
            - P&D continuado
            - Lucro Real
            
            ✅ Economia fiscal significativa
            """)
        
        with rec_col3:
            st.markdown("""
            **LC 182/21**
            
            Ideal para:
            - Todos os estágios
            - Com investidores
            - Segurança jurídica
            
            ✅ Compatível com ambos!
            """)

# --- 6. S.A. ---
with aba_selecionada[6]:
    st.header("📊 Sociedade Anônima (S.A.)")
    
    st.markdown("""
    Análise aprofundada da estrutura de **Sociedade Anônima**, recomendada para empresas 
    em **estágio avançado (Series A+)** ou preparadas para **IPO**.
    """)
    
    # Comparativo com LTDA e Controladora
    st.subheader("Comparativo: S.A. vs. Outros Modelos")
    
    st.dataframe(
        tabela_sa_display,
        use_container_width=True,
        column_config={
            "Critério": st.column_config.TextColumn(width="large"),
            **{col: st.column_config.TextColumn(width="medium") 
               for col in tabela_sa_display.columns if col != "Critério"}
        },
        hide_index=True,
        height=350
    )
    
    st.markdown("---")
    
    # Características da S.A.
    st.subheader("🔑 Características Principais")
    
    char_col1, char_col2 = st.columns(2)
    
    with char_col1:
        st.markdown("""
        **Vantagens**
        
        ✅ Proteção máxima de acionistas
        ✅ Liquidez de ações
        ✅ Acesso a mercado de capitais
        ✅ Estrutura profissional
        ✅ Ideal para IPO/M&A
        """)
    
    with char_col2:
        st.markdown("""
        **Desvantagens**
        
        ❌ Custo inicial muito alto (R$ 5k+)
        ❌ Complexidade jurídica extrema
        ❌ Custo mensal elevado (R$ 3-10k)
        ❌ Compliance rigoroso exigido
        ❌ Desnecessária para startups early stage
        """)
    
    st.markdown("---")
    st.subheader("📋 Quando Adotar S.A.?")
    
    st.info("""
    **Recomendações:**
    
    1. **Estágio avançado:** Series A ou superior
    2. **Receita confirmada:** Mínimo R$ 5-10M anuais
    3. **Investimento institucional:** Fundos VC/PE
    4. **Preparação para IPO:** Visão de mercado público
    5. **Liquidez de ações:** Necessidade de negociação secundária
    """)
    
    # Timeline de adoção
    st.subheader("📅 Timeline Recomendado")
    
    timeline_data = {
        "Estágio": ["MVP", "Early Stage", "Growth", "Series A+", "Pré-IPO"],
        "Modelo Ideal": [
            "Inova Simples / LTDA",
            "LTDA + Vesting",
            "Controladora + SPE",
            "S.A. (opcional)",
            "S.A. (obrigatório)"
        ],
        "Quando Mudar": [
            "0-6 meses",
            "6-18 meses",
            "18-36 meses",
            "36-60 meses",
            "60+ meses"
        ]
    }
    
    st.table(pd.DataFrame(timeline_data))

# --- 7. CONCLUSÃO JURÍDICA ---
def download_parecer():
    st.download_button(
        label="Gerar PDF do Parecer (Simulado)",
        data="Conteúdo do Parecer Gerado pelo Dashboard Societário",
        file_name="parecer_societario_tattoopop.txt",
        mime="text/plain"
    )

with aba_selecionada[7]:
    st.header("⚖️ Parecer Técnico de Implementação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        modelo_parecer = st.selectbox(
            "Escolha o modelo societário para parecer:",
            ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única", "S.A."],
            key="modelo_parecer"
        )

        investidor_parecer = st.selectbox(
            "Há expectativa de investimento externo?",
            ["Sim", "Não"],
            key="investidor_parecer"
        )
    
    if modelo_parecer == "LTDA + Vesting":
        st.info("### Estratégia: Escala Inicial e Validação")
        st.markdown("""
        **Diagnóstico:** Ideal para startups em estágio *Pre-Seed* ou com foco em redução de *burn rate*. 
        
        **Recomendações Práticas:**
        1. **Vesting Preciso:** Utilize cláusulas de *Good Leaver* e *Bad Leaver* para evitar litígios na saída de devs.
        2. **Propriedade Intelectual (IP):** Insira cláusulas de cessão total e irrevogável de direitos autorais em todos os contratos de prestação de serviços.
        3. **Risco Trabalhista:** Se o risco for **Alto**, considere formalizar o vínculo CLT para os 'Key Players' ou acelerar a migração para SPE.
        """)
        
    elif modelo_parecer == "Controladora + SPE":
        st.success("### Estratégia: Blindagem de Ativos e Governança Sênior")
        st.markdown("""
        **Diagnóstico:** Recomendado para startups com alto valor de IP ou que já possuem rodada de investimento confirmada.
        
        **Recomendações Práticas:**
        1. **Segregação:** Mantenha a operação na SPE e os ativos de software na Controladora (Holding).
        2. **Acordo de Sócios (SHA):** Essencial para regular a relação entre fundadores e desenvolvedores minoritários.
        3. **Compliance:** Exige contabilidade rigorosa para evitar a desconsideração da personalidade jurídica.
        """)
    
    else:
        st.warning("### Estratégia: Reorganização de Cap Table")
        st.markdown("""
        **Diagnóstico:** Modelo de transição complexa. Exige cuidado com a sucessão de obrigações da empresa antiga.
        
        **Recomendações Práticas:**
        1. **Due Diligence:** Realize auditoria tributária na empresa atual antes de transferir ativos para a nova.
        2. **Valuation:** Defina o preço das quotas de forma a não gerar tributação por ganho de capital indevido.
        """)

    st.markdown("---")
    
    st.subheader("📌 Roadmap Societário Sugerido")
    
    roadmap_data = {
        "Fase": ["Validação (MVP)", "Tração (Early Stage)", "Escala (Growth)"],
        "Modelo Ideal": ["LTDA + Vesting / Inova Simples", "Controladora + SPE (LTDA)", "S.A. (Lucro Real)"],
        "Foco Jurídico": ["Proteção de IP", "Atratividade para Anjos", "Governança e IPO Readiness"]
    }
    st.table(pd.DataFrame(roadmap_data))

    st.subheader("📋 Próximos Passos Imediatos")
    
    st.checkbox("Revisar contratos de Vesting atuais (Minuta Padrão)", value=True)
    st.checkbox("Verificar enquadramento no Lucro Real para Lei do Bem")
    
    if investidor_parecer == "Sim":
        st.checkbox("👉 **Ação Crítica:** Organizar Data Room jurídico para Due Diligence do investidor.")
    
    download_parecer()

# --- 8. PESQUISA SALARIAL DEV ---
with aba_selecionada[8]:
    st.header("💼 Pesquisa Salarial de Programadores 2025")
    
    st.markdown("""
    Análise completa de **salários, distribuição de talentos e custos de folha** 
    para ajudar na estruturação de equipes de desenvolvimento.
    """)
    
    # Abas para diferentes análises
    tab_salarios, tab_distribuicao, tab_custos, tab_simulador = st.tabs([
        "Salários por Nível",
        "Distribuição de Talentos",
        "Análise de Custos",
        "Simulador de Folha"
    ])
    
    with tab_salarios:
        st.subheader("📊 Média Salarial por Nível de Experiência")
        st.info("""
        Salários médios **mensais** para diferentes níveis de programadores em 2025.
        """)
        
        # Exibir tabela
        st.dataframe(
            salary_df,
            use_container_width=True,
            column_config={
                "Level": st.column_config.TextColumn(width="large"),
                "Average Salary (R$)": st.column_config.NumberColumn(format="R$ %.2f")
            },
            hide_index=True
        )
        
        st.markdown("---")
        st.subheader("📈 Gráfico Comparativo de Salários")
        
        # Criar gráfico de barras
        chart_data = salary_df.copy()
        chart_data.columns = ["Nível", "Salário Médio"]
        
        st.bar_chart(
            data=chart_data.set_index("Nível"),
            height=400,
            use_container_width=True
        )
        
        # Cards informativos
        st.markdown("---")
        st.subheader("🎯 Insights Salariais")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Estágio",
                f"R$ {salary_df[salary_df['Level'] == 'Estágio']['Average Salary (R$)'].values[0]:,.0f}",
                "Entrada"
            )
        
        with col2:
            st.metric(
                "Júnior",
                f"R$ {salary_df[salary_df['Level'] == 'Júnior']['Average Salary (R$)'].values[0]:,.0f}",
                "+138%"
            )
        
        with col3:
            st.metric(
                "Pleno",
                f"R$ {salary_df[salary_df['Level'] == 'Pleno']['Average Salary (R$)'].values[0]:,.0f}",
                "+88%"
            )
        
        with col4:
            st.metric(
                "Sênior",
                f"R$ {salary_df[salary_df['Level'] == 'Sênior']['Average Salary (R$)'].values[0]:,.0f}",
                "+99%"
            )
        
        with col5:
            st.metric(
                "Especialista",
                f"R$ {salary_df[salary_df['Level'] == 'Outro (Especialista, Tech Lead, Principal)']['Average Salary (R$)'].values[0]:,.0f}",
                "+23%"
            )
        
        st.markdown("""
        > **Nota:** Valores são médias ponderadas do mercado brasileiro de tecnologia em 2025.
        """)
    
    with tab_distribuicao:
        st.subheader("👥 Distribuição de Programadores por Nível")
        st.info("""
        Percentual de profissionais em cada nível no mercado brasileiro.
        """)
        
        # Tabela de distribuição
        st.dataframe(
            programmer_distribution_df,
            use_container_width=True,
            column_config={
                "Level": st.column_config.TextColumn(width="large"),
                "Percentage (%)": st.column_config.NumberColumn(format="%.2f%%")
            },
            hide_index=True
        )
        
        st.markdown("---")
        st.subheader("📊 Visualização: Distribuição de Talentos")
        
        # Gráfico de pizza
        dist_data = programmer_distribution_df.copy()
        dist_data.columns = ["Nível", "Percentual"]
        
        col_pie1, col_pie2 = st.columns(2)
        
        with col_pie1:
            # Gráfico de barras horizontal
            st.bar_chart(
                data=dist_data.set_index("Nível"),
                height=400,
                use_container_width=True
            )
        
        with col_pie2:
            st.markdown("""
            **Análise da Distribuição:**
            
            🟢 **Pleno (33.75%)** - Maior disponibilidade
            - Profissionais com experiência consolidada
            - Melhor custo-benefício
            
            🟠 **Sênior (24.92%)** - Segunda maior fatia
            - Liderança técnica
            - Arquitetura de sistemas
            
            🟡 **Júnior (24.47%)** - Praticamente equilibrado
            - Necessitam mentoria
            - Custo mais baixo
            
            🟣 **Especialista (11.76%)** - Mais escasso
            - Tech Leads, Architects
            - Premium em custo
            
            ⚪ **Estágio (5.1%)** - Menor disponibilidade
            - Recém-formados
            - Custo mínimo
            """)
        
        st.markdown("---")
        st.subheader("🌐 Distribuição por Área de Atuação")
        
        st.dataframe(
            area_distribution_df,
            use_container_width=True,
            column_config={
                "Area": st.column_config.TextColumn(width="large"),
                "Percentage (%)": st.column_config.NumberColumn(format="%.2f%%")
            },
            hide_index=True
        )
        
        # Gráfico de áreas
        area_data = area_distribution_df.copy()
        area_data.columns = ["Área", "Percentual"]
        
        st.bar_chart(
            data=area_data.set_index("Área"),
            height=400,
            use_container_width=True
        )
    
    with tab_custos:
        st.subheader("💰 Análise de Custos de Folha de Pagamento")
        st.info("""
        Projeção de **custos mensais e anuais** baseada em diferentes composições de equipe.
        """)
        
        # Seletor de composição de equipe
        st.markdown("**Configure sua equipe:**")
        
        col_team1, col_team2, col_team3 = st.columns(3)
        
        with col_team1:
            num_stagiarios = st.slider("Estagiários", 0, 10, 1, key="num_stagiarios")
            num_juniores = st.slider("Juniores", 0, 10, 2, key="num_juniores")
        
        with col_team2:
            num_plenos = st.slider("Plenos", 0, 10, 3, key="num_plenos")
            num_seniores = st.slider("Sêniores", 0, 10, 2, key="num_seniores")
        
        with col_team3:
            num_especialistas = st.slider("Especialistas", 0, 5, 1, key="num_especialistas")
        
        # Calcular custos
        custo_stagiarios = num_stagiarios * salary_df[salary_df['Level'] == 'Estágio']['Average Salary (R$)'].values[0]
        custo_juniores = num_juniores * salary_df[salary_df['Level'] == 'Júnior']['Average Salary (R$)'].values[0]
        custo_plenos = num_plenos * salary_df[salary_df['Level'] == 'Pleno']['Average Salary (R$)'].values[0]
        custo_seniores = num_seniores * salary_df[salary_df['Level'] == 'Sênior']['Average Salary (R$)'].values[0]
        custo_especialistas = num_especialistas * salary_df[salary_df['Level'] == 'Outro (Especialista, Tech Lead, Principal)']['Average Salary (R$)'].values[0]
        
        custo_mensal_bruto = custo_stagiarios + custo_juniores + custo_plenos + custo_seniores + custo_especialistas
        custo_mensal_encargos = custo_mensal_bruto * 0.58  # 58% de encargos sociais (13º, FGTS, etc)
        custo_mensal_total = custo_mensal_bruto + custo_mensal_encargos
        
        custo_anual = custo_mensal_total * 13.3  # 13 meses + provisão 13º
        
        st.markdown("---")
        st.subheader("📊 Resumo de Custos")
        
        cost_col1, cost_col2, cost_col3, cost_col4 = st.columns(4)
        
        with cost_col1:
            st.metric(
                "Folha Bruta (Mês)",
                f"R$ {custo_mensal_bruto:,.2f}",
                f"{num_stagiarios + num_juniores + num_plenos + num_seniores + num_especialistas} devs"
            )
        
        with cost_col2:
            st.metric(
                "Encargos Sociais",
                f"R$ {custo_mensal_encargos:,.2f}",
                "58% folha bruta"
            )
        
        with cost_col3:
            st.metric(
                "Custo Total Mensal",
                f"R$ {custo_mensal_total:,.2f}",
                f"R$ {custo_mensal_total/max(1, num_stagiarios + num_juniores + num_plenos + num_seniores + num_especialistas):,.0f}/dev"
            )
        
        with cost_col4:
            st.metric(
                "Custo Anual",
                f"R$ {custo_anual:,.2f}",
                "13.3 meses"
            )
        
        # Tabela detalhada
        st.markdown("---")
        st.subheader("🔍 Detalhamento por Nível")
        
        detalhamento_data = {
            "Nível": ["Estagiário", "Júnior", "Pleno", "Sênior", "Especialista", "TOTAL"],
            "Quantidade": [num_stagiarios, num_juniores, num_plenos, num_seniores, num_especialistas, 
                          num_stagiarios + num_juniores + num_plenos + num_seniores + num_especialistas],
            "Salário Unit.": [
                salary_df[salary_df['Level'] == 'Estágio']['Average Salary (R$)'].values[0],
                salary_df[salary_df['Level'] == 'Júnior']['Average Salary (R$)'].values[0],
                salary_df[salary_df['Level'] == 'Pleno']['Average Salary (R$)'].values[0],
                salary_df[salary_df['Level'] == 'Sênior']['Average Salary (R$)'].values[0],
                salary_df[salary_df['Level'] == 'Outro (Especialista, Tech Lead, Principal)']['Average Salary (R$)'].values[0],
                custo_mensal_bruto / max(1, num_stagiarios + num_juniores + num_plenos + num_seniores + num_especialistas)
            ],
            "Custo Mensal": [custo_stagiarios, custo_juniores, custo_plenos, custo_seniores, custo_especialistas, custo_mensal_bruto]
        }
        
        df_detalhamento = pd.DataFrame(detalhamento_data)
        
        st.dataframe(
            df_detalhamento,
            use_container_width=True,
            column_config={
                "Nível": st.column_config.TextColumn(width="large"),
                "Quantidade": st.column_config.NumberColumn(format="%d"),
                "Salário Unit.": st.column_config.NumberColumn(format="R$ %.2f"),
                "Custo Mensal": st.column_config.NumberColumn(format="R$ %.2f")
            },
            hide_index=True
        )
    
    with tab_simulador:
        st.subheader("🎯 Simulador Interativo de Folha")
        st.info("""
        Projete o custo da sua equipe e veja o impacto no ROI societário.
        """)
        
        # Inputs
        sim_col1, sim_col2 = st.columns(2)
        
        with sim_col1:
            total_devs_sim = st.slider(
                "Total de Desenvolvedores",
                min_value=1,
                max_value=20,
                value=5,
                key="total_devs_sim"
            )
            
            percentual_pleno = st.slider(
                "% de Plenos",
                min_value=0,
                max_value=100,
                value=40,
                key="pct_pleno"
            )
            
            percentual_senior = st.slider(
                "% de Sêniores",
                min_value=0,
                max_value=100,
                value=30,
                key="pct_senior"
            )
        
        with sim_col2:
            modelo_sim = st.selectbox(
                "Modelo Societário",
                ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única"],
                key="modelo_sim"
            )
            
            anos_projecao_folha = st.slider(
                "Anos de Projeção",
                min_value=1,
                max_value=5,
                value=3,
                key="anos_proj_folha"
            )
            
            aumento_anual = st.slider(
                "Aumento Anual (%)",
                min_value=0,
                max_value=15,
                value=5,
                key="aumento_anual"
            )
        
        # Distribuição automática
        percentual_junior = 100 - percentual_pleno - percentual_senior
        if percentual_junior < 0:
            st.error("⚠️ Ajuste os percentuais para somar 100%")
        else:
            num_plenos_sim = int(total_devs_sim * percentual_pleno / 100)
            num_seniores_sim = int(total_devs_sim * percentual_senior / 100)
            num_juniores_sim = total_devs_sim - num_plenos_sim - num_seniores_sim
            
            # Projeção
            projecao_folha = {
                "Ano": list(range(1, anos_projecao_folha + 1)),
                "Folha Bruta": [],
                "Com Encargos": [],
                "Custo Anualizado": []
            }
            
            salario_base = (
                (num_juniores_sim * salary_df[salary_df['Level'] == 'Júnior']['Average Salary (R$)'].values[0]) +
                (num_plenos_sim * salary_df[salary_df['Level'] == 'Pleno']['Average Salary (R$)'].values[0]) +
                (num_seniores_sim * salary_df[salary_df['Level'] == 'Sênior']['Average Salary (R$)'].values[0])
            )
            
            for ano in range(1, anos_projecao_folha + 1):
                multiplicador = (1 + aumento_anual/100) ** (ano - 1)
                folha_bruta = salario_base * multiplicador
                com_encargos = folha_bruta * 1.58
                anualizado = com_encargos * 13.3
                
                projecao_folha["Folha Bruta"].append(folha_bruta)
                projecao_folha["Com Encargos"].append(com_encargos)
                projecao_folha["Custo Anualizado"].append(anualizado)
            
            df_projecao_folha = pd.DataFrame(projecao_folha)
            
            st.markdown("---")
            st.subheader("📈 Projeção de Custos")
            
            st.dataframe(
                df_projecao_folha,
                use_container_width=True,
                column_config={
                    "Ano": st.column_config.NumberColumn(format="Ano %d"),
                    **{col: st.column_config.NumberColumn(format="R$ %.0f") 
                       for col in df_projecao_folha.columns if col != "Ano"}
                },
                hide_index=True
            )
            
            st.markdown("---")
            st.subheader("📊 Gráfico de Evolução")
            
            st.line_chart(
                df_projecao_folha.set_index("Ano"),
                use_container_width=True,
                height=400
            )
            
            st.markdown("---")
            st.subheader("💡 Recomendações")
            
            custo_final_anual = df_projecao_folha["Custo Anualizado"].iloc[-1]
            
            if modelo_sim == "LTDA + Vesting":
                receita_recomendada = custo_final_anual * 3
                st.info(f"""
                **Para LTDA + Vesting:** Recomenda-se faturamento mínimo de **R$ {receita_recomendada:,.0f}/ano** 
                para manter a operação sustentável com folha de R$ {custo_final_anual:,.0f}.
                """)
            
            elif modelo_sim == "Controladora + SPE":
                receita_recomendada = custo_final_anual * 2.5
                st.success(f"""
                **Para Controladora + SPE:** Com estrutura profissional, faturamento de **R$ {receita_recomendada:,.0f}/ano** 
                é adequado para esta folha de R$ {custo_final_anual:,.0f}.
                """)
            
            else:
                receita_recomendada = custo_final_anual * 4
                st.warning(f"""
                **Para Nova Sociedade Única:** Exige faturamento robusto de **R$ {receita_recomendada:,.0f}/ano** 
                devido à complexidade. Folha estimada: R$ {custo_final_anual:,.0f}.
                """)
    
    st.markdown("---")
    st.subheader("📌 Notas Importantes")
    
    st.markdown(f"""
    **Salário Médio Geral Ponderado (2025):** R$ {overall_average_salary:,.2f}
    
    - Dados baseados em pesquisa de mercado brasileiro
    - Valores incluem benefícios (vale refeição, vale transporte, convênio)
    - Encargos sociais estimados em 58% (FGTS, INSS, 13º, provisões)
    - Projeções consideram inflação/reajuste anual
    - Para salários específicos, consulte especialista em RH/Folha
    """)