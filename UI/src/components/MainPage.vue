<template>
    <div class="main-page">
      <header>
        <img src="@/assets/logounla.png" alt="Logo de la Universidad" class="logo" />
        <h1>
          Sistema de Gestión<br />
          <span class="highlight">Stockearte</span>
        </h1>
      </header>
      <main>
        <div class="options-container">
          <router-link to="/user-management" class="option-card">Ir a Gestión de Usuarios</router-link>
          <router-link to="/stores" class="option-card">Gestión de Tiendas</router-link>
          <router-link to="/products" class="option-card">Gestión de Productos</router-link>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: "MainPage",
  };
  </script>
  
  <style scoped>
  .main-page {
    display: flex;
    flex-direction: column;
    align-items: center; /* Centrar horizontalmente */
    justify-content: center; /* Centrar verticalmente */
    padding: 20px;
    background-color: #282c34;
    min-height: 100vh; /* Ocupa toda la altura */
    color: white;
    font-family: 'Arial', sans-serif;
  }
  
  .logo {
    width: 150px; /* Ajusta el tamaño del logo */
    margin-bottom: 20px; /* Espacio entre el logo y el título */
  }
  
  header h1 {
    font-size: 2.5rem;
    margin-bottom: 20px;
    text-align: center; /* Centrar texto */
  }
  
  .highlight {
    color: #9b1c30; /* Color granate */
    font-weight: bold;
  }
  
  .options-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .option-card {
    background-color: #444; /* Color de fondo de las tarjetas */
    border: 2px solid #9b1c30; /* Color del borde */
    border-radius: 10px;
    padding: 15px 30px;
    margin: 10px;
    color: white;
    text-decoration: none;
    font-size: 1.2rem;
    transition: background-color 0.3s, transform 0.3s; /* Animación suave */
  }
  
  .option-card:hover {
    background-color: #9b1c30; /* Cambia a granate al pasar el ratón */
    transform: translateY(-3px); /* Efecto de elevación */
  }
  </style>
  