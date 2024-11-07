import axios from 'axios';

const apiClient = axios.create({
    baseURL:'http://localhost:3000',
    headers: {
        'Content-Type': 'application/json',
    },
});
// -----------USER-------------
export default {
    async listUsers() {
      const response = await apiClient.get('/list-users'); // Endpoint para listar usuarios
      return response.data; // Ajusta esto según la estructura de tu respuesta
    },
    async createUser(data) {
      const response = await apiClient.post('/create-user', data); // Endpoint para crear usuario
      return response.data;
    },
    async updateUser(data) {
      const response = await apiClient.post('/update-user', data); // Endpoint para actualizar usuario
      return response.data;
    },

// ----------STORE------------------------
async searchStore() {
  const response = await apiClient.get('/search-store'); // Endpoint para listar usuarios
  return response.data; // Ajusta esto según la estructura de tu respuesta
},
async createStore(data) {
  const response = await apiClient.post('/create-store', data); // Endpoint para crear usuario
  return response.data;
},

  };