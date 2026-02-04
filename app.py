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



def parse_and_fill_salaries(salaries_str, num_devs_for_level, average_salary):
    parsed_salaries = []
    if salaries_str:
        raw_salaries = salaries_str.replace(' ', '').replace('.', '').replace(',', '.').split(',')
        for s in raw_salaries:
            try:
                parsed_salaries.append(float(s))
            except ValueError:
                # Ignore non-numeric values
                continue

    # Fill with average salary if not enough custom salaries
    while len(parsed_salaries) < num_devs_for_level:
        parsed_salaries.append(average_salary)

    # Trim if too many custom salaries
    return parsed_salaries[:num_devs_for_level]

# ===============================
# DADOS BASE (TODOS OS ORIGINAIS + NOVOS)
# ===============================

# FORMA CORRETA: Aplica a função diretamente no DataFrame
st.dataframe(
    tabela_modelos.applymap(color_ball), 
    use_container_width=True,
    height=500
)

df_modelos = pd.DataFrame({
    "Modelo": ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única"],
    "Custo Inicial": ["Baixo", "Alto", "Alto"],
    "Risco Jurídico": ["Médio", "Alto", "Alto"],
    "Atratividade Investidor": ["Médio", "Alto", "Baixo"],
    "Prazo (dias)": ["Curto (30–60)", "Médio (60–120)", "Longo (90–150)"],
    "Receita Mínima Recomendada": ["0", "R$ 50.000", "R$ 100.000"]
})

tabela_custos_base = pd.DataFrame({
    "Modelo": ["LTDA + Vesting", "Controladora + SPE", "Nova Sociedade Única"],
    "Custo abertura": ["Baixo", "Alto", "Muito Alto"],
    "Custo manutenção mensal": ["Baixo", "Alto", "Médio/Alto"],
    "Custo legal/consultivo": ["Baixo", "Alto", "Muito Alto"],
    "Custo contábil": ["Baixo", "Médio/Alto", "Médio/Alto"]
})

# NOVA: Tabela detalhada de custos reais solicitada
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
# DADOS DA PESQUISA SALARIAL (NOVOS)
salary_df = pd.DataFrame([('Estágio', 1743.4), ('Júnior', 4154.21), ('Pleno', 7840.74), ('Sênior', 15635.35), ('Outro (Especialista, Tech Lead, Principal)', 19290.08)], columns=['Level', 'Average Salary (R$)'])
programmer_distribution_df = pd.DataFrame([('Pleno', 33.75), ('Sênior', 24.92), ('Júnior', 24.47), ('Outro (Especialista, Tech Lead, Principal)', 11.76), ('Estágio', 5.1)], columns=['Level', 'Percentage (%)'])
area_distribution_df = pd.DataFrame([('Full-Stack', 37.42), ('Back-End', 30.06), ('Front-End', 9.06), ('Dados (BI, Data Science)', 5.45), ('Mobile', 5.4)], columns=['Area', 'Percentage (%)'])

# Calculate overall average salary
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

# --- 0. DASHBOARD GERAL ---
with aba_selecionada[0]:
    st.subheader("Comparação Geral dos Modelos Societários")
    st.dataframe(df_modelos.applymap(color_ball), use_container_width=True)

## --- 1. DEFINIÇÕES GERAIS ---
with aba_selecionada[1]:
    st.header("📖 Sumário Executivo e Teses Jurídicas")
    
    # Seção de Visão de Negócio com Cards
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

    st.markdown("---")
    
    # Infográfico de Fluxo de Operação (Conceitual)
    st.subheader("🔄 Fluxo de Valor e Estrutura")
    
    
    st.markdown("---")
    
    # Tabela Comparativa com Explicação
    st.subheader("📊 Matriz Comparativa de Modelos")
    st.info("""
    A tabela abaixo cruza **18 critérios técnicos** para determinar qual estrutura 
    suporta melhor o crescimento da TattooPop sem gerar passivos ocultos.
    """)
    
    # Exibição da Tabela Detalhada
    st.dataframe(
        tabela_modelos.style.applymap(color_ball), 
        use_container_width=True,
        height=500 # Aumentado para evitar scroll excessivo em tabelas longas
    )
    
    st.markdown("""
    > **Nota Técnica:** Os critérios de **Risco Trabalhista** e **Tributário** > consideram a jurisprudência atual do TST e CARF sobre contratos de Vesting e Stock Options.
    """)

