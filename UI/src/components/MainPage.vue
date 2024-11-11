<template>
  <div class="main-page">
    <!-- Botón de Logout -->
    <button @click="logout" class="logout-button">Cerrar sesión</button>

    <header>
      <img src="@/assets/logounla.png" alt="Logo de la Universidad" class="logo" />
      <h1>
        Sistema de Gestión<br />
        <span class="highlight">Stockearte</span>
      </h1>
    </header>
    <main>
      <div class="options-container">
        <router-link to="/user-management" class="option-card">Gestión de Usuarios</router-link>
        <router-link to="/store-management" class="option-card">Gestión de Tiendas</router-link>
        <router-link to="/product-management" class="option-card">Gestión de Productos</router-link>
        <router-link to="/order-management" class = "option-card">Crear Orden de Compra</router-link>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "MainPage",
  methods: {
    logout() {
      // Elimina el token del localStorage
      localStorage.removeItem('auth_token');
      
      // Redirige al login
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.main-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: #282c34;
  min-height: 100vh;
  color: white;
  font-family: 'Arial', sans-serif;
  position: relative;
}

.logo {
  width: 150px;
  margin-bottom: 20px;
}

header h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  text-align: center;
}

.highlight {
  color: #9b1c30;
  font-weight: bold;
}

.options-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.option-card {
  background-color: #444;
  border: 2px solid #9b1c30;
  border-radius: 10px;
  padding: 15px 30px;
  margin: 10px;
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
  transition: background-color 0.3s, transform 0.3s;
}

.option-card:hover {
  background-color: #9b1c30;
  transform: translateY(-3px);
}

/* Estilos para el botón de Logout */
.logout-button {
  background-color: #9b1c30;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  position: absolute;
  top: 20px;
  left: 20px;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background-color: #7a1522;
}
</style>
