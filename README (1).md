# Dashboard de Operaciones Fiduciarias

## Objetivo
Visualizar:
- Cantidad de operaciones por proveedor.
- Cantidad de operaciones por fecha de grabación de pago.
- Cantidad de operaciones por negocio.
- Cantidad de operaciones por gestor.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

## Archivo esperado
Debe contener como mínimo las columnas:
- PROVEEDOR
- Fecha Grabación Pago
- Nombre Negocio
- Gestor responsable negocios

## Funcionalidades
- Filtros dinámicos.
- KPIs principales.
- Gráficos interactivos.
- Tabla detallada.
- Compatible con Excel (.xlsx).
