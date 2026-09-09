import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Operaciones Fiduciarias",layout="wide",page_icon="📊")

st.title("📊 Dashboard de Operaciones Fiduciarias")
archivo = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    df.columns = df.columns.str.strip()

    req = ["PROVEEDOR","Fecha Grabación Pago","Nombre Negocio","Gestor responsable negocios"]
    faltantes = [c for c in req if c not in df.columns]

    if faltantes:
        st.error(f"Faltan columnas: {', '.join(faltantes)}")
        st.stop()

    df["Fecha Grabación Pago"] = pd.to_datetime(df["Fecha Grabación Pago"], errors="coerce")

    st.sidebar.header("Filtros")
    proveedores = st.sidebar.multiselect("Proveedor", sorted(df["PROVEEDOR"].dropna().astype(str).unique()))
    negocios = st.sidebar.multiselect("Negocio", sorted(df["Nombre Negocio"].dropna().astype(str).unique()))
    gestores = st.sidebar.multiselect("Gestor", sorted(df["Gestor responsable negocios"].dropna().astype(str).unique()))

    df_f = df.copy()
    if proveedores:
        df_f = df_f[df_f["PROVEEDOR"].isin(proveedores)]
    if negocios:
        df_f = df_f[df_f["Nombre Negocio"].isin(negocios)]
    if gestores:
        df_f = df_f[df_f["Gestor responsable negocios"].isin(gestores)]

    c1,c2,c3 = st.columns(3)
    c1.metric("Operaciones", len(df_f))
    c2.metric("Proveedores", df_f["PROVEEDOR"].nunique())
    c3.metric("Negocios", df_f["Nombre Negocio"].nunique())

    prov = df_f.groupby("PROVEEDOR").size().reset_index(name="Operaciones").sort_values("Operaciones",ascending=False)
    st.plotly_chart(px.bar(prov,x="PROVEEDOR",y="Operaciones",title="Operaciones por Proveedor"),use_container_width=True)

    fecha = df_f.groupby(df_f["Fecha Grabación Pago"].dt.date).size().reset_index(name="Operaciones")
    st.plotly_chart(px.line(fecha,x="Fecha Grabación Pago",y="Operaciones",markers=True,title="Operaciones por Fecha"),use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        neg = df_f.groupby("Nombre Negocio").size().reset_index(name="Operaciones").sort_values("Operaciones",ascending=False)
        st.plotly_chart(px.bar(neg.head(20),x="Operaciones",y="Nombre Negocio",orientation='h',title="Top Negocios"),use_container_width=True)
    with col2:
        ges = df_f.groupby("Gestor responsable negocios").size().reset_index(name="Operaciones")
        st.plotly_chart(px.pie(ges,names="Gestor responsable negocios",values="Operaciones",title="Operaciones por Gestor"),use_container_width=True)

    st.dataframe(df_f,use_container_width=True)
