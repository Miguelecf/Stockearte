<template>
    <div class="user-management">
      <router-link to="/" class="back-button">Volver al Dashboard</router-link>
      <h2>Gestión de Usuarios</h2>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Codigo</th>
              <th>Username</th>
              <th>Nombre</th>
              <th>Apellido</th>
              <th>Habilitado</th>
              <th>Es Casa Central</th>
              <th>Codigo de Tienda</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users.users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.firstName }}</td>
              <td>{{ user.lastName }}</td>
              <td>{{ user.enabled ? 'Sí' : 'No' }}</td>
              <td>{{ user.isCentral ? 'Sí' : 'No' }}</td>
              <td>{{ user.storeId }}</td>
              <td>
                <button @click="editUser(user.id)" class="action-button">Editar</button>
                <button @click="deleteUser(user.id)" class="action-button delete">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <button @click="addUser" class="add-user-button">Agregar Usuario</button>
    </div>
  </template>

<script>
import apiClient from '@/api/apiClient.ts';

export default {
  name: "UserManagement",
  data() {
    return {
      users: [],
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await apiClient.listUsers(); // Llama a la API para obtener usuarios
        this.users = response.users; // Ajusta esto según la estructura de la respuesta
        console.log("Usuarios cargados:", response); // Imprime los usuarios para verificar
      } catch (error) {
        console.error("Error al obtener los usuarios:", error);
      }
    },
    addUser() {
      console.log("Agregar usuario");
    },
    editUser(id) {
      console.log(`Editar usuario con ID: ${id}`);
    },
    deleteUser(id) {
      console.log(`Eliminar usuario con ID: ${id}`);
    },
  },
  mounted() {
    this.fetchUsers(); // Llama a la función cuando se monta el componente para cargar los usuarios
  },
};
</script>




  <style scoped>.user-management {
    padding: 40px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .back-button {
    background-color: #444;
    border: none;
    border-radius: 5px;
    color: white;
    padding: 10px 20px;
    margin-bottom: 20px;
    text-decoration: none;
    transition: background-color 0.3s;
  }
  
  .back-button:hover {
    background-color: #9b1c30;
  }
  
  .table-container {
    max-width: 800px;
    width: 100%;
    margin-bottom: 20px;
    overflow-x: auto; /* Permite desplazamiento horizontal en caso de que la tabla sea más ancha que el contenedor */
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    background-color: #222;
    border-radius: 10px;
    overflow: hidden;
  }
  
  th, td {
    border: 1px solid #333;
    padding: 12px;
    text-align: left;
  }
  
  th {
    background-color: #9b1c30;
    color: white;
  }
  
  .action-button {
    background-color: #444;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    color: white;
    margin-right: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .action-button:hover {
    background-color: #9b1c30;
  }
  
  .action-button.delete {
    background-color: #d9534f;
  }
  
  .action-button.delete:hover {
    background-color: #c9302c;
  }
  
  .add-user-button {
    background-color: #444;
    font-size: large;
    border: none;
    border-radius: 5px;
    color: white;
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .add-user-button:hover {
    background-color: #9b1c30;
  }
  </style>