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
import apiClient from '@/api/apiClient.ts';  // Asegúrate de que la ruta esté correcta

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
                const response = await apiClient.login(credentials);  // Llamada a tu API
                console.log('Login successful:', response);

                // Guarda el token en localStorage
                localStorage.setItem('auth_token', response.token);  // Guarda el token

                this.successMessage = 'Login successful! Redirecting...';
                setTimeout(() => {
                    this.$router.push('/main');  // Redirige al main
                }, 1500); // Espera un segundo antes de redirigir
            } catch (error) {
                console.error('Login failed', error);
                this.error = 'Login failed. Please check your credentials and try again.';
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