# --- 2. SIMULAÇÃO & ROI INTERATIVO ---
with aba_selecionada[2]:
    st.subheader("Simulador Interativo de ROI Societário")

    st.markdown("""
    Ajuste os parâmetros abaixo para simular **riscos, custos e atratividade** dos modelos societários.
    """)

    # ===============================
    # Entradas interativas
    # ===============================
    col1, col2 = st.columns(2)

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


    # ===============================
    # Cálculo dinâmico de métricas
    # ===============================
    # Valores iniciais
    risco_juridico = 2
    risco_trabalhista = 2
    risco_fiscal = 2
    atratividade = 3
    custo = 2

    # Ajustes baseados nas entradas
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

    # Limites entre 1 e 5
    def limitar(valor):
        return max(1, min(valor, 5))

    risco_juridico = limitar(risco_juridico)
    risco_trabalhista = limitar(risco_trabalhista)
    risco_fiscal = limitar(risco_fiscal)
    atratividade = limitar(atratividade)
    custo = limitar(custo)

    # =============================================================
 # CÁLCULO DE ROI AVANÇADO (FISCAL + JURÍDICO + GOVERNANÇA)
    # =============================================================
    
    # 1. Ganho Fiscal (Lei do Bem) - Aprox. 20.4% da folha anual de P&D
    custo_folha_anual = (num_devs * overall_average_salary) * 13.3
    if lei_do_bem == "Sim":
        ganho_fiscal_anual = custo_folha_anual * 0.204
    else:
        ganho_fiscal_anual = 0

    # 2. Ganho de Mitigação de Risco (Processos evitados)
    # Estimativa de evitar um passivo trabalhista médio de R$ 150k
    if modelo == "Controladora + SPE":
        ganho_seguranca = 150000 * 0.80  # 80% de redução de risco
    else:
        ganho_seguranca = 150000 * 0.20  # LTDA protege pouco

    # 3. Prêmio de Governança (Equity)
    if investidor == "Sim":
        premio_gov = aporte * 0.15
    else:
        premio_gov = 0

    # ROI Global
    ganho_total = ganho_fiscal_anual + ganho_seguranca + premio_gov
    # Define custo de manutenção com base na seleção (LTDA é mais barata que SPE/S.A.)
    custo_operacional = custo_anual_Sa if modelo != "LTDA + Vesting" else 5000
    
    divisor = custo_operacional if custo_operacional > 0 else 1
    roi_global = ((ganho_total - custo_operacional) / divisor) * 100

    # ===============================
    # Exibição dos resultados
    # ===============================
    st.subheader("Resultados da Simulação")
    
    # Métricas de Risco (1 a 5)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Risco Jurídico", limitar(risco_juridico))
    m2.metric("Risco Trabalhista", limitar(risco_trabalhista))
    m3.metric("Risco Fiscal", limitar(risco_fiscal))
    m4.metric("Custo Estrutural", limitar(custo))
    m5.metric("Atratividade", limitar(atratividade))

    # Métricas Financeiras
    st.markdown("---")
    f1, f2, f3 = st.columns(3)
    f1.metric("Economia Fiscal (Ano)", f"R$ {ganho_fiscal_anual:,.2f}")
    f2.metric("Mitigação de Passivo", f"R$ {ganho_seguranca:,.2f}")
    f3.metric("ROI Global do Modelo", f"{roi_global:.1f}%")

    # ===============================
    # Interpretação jurídica automática
    # ===============================
    st.subheader("Análise Jurídica Automática")

    if modelo == "LTDA + Vesting" and risco_trabalhista >= 4:
        st.warning("⚠️ **Alerta:** Estrutura vulnerável a requalificação trabalhista. Recomenda-se vínculo formal ou SPE.")

    if investidor == "Sim" and atratividade <= 2:
        st.error("❌ **Alerta:** Estrutura pouco atrativa para investidores institucionais. Risco de exigência de 'Flip' ou reorganização cara.")

    if lei_do_bem == "Sim":
        st.success("✅ **Oportunidade:** Estrutura compatível com incentivos da Lei nº 11.196/2005 via Lucro Real.")
   
    # ===============================
    # Recomendação final
    # ===============================
    st.subheader("Recomendação Final")
    if modelo == "Controladora + SPE":
        st.info("💡 **Modelo Recomendado:** Garante o isolamento do IP (Ativo Intelectual) e reduz o risco de confusão patrimonial com os desenvolvedores.")
    else:
        st.write("Considere a migração para SPE caso o número de desenvolvedores ultrapasse 5 ou o aporte supere R$ 500k.")

# --- 3. CUSTOS ---
with aba_selecionada[3]:
    st.subheader("Análise de Custos de Manutenção")
    st.dataframe(tabela_manutencao_financeira.applymap(color_ball), use_container_width=True)
    st.dataframe(tabela_custos_base.applymap(color_ball), use_container_width=True)

# --- 4. RISCOS LEGAIS ---
with aba_selecionada[4]:
    st.subheader("Matriz de Riscos")
    st.dataframe(tabela_riscos_legais.applymap(color_ball), use_container_width=True)

