<template>
    <div class="login-container">
        <!-- Imagen arriba del texto -->
        <img src="@/assets/logounla.png" alt="Logo de la Universidad" class="logo" />

        <h2>Bienvenido a Stockearte</h2>
        
        <div class="login-form">
            <input v-model="username" class="input-field" placeholder="Usuario" />
            <input v-model="password" type="password" class="input-field" placeholder="Contraseña" />
            <button @click="login" class="submit-button">Iniciar Sesión</button>
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
import apiClient from '@/api/apiClient.ts';

export default {
    data() {
        return {
            username: '',
            password: '',
            error: '',
            successMessage: ''
        };
    },
    methods: {
        async login() {
            const credentials = {
                username: this.username,
                password: this.password
            };

            try {
                const response = await apiClient.login(credentials);

                // Guarda el token en localStorage
                localStorage.setItem('auth_token', response.token);

                this.successMessage = 'Redireccionando...';
                setTimeout(() => {
                    this.$router.push('/main');  // Redirige al main
                }, 1500);
            } catch (error) {
                this.error = 'Fallo el inicio de sesion, revise los datos ingresados.';
            }
        }
    }
};
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

.logo {
    width: 100px; /* Ajusta el tamaño de la imagen */
    margin-bottom: 20px; /* Espacio debajo de la imagen */
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
