<template>
  <div id="app">
    <router-view /> <!-- Renderiza el componente de la ruta actual -->
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Estilos globales */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  background-color: black;
  color: white;
  font-family: 'Arial', sans-serif;
}

#app {
  height: 100%;
}
</style>
