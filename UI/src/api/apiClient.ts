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
    /*async deleteUser(id) {
      const response = await apiClient.delete(`/delete-user/${id}`); // Ajusta según tu lógica
      return response.data;
    },*/
  };