<template>
    <div class="login-container">
      <h2>Login</h2>
      <div class="login-form">
        <input v-model="username" class="input-field" placeholder="Username" />
        <input v-model="password" type="password" class="input-field" placeholder="Password" />
        <button @click="login" class="submit-button">Login</button>
      </div>
  
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
  
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent } from 'vue';
  import apiClient from '@/api/apiClient.ts'; // Asegúrate de que la ruta es correcta
  
  export default defineComponent({
    name: 'UserLogin',
    data() {
      return {
        username: '',
        password: '',
        error: '', // Para manejar el mensaje de error
        successMessage: '' // Para manejar el mensaje de éxito
      };
    },
    methods: {
      async login() {
        const credentials = {
          username: this.username,
          password: this.password
        };
        try {
          const response = await apiClient.login(credentials); // Asegúrate de que login esté bien definido
          console.log(response);
          
          // Mostrar el mensaje de éxito
          this.successMessage = 'Login successful! Redirecting...';
  
          // Redirigir a la página principal
          setTimeout(() => {
            this.$router.push('/main'); // Cambia la ruta a la página principal después de un login exitoso
          }, 1500); // Espera 1.5 segundos antes de redirigir
  
          // Resetea los mensajes
          this.error = '';
        } catch (error) {
          console.error('Login failed', error);
          this.error = 'Login failed. Please check your credentials and try again.'; // Muestra un mensaje de error
          this.successMessage = ''; // Resetea el mensaje de éxito si el login falla
        }
      }
    }
  });
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #222;
    color: white;
  }
  
  h2 {
    margin-bottom: 20px;
    font-size: 24px;
  }
  
  .login-form {
    width: 300px;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .input-field {
    padding: 10px;
    border-radius: 5px;
    background-color: #333;
    color: #fff;
    border: none;
    font-size: 16px;
  }
  
  .submit-button {
    background-color: #9b1b30;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .submit-button:hover {
    background-color: #7a1522;
  }
  
  .error-message {
    color: red;
    margin-top: 10px;
    text-align: center;
  }
  
  .success-message {
    color: green;
    margin-top: 10px;
    text-align: center;
    font-weight: bold;
  }
  </style>
  