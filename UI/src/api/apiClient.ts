import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:3000',
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
  async login(data) {
    try {
      const response = await apiClient.post('/login', data);
      return response.data; // Asegúrate de devolver los datos de la respuesta
    } catch (error) {
      console.error('Error en el login:', error);
      throw error; // Lanza el error para que el componente lo maneje
    }
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

  //------------------PRODUCT------------------
  async allProduct(){
    const response = await apiClient.get('/search-product'); // Endpoint para listar usuarios
    return response.data; // Ajusta esto según la estructura de tu respuesta
  }

};  
