import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Operaciones Fiduciarias", layout="wide")

st.title("📊 Dashboard de Operaciones Fiduciarias")

archivo = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)

    cols_requeridas = [
        'PROVEEDOR',
        'Fecha Grabación Pago',
        'Nombre Negocio',
        'Gestor responsable negocios'
    ]

    faltantes = [c for c in cols_requeridas if c not in df.columns]

    if faltantes:
        st.error(f'Columnas faltantes: {faltantes}')
    else:
        df['Fecha Grabación Pago'] = pd.to_datetime(df['Fecha Grabación Pago'], errors='coerce')

        st.sidebar.header('Filtros')

        proveedores = st.sidebar.multiselect(
            'Proveedor',
            sorted(df['PROVEEDOR'].dropna().astype(str).unique())
        )

        gestores = st.sidebar.multiselect(
            'Gestor',
            sorted(df['Gestor responsable negocios'].dropna().astype(str).unique())
        )

        df_f = df.copy()

        if proveedores:
            df_f = df_f[df_f['PROVEEDOR'].isin(proveedores)]

        if gestores:
            df_f = df_f[df_f['Gestor responsable negocios'].isin(gestores)]

        total_operaciones = len(df_f)
        total_proveedores = df_f['PROVEEDOR'].nunique()
        total_negocios = df_f['Nombre Negocio'].nunique()

        c1,c2,c3 = st.columns(3)
        c1.metric('Operaciones', total_operaciones)
        c2.metric('Proveedores', total_proveedores)
        c3.metric('Negocios', total_negocios)

        st.subheader('Operaciones por Proveedor')
        proveedor_df = df_f.groupby('PROVEEDOR').size().reset_index(name='Operaciones').sort_values('Operaciones', ascending=False)
        fig1 = px.bar(proveedor_df, x='PROVEEDOR', y='Operaciones', color='Operaciones')
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader('Operaciones por Fecha de Grabación')
        fecha_df = df_f.groupby(df_f['Fecha Grabación Pago'].dt.date).size().reset_index(name='Operaciones')
        fig2 = px.line(fecha_df, x='Fecha Grabación Pago', y='Operaciones', markers=True)
        st.plotly_chart(fig2, use_container_width=True)

        col1,col2 = st.columns(2)

        with col1:
            st.subheader('Operaciones por Negocio')
            negocio_df = df_f.groupby('Nombre Negocio').size().reset_index(name='Operaciones').sort_values('Operaciones', ascending=False)
            fig3 = px.bar(negocio_df.head(20), x='Operaciones', y='Nombre Negocio', orientation='h')
            st.plotly_chart(fig3, use_container_width=True)

        with col2:
            st.subheader('Operaciones por Gestor')
            gestor_df = df_f.groupby('Gestor responsable negocios').size().reset_index(name='Operaciones').sort_values('Operaciones', ascending=False)
            fig4 = px.pie(gestor_df, names='Gestor responsable negocios', values='Operaciones')
            st.plotly_chart(fig4, use_container_width=True)

        st.subheader('Detalle de Operaciones')
        st.dataframe(df_f, use_container_width=True)
else:
    st.info('Cargue el archivo Excel para visualizar el dashboard.')