# --- 5. TRIBUTAÇÃO / BENEFÍCIOS ---
with aba_selecionada[5]:
    
    st.markdown("### Tributação Detalhada")
    st.dataframe(tabela_tributacao_detalhada.applymap(color_ball), use_container_width=True)

    st.subheader("Benefícios Legais e Fiscais")
    st.markdown("### Lei do Bem (P&D)")
    st.dataframe(tabela_lei_bem.applymap(color_ball), use_container_width=True)
    st.markdown("### Marco Legal das Startups (LC 182/21)")
    st.dataframe(tabela_lc182.applymap(color_ball), use_container_width=True)
    st.markdown("### Comparativo de Regimes")
    st.dataframe(tabela_inova.applymap(color_ball), use_container_width=True)

# --- 6. S.A. ---
with aba_selecionada[6]:
    st.subheader("Aprofundamento: Sociedade Anônima")
    st.dataframe(tabela_sa.applymap(color_ball), use_container_width=True)

# --- 7. CONCLUSÃO JURÍDICA ---
# --- 7. CONCLUSÃO JURÍDICA (Parecer Consultivo Dinâmico) ---
with aba_selecionada[7]:
    st.header("⚖️ Parecer Técnico de Implementação")
    
    # Lógica de Recomendação Baseada no Simulador
    if modelo == "LTDA + Vesting":
        st.info("### Estratégia: Escala Inicial e Validação")
        st.markdown("""
        **Diagnóstico:** Ideal para startups em estágio *Pre-Seed* ou com foco em redução de *burn rate*. 
        
        **Recomendações Práticas:**
        1. **Vesting Preciso:** Utilize cláusulas de *Good Leaver* e *Bad Leaver* para evitar litígios na saída de devs.
        2. **Propriedade Intelectual (IP):** Insira cláusulas de cessão total e irrevogável de direitos autorais em todos os contratos de prestação de serviços.
        3. **Risco Trabalhista:** Se o risco for **Alto**, considere formalizar o vínculo CLT para os 'Key Players' ou acelerar a migração para SPE.
        """)
        
    elif modelo == "Controladora + SPE":
        st.success("### Estratégia: Blindagem de Ativos e Governança Sênior")
        st.markdown("""
        **Diagnóstico:** Recomendado para startups com alto valor de IP ou que já possuem rodada de investimento confirmada.
        
        **Recomendações Práticas:**
        1. **Segregação:** Mantenha a operação na SPE e os ativos de software na Controladora (Holding).
        2. **Acordo de Sócios (SHA):** Essencial para regular a relação entre fundadores e desenvolvedores minoritários.
        3. **Compliance:** Exige contabilidade rigorosa para evitar a desconsideração da personalidade jurídica.
        """)
    
    else: # Nova Sociedade Única
        st.warning("### Estratégia: Reorganização de Cap Table")
        st.markdown("""
        **Diagnóstico:** Modelo de transição complexa. Exige cuidado com a sucessão de obrigações da empresa antiga.
        
        **Recomendações Práticas:**
        1. **Due Diligence:** Realize auditoria tributária na empresa atual antes de transferir ativos para a nova.
        2. **Valuation:** Defina o preço das quotas de forma a não gerar tributação por ganho de capital indevido.
        """)

    st.markdown("---")
    
    # Timeline de Evolução Societária
    st.subheader("📌 Roadmap Societário Sugerido")
    
    roadmap_data = {
        "Fase": ["Validação (MVP)", "Tração (Early Stage)", "Escala (Growth)"],
        "Modelo Ideal": ["LTDA + Vesting / Inova Simples", "Controladora + SPE (LTDA)", "S.A. (Lucro Real)"],
        "Foco Jurídico": ["Proteção de IP", "Atratividade para Anjos", "Governança e IPO Readiness"]
    }
    st.table(pd.DataFrame(roadmap_data))

    

    # Checklist de Próximos Passos
    st.subheader("📋 Próximos Passos Imediatos")
    
    st.checkbox("Revisar contratos de Vesting atuais (Minuta Padrão)", value=True)
    st.checkbox("Verificar enquadramento no Lucro Real para Lei do Bem")
    
    if investidor == "Sim":
        st.checkbox("👉 **Ação Crítica:** Organizar Data Room jurídico para Due Diligence do investidor.")
    
    # Botão de Exportação (Simulado)
    st.download_button(
        label="Gerar PDF do Parecer (Simulado)",
        data="Conteúdo do Parecer Gerado pelo Dashboard Societário",
        file_name="parecer_societario_tattoopop.txt",
        mime="text/plain"
    )

# --- 8. PESQUISA SALARIAL DEV ---
with aba_selecionada[8]:
    st.subheader("Pesquisa Salarial de Programadores 2025")
    st.markdown("### Média Salarial por Nível")
    st.dataframe(salary_df, use_container_width=True)

    st.markdown("### Distribuição de Programadores por Nível")
    st.dataframe(programmer_distribution_df, use_container_width=True)

    st.markdown("### Distribuição por Área de Atuação")
    st.dataframe(area_distribution_df, use_container_width=True)

    st.markdown(f"**Salário Médio Geral Ponderado:** R$ {overall_average_salary:,.2f}")


