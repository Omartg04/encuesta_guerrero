# src/logic.py
import pandas as pd
import geopandas as gpd
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from src.config import MUNICIPIOS_MAP, SUPERVISORES_CONFIG

def balanced_cluster_optimization(gdf, n_clusters):
    """Algoritmo Húngaro para balanceo de cargas."""
    if len(gdf) <= n_clusters:
        gdf = gdf.copy()
        gdf['Supervisor_ID'] = range(1, len(gdf) + 1)
        return gdf

    # Proyección temporal a UTM para metros
    gdf_utm = gdf.to_crs("EPSG:32614")
    coords = np.column_stack((gdf_utm.geometry.centroid.x, gdf_utm.geometry.centroid.y))
    n_points = len(coords)

    base_size = n_points // n_clusters
    remainder = n_points % n_clusters
    
    cluster_slots = []
    for i in range(n_clusters):
        size = base_size + (1 if i < remainder else 0)
        cluster_slots.extend([i] * size)
    
    kmeans = KMeans(n_clusters=n_clusters, n_init=20, random_state=42)
    kmeans.fit(coords)
    centroids = kmeans.cluster_centers_

    target_coords = centroids[cluster_slots]
    cost_matrix = cdist(coords, target_coords)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    assigned_supervisors = [cluster_slots[c] + 1 for c in col_ind]
    final_assignment = pd.Series(data=assigned_supervisors, index=row_ind).sort_index()
    
    gdf_out = gdf.copy()
    gdf_out['Supervisor_ID'] = final_assignment.values
    return gdf_out

def procesar_todo_el_estado(gdf_global):
    """Procesamiento iterativo por municipio."""
    resultados = []
    for muni_key, nombre_oficial in MUNICIPIOS_MAP.items():
        sub_gdf = gdf_global[gdf_global['nombre_municipio'].str.upper() == nombre_oficial.upper()].copy()
        if not sub_gdf.empty:
            n_supervisores = SUPERVISORES_CONFIG[muni_key]
            sub_gdf = balanced_cluster_optimization(sub_gdf, n_supervisores)
            sub_gdf['Supervisor_Global'] = f"{muni_key[:3]}-" + sub_gdf['Supervisor_ID'].astype(str)
            resultados.append(sub_gdf)
    if resultados:
        return pd.concat(resultados)
    return gpd.GeoDataFrame()