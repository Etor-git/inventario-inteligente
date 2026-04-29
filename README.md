# Sistema de Inventario Inteligente

Proyecto desarrollado con Flask + MySQL + Docker + Streamlit + Machine Learning para la gestión de inventario, control de productos, dashboard de estadísticas y predicción de agotamiento de stock.

---

# Descripción

Este sistema permite administrar productos de inventario de forma profesional mediante un CRUD completo (Crear, Leer, Actualizar y Eliminar), además de visualizar estadísticas en un dashboard interactivo y predecir cuándo un producto podría agotarse usando Machine Learning.

Este proyecto busca resolver problemas comunes en pequeñas y medianas empresas que aún controlan su inventario manualmente.

---

# Objetivo

Desarrollar un sistema de inventario inteligente que permita:

- Registrar productos
- Visualizar productos almacenados
- Editar productos
- Eliminar productos
- Monitorear stock bajo
- Mostrar dashboard de estadísticas
- Predecir agotamiento de inventario mediante Machine Learning
- Ejecutar todo el sistema con Docker

---

# Tecnologías utilizadas

## Backend
- Flask

## Base de Datos
- MySQL

## Contenedores
- Docker
- Docker Compose

## Dashboard
- Streamlit

## Machine Learning
- Scikit-learn
- Pandas

## Administración de BD
- phpMyAdmin

---

# Estructura del Proyecto

inventario-inteligente/
│
├── app/
│   ├── app.py
│   ├── database.py
│   ├── dashboard.py
│   ├── ml_model.py
│   ├── models.py
│   └── requirements.txt
│
├── mysql/
│   └── init.sql
│
├── Dockerfile
├── docker-compose.yml
└── README.md

---

# Requisitos previos

Antes de ejecutar el proyecto necesitas tener instalado:

- Python 3.11 o superior
- Docker Desktop
- Docker Compose
- Git (opcional)
- Navegador web

En Mac se recomienda tener Docker Desktop correctamente iniciado antes de ejecutar los contenedores.

---

# Instalación y ejecución

## 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/inventario-inteligente.git
cd inventario-inteligente
