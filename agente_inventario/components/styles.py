import streamlit as st


def aplicar_estilos():
    st.markdown(
        """
        <style>
    
        /* Fondo general */
        .stApp {
            background-color: #f5f7fb;
        }
    
        /* Ocultar menú y footer */
        #MainMenu {
            visibility: hidden;
        }

        /* Mantener el control del sidebar y camuflar la cabecera */
        header[data-testid="stHeader"] {
            background: #07111f;
        }

        /* Ocultar solo Deploy, sin quitar el botón de expandir/contraer */
        [data-testid="stDeployButton"] {
            display: none;
        }
    
        footer {
            visibility: hidden;
        }
    
        /* Contenedor principal */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }
    
        /* Título principal */
        .main-title {
            font-size: 2.4rem;
            font-weight: 700;
            color: #172033;
            margin-bottom: 0.2rem;
        }
    
        .subtitle {
            color: #667085;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }
    
        /* Tarjetas */
        .info-card {
            background: white;
            border: 1px solid #e4e7ec;
            border-radius: 14px;
            padding: 20px;
            min-height: 145px;
            box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);
        }
    
        .card-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #667085;
            margin-bottom: 8px;
        }
    
        .card-value {
            font-size: 1.35rem;
            font-weight: 700;
            color: #172033;
        }
    
        .card-description {
            font-size: 0.85rem;
            color: #667085;
            margin-top: 6px;
            line-height: 1.4;
        }
    
        /* Agentes */
        .agent-card {
            background: white;
            border: 1px solid #e4e7ec;
            border-radius: 14px;
            padding: 18px;
            height: 100%;
            box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);
        }
    
        .agent-number {
            font-size: 0.8rem;
            font-weight: 700;
            color: #667085;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
    
        .agent-name {
            font-size: 1.2rem;
            font-weight: 700;
            color: #172033;
            margin: 7px 0;
        }
    
        .agent-description {
            font-size: 0.9rem;
            color: #667085;
            line-height: 1.5;
        }
    
        /* Separador */
        .section-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #172033;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
    
        /* Estado */
        .status-connected {
            background-color: #ecfdf3;
            color: #027a48;
            border: 1px solid #abefc6;
            border-radius: 10px;
            padding: 12px 15px;
            font-weight: 600;
        }
    
        .status-disconnected {
            background-color: #fef3f2;
            color: #b42318;
            border: 1px solid #fecdca;
            border-radius: 10px;
            padding: 12px 15px;
            font-weight: 600;
        }
    
        /* Resultado */
        .result-header {
            background: white;
            border: 1px solid #e4e7ec;
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 12px;
        }
    
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #172033;
        }
    
        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }
    
        /* ============================================================
        SMARTSTOCK - SIDEBAR
        ============================================================ */
    
        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 4px 18px 4px;
        }
    
        .brand-icon {
            width: 38px;
            height: 38px;
            border-radius: 12px;
            background: linear-gradient(135deg, #0ea5e9, #2563eb);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 13px;
            font-weight: 800;
        }
    
        .brand-name {
            font-size: 1.05rem;
            font-weight: 700;
            color: #f8fafc;
        }
    
        .brand-subtitle {
            font-size: 0.72rem;
            color: #94a3b8;
            margin-top: 2px;
        }
    
        .sidebar-separator {
            height: 1px;
            background: #1e293b;
            margin: 4px 0 20px 0;
        }
    
        .sidebar-section-title {
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 10px;
        }
    
        .sidebar-spacer {
            height: 25vh;
        }
    
        .erp-status-card {
            background: #101b2b;
            border: 1px solid #1e334d;
            border-radius: 14px;
            padding: 14px;
            margin-top: 15px;
        }
    
        .erp-status-title {
            color: #e2e8f0;
            font-size: 0.82rem;
            font-weight: 600;
        }
    
        .erp-status-text {
            color: #64748b;
            font-size: 0.72rem;
            margin-top: 7px;
            line-height: 1.4;
        }
    
        .status-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #22c55e;
            margin-right: 7px;
        }
    
        .sidebar-footer-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 18px;
            padding: 5px 3px;
        }
    
        .mini-logo {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #0ea5e9;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 11px;
            font-weight: 800;
        }
    
        .mini-brand-name {
            color: #e2e8f0;
            font-size: 0.78rem;
            font-weight: 600;
        }
    
        .mini-brand-text {
            color: #64748b;
            font-size: 0.68rem;
        }
    
        
        /* ============================================================
        SMARTSTOCK DASHBOARD
        ============================================================ */
    
        .stApp {
            background: #07111f !important;
            color: #e2e8f0;
        }
    
        .main .block-container {
            max-width: 1500px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }
    
        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
    
        .dashboard-title {
            color: #f8fafc;
            font-size: 2rem;
            font-weight: 700;
        }
    
        .dashboard-subtitle {
            color: #64748b;
            font-size: 0.9rem;
            margin-top: 4px;
        }
    
        .dashboard-status {
            background: #0d1b2b;
            border: 1px solid #1e334d;
            border-radius: 20px;
            padding: 9px 15px;
            color: #94a3b8;
            font-size: 0.8rem;
        }
    
        .kpi-grid {
            margin-bottom: 22px;
        }
    
        .kpi-card {
            min-height: 125px;
            border-radius: 16px;
            padding: 18px;
            border: 1px solid #1e334d;
            background: #0d1928;
        }
    
        .kpi-card.blue {
            border-top: 2px solid #0ea5e9;
        }
    
        .kpi-card.red {
            border-top: 2px solid #ef4444;
        }
    
        .kpi-card.orange {
            border-top: 2px solid #f59e0b;
        }
    
        .kpi-card.cyan {
            border-top: 2px solid #38bdf8;
        }
    
        .kpi-card.green {
            border-top: 2px solid #22c55e;
        }
    
        .kpi-label {
            color: #94a3b8;
            font-size: 0.75rem;
            font-weight: 600;
        }
    
        .kpi-value {
            color: #f8fafc;
            font-size: 2rem;
            font-weight: 700;
            margin-top: 8px;
        }
    
        .kpi-description {
            color: #64748b;
            font-size: 0.7rem;
            margin-top: 3px;
        }
    
        .dashboard-section-title {
            color: #f8fafc;
            font-size: 1.15rem;
            font-weight: 700;
            margin: 25px 0 12px 0;
        }
    
        .dashboard-panel {
            background: #0d1928;
            border: 1px solid #1e334d;
            border-radius: 16px;
            padding: 18px;
            min-height: 315px;
            margin-bottom: 18px;
        }
    
        .panel-title {
            color: #e2e8f0;
            font-size: 0.95rem;
            font-weight: 700;
        }
    
        .panel-subtitle {
            color: #64748b;
            font-size: 0.72rem;
            margin-top: 4px;
            margin-bottom: 15px;
        }
    
        /* ============================================================
        GRÁFICOS DEL DASHBOARD
        ============================================================ */
    
        .inventory-panel,
        .sales-panel {
            min-height: 340px;
        }
    
        .inventory-content {
            min-height: 265px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 55px;
        }
    
        .inventory-donut {
            width: 185px;
            height: 185px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
    
        .donut-center {
            width: 112px;
            height: 112px;
            border-radius: 50%;
            background: #0d1928;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
    
        .donut-number {
            color: #f8fafc;
            font-size: 1.8rem;
            font-weight: 700;
        }
    
        .donut-label {
            color: #64748b;
            font-size: 0.7rem;
            margin-top: 2px;
        }
    
        .inventory-legend {
            display: flex;
            flex-direction: column;
            gap: 13px;
            min-width: 130px;
        }
    
        .legend-item {
            display: grid;
            grid-template-columns: 10px 1fr auto;
            align-items: center;
            gap: 8px;
            color: #94a3b8;
            font-size: 0.75rem;
        }
    
        .legend-item strong {
            color: #e2e8f0;
            font-weight: 700;
        }
    
        .legend-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
        }
    
        .legend-dot.green {
            background: #22c55e;
        }
    
        .legend-dot.yellow {
            background: #f59e0b;
        }
    
        .legend-dot.orange {
            background: #f97316;
        }
    
        .legend-dot.red {
            background: #ef4444;
        }
    
        .legend-dot.gray {
            background: #64748b;
        }
    
    
        /* ------------------------------------------------------------
        BARRAS DE VENTAS
        ------------------------------------------------------------ */
    
        .sales-chart {
            margin-top: 15px;
            max-height: 255px;
            overflow-y: auto;
            padding-right: 5px;
        }
    
        .sales-row {
            margin-bottom: 13px;
        }
    
        .sales-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }
    
        .sales-name {
            color: #cbd5e1;
            font-size: 0.7rem;
            max-width: 75%;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    
        .sales-value {
            color: #2dd4bf;
            font-size: 0.7rem;
            font-weight: 700;
        }
    
        .sales-bar-background {
            width: 100%;
            height: 7px;
            background: #172a40;
            border-radius: 10px;
            overflow: hidden;
        }
    
        .sales-bar {
            height: 100%;
            border-radius: 10px;
            background: linear-gradient(
                90deg,
                #0ea5e9,
                #38bdf8
            );
        }
    
        /* ============================================================
        PANELES INFERIORES
        ============================================================ */
    
        .bottom-panel {
            min-height: 330px;
        }
    
        .panel-header-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }
    
        .panel-link {
            color: #38bdf8;
            font-size: 0.7rem;
            font-weight: 600;
            cursor: pointer;
        }
    
        .critical-table-header {
            display: grid;
            grid-template-columns: 1fr 90px 100px;
            align-items: center;
            padding: 8px 12px;
            color: #475569;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            border-bottom: 1px solid #1e334d;
            margin-bottom: 8px;
        }
    
        .critical-table-header span:nth-child(2),
        .critical-table-header span:nth-child(3) {
            text-align: center;
        }
    
        .empty-state {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 180px;
            color: #64748b;
            font-size: 0.8rem;
        }
    
        /* ============================================================
        PRODUCTOS CRÍTICOS
        ============================================================ */
    
        .product-row {
            display: grid;
            grid-template-columns: 1fr 90px 100px;
            align-items: center;
            gap: 10px;
    
            background: #101d2d;
            border: 1px solid #1a3048;
            border-radius: 10px;
    
            padding: 11px 12px;
            margin-bottom: 7px;
        }
    
        .product-name {
            color: #dbeafe;
            font-size: 0.76rem;
            font-weight: 600;
        }
    
        .product-stock {
            color: #64748b;
            font-size: 0.7rem;
            text-align: center;
        }
    
        .product-stock strong {
            color: #e2e8f0;
            font-weight: 700;
        }
    
        .risk-badge {
            justify-self: center;
    
            border-radius: 20px;
            padding: 5px 10px;
    
            font-size: 0.62rem;
            font-weight: 700;
        }
    
        .risk-critical {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.2);
        }
    
        .risk-high {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.2);
        }
    
        .risk-medium {
            background: rgba(14, 165, 233, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(14, 165, 233, 0.2);
        }
    
    
        /* ============================================================
        PRODUCTOS CON MAYOR DEMANDA
        ============================================================ */
    
        .demand-row {
            display: flex;
            align-items: center;
            gap: 10px;
    
            background: #101d2d;
            border: 1px solid #1a3048;
            border-radius: 10px;
    
            padding: 11px 12px;
            margin-bottom: 7px;
        }
    
        .demand-position {
            width: 25px;
            height: 25px;
    
            border-radius: 50%;
    
            background: #172a40;
            color: #7dd3fc;
    
            display: flex;
            align-items: center;
            justify-content: center;
    
            font-size: 0.65rem;
            font-weight: 700;
    
            flex-shrink: 0;
        }
    
        .demand-product {
            flex: 1;
    
            color: #dbeafe;
            font-size: 0.76rem;
            font-weight: 600;
        }
    
        .demand-value {
            color: #2dd4bf;
            font-size: 0.72rem;
            font-weight: 700;
            white-space: nowrap;
        }
    
        .demand-value span {
            color: #64748b;
            font-weight: 400;
        }
    
    
        /* ============================================================
        ESTADO ERP
        ============================================================ */
    
        .dashboard-footer-status {
            display: flex;
            align-items: center;
            gap: 9px;
    
            background: #0d1928;
            border: 1px solid #1e334d;
            border-radius: 12px;
    
            padding: 12px 16px;
    
            color: #64748b;
            font-size: 0.75rem;
    
            margin-top: 8px;
        }
    
        .dashboard-footer-status strong {
            color: #22c55e;
        }
    
        .dashboard-footer-status.error strong {
            color: #f87171;
        }
    
        .status-dot-error {
            width: 7px;
            height: 7px;
    
            border-radius: 50%;
    
            background: #ef4444;
        }
    
        .smartstock-footer {
            text-align: center;
    
            color: #475569;
            font-size: 0.7rem;
    
            margin-top: 25px;
        }
        /* ============================================================
        BOTONES DE NAVEGACIÓN DEL SIDEBAR
        ============================================================ */
    
        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            border-radius: 9px;
            border: 1px solid #1e334d;
            background: #101b2b;
            color: #cbd5e1 !important;
            font-size: 0.78rem;
            font-weight: 600;
            text-align: left;
            padding: 10px 14px;
            margin-bottom: 7px;
        }
    
        [data-testid="stSidebar"] .stButton > button:hover {
            background: #16283d;
            border-color: #285070;
            color: #f8fafc !important;
        }
    
        [data-testid="stSidebar"] .stButton > button p {
            color: inherit !important;
        }
    
    
        /* ============================================================
        ANÁLISIS MULTI-AGENTE
        ============================================================ */
    
        .analysis-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }
    
        .analysis-title {
            color: #f8fafc;
            font-size: 2rem;
            font-weight: 700;
        }
    
        .analysis-subtitle {
            color: #64748b;
            font-size: 0.88rem;
            margin-top: 5px;
        }
    
        .analysis-status {
            background: #0d1b2b;
            border: 1px solid #1e334d;
            border-radius: 20px;
            padding: 9px 15px;
            color: #94a3b8;
            font-size: 0.75rem;
        }
    
    
        /* ============================================================
        CONSULTA
        ============================================================ */
    
        .analysis-query-card {
            background: #0d1928;
            border: 1px solid #1e334d;
            border-radius: 16px;
            padding: 22px;
            min-height: 145px;
        }
    
        .query-label {
            color: #64748b;
            font-size: 0.67rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            margin-bottom: 12px;
        }
    
        .query-title {
            color: #e2e8f0;
            font-size: 1rem;
            font-weight: 600;
            line-height: 1.5;
        }
    
        .analysis-info-card {
            background: #0d1928;
            border: 1px dashed #28435f;
            border-radius: 16px;
            padding: 22px;
            min-height: 145px;
    
            display: flex;
            align-items: center;
            gap: 16px;
        }
    
        .info-icon {
            width: 45px;
            height: 45px;
            border-radius: 12px;
    
            background: rgba(14, 165, 233, 0.12);
            border: 1px solid rgba(14, 165, 233, 0.25);
    
            color: #38bdf8;
    
            display: flex;
            align-items: center;
            justify-content: center;
    
            font-size: 0.75rem;
            font-weight: 800;
        }
    
        .info-title {
            color: #e2e8f0;
            font-size: 0.9rem;
            font-weight: 700;
        }
    
        .info-text {
            color: #64748b;
            font-size: 0.72rem;
            line-height: 1.5;
            margin-top: 6px;
        }
    
    
        /* ============================================================
        TÍTULOS
        ============================================================ */
    
        .analysis-section-title {
            color: #f8fafc;
            font-size: 1.05rem;
            font-weight: 700;
            margin-top: 25px;
        }
    
        .analysis-section-subtitle {
            color: #64748b;
            font-size: 0.72rem;
            margin-top: 4px;
            margin-bottom: 14px;
        }
    
    
        /* ============================================================
        FLUJO DE AGENTES
        ============================================================ */
    
        .agent-flow {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
        }
    
        .flow-agent {
            flex: 1;
    
            min-height: 105px;
    
            background: #0d1928;
            border: 1px solid #1e334d;
            border-radius: 14px;
    
            padding: 15px;
    
            display: flex;
            align-items: center;
            gap: 12px;
        }
    
        .flow-icon {
            width: 42px;
            height: 42px;
    
            border-radius: 11px;
    
            background: #101f32;
    
            display: flex;
            align-items: center;
            justify-content: center;
    
            font-size: 1.1rem;
        }
    
        .flow-number {
            color: #64748b;
            font-size: 0.6rem;
            font-weight: 700;
            letter-spacing: 0.08em;
        }
    
        .flow-name {
            color: #e2e8f0;
            font-size: 0.88rem;
            font-weight: 700;
            margin-top: 4px;
        }
    
        .flow-status {
            color: #64748b;
            font-size: 0.68rem;
            margin-top: 4px;
        }
    
        .flow-arrow {
            color: #334e68;
            font-size: 1.3rem;
            flex-shrink: 0;
        }
    
        .agent-completed {
            border-color: rgba(34, 197, 94, 0.35);
        }
    
        .agent-completed .flow-icon {
            background: rgba(34, 197, 94, 0.1);
        }
    
        .agent-completed .flow-status {
            color: #22c55e;
        }
    
        .agent-pending .flow-status {
            color: #64748b;
        }
    
    
        /* ============================================================
        RESULTADOS
        ============================================================ */
    
        .analysis-results-header {
            margin-top: 25px;
            margin-bottom: 10px;
        }
    
        .result-agent-header {
            display: flex;
            align-items: center;
            gap: 12px;
    
            background: #0d1928;
            border: 1px solid #1e334d;
            border-radius: 12px;
    
            padding: 14px 16px;
    
            margin-bottom: 12px;
        }
    
        .result-agent-icon {
            width: 38px;
            height: 38px;
    
            border-radius: 10px;
    
            background: #101f32;
    
            display: flex;
            align-items: center;
            justify-content: center;
        }
    
        .result-agent-number {
            color: #64748b;
            font-size: 0.6rem;
            font-weight: 700;
            letter-spacing: 0.08em;
        }
    
        .result-agent-name {
            color: #e2e8f0;
            font-size: 0.82rem;
            font-weight: 700;
            margin-top: 3px;
        }
    
    
        /* ============================================================
        REVISIÓN HUMANA
        ============================================================ */
    
        .human-review-card {
            display: flex;
            align-items: center;
            gap: 14px;
    
            background: rgba(14, 165, 233, 0.06);
            border: 1px solid rgba(14, 165, 233, 0.2);
            border-radius: 14px;
    
            padding: 17px;
    
            margin-top: 20px;
        }
    
        .human-review-icon {
            width: 40px;
            height: 40px;
    
            border-radius: 10px;
    
            background: rgba(14, 165, 233, 0.1);
    
            display: flex;
            align-items: center;
            justify-content: center;
        }
    
        .human-review-title {
            color: #7dd3fc;
            font-size: 0.8rem;
            font-weight: 700;
        }
    
        .human-review-text {
            color: #64748b;
            font-size: 0.7rem;
            line-height: 1.5;
            margin-top: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
