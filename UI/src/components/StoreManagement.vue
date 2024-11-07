<template>
    <div class="store-management">
      <router-link to="/main" class="back-button">Volver al Dashboard</router-link>
      <h2>Gestión de Tiendas</h2>
      <div class="filter-container">
    <input type="text" class="filter-input" v-model="storeCode" placeholder="Buscar por código de tienda" />
    <label>
        <input type="checkbox" v-model="enabled" /> Habilitado?
    </label>
    <button @click="searchStores" class="filter-button">Buscar</button>
</div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Código</th>
              <th>Dirección</th>
              <th>Ciudad</th>
              <th>Estado</th>
              <th>Habilitado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="store in stores" :key="store?.id">
                <td>{{ store?.id || 'N/A' }}</td>
                <td>{{ store?.code || 'N/A' }}</td>
                <td>{{ store?.address || 'N/A' }}</td>
                <td>{{ store?.city || 'N/A' }}</td>
                <td>{{ store?.state || 'N/A' }}</td>
                <td>{{ store?.enabled ? 'Sí' : 'No' }}</td>
                <td>
                <button @click="editStore(store?.id)" class="action-button" v-if="store?.id">Editar</button>
                <button @click="toggleStoreState(store?.id)" class="action-button" v-if="store?.id">
                {{ store?.enabled ? 'Deshabilitar' : 'Habilitar' }}
                </button>
        </td>
        </tr>

          </tbody>
        </table>
      </div>
      <button @click="showAddStoreForm = true" class="add-store-button">Agregar Tienda</button>
      
      <!-- Modal para agregar tienda -->
      <div v-if="showAddStoreForm" class="modal">
        <div class="modal-content">
          <span class="close" @click="showAddStoreForm = false">&times;</span>
          <h3>Agregar Nueva Tienda</h3>
          <form @submit.prevent="addStore">
            <input v-model="newStore.code" placeholder="Código de Tienda" required />
            <input v-model="newStore.address" placeholder="Dirección" required />
            <input v-model="newStore.city" placeholder="Ciudad" required />
            <input v-model="newStore.state" placeholder="Estado" required />
            <label>
              Habilitado?
              <input type="checkbox" v-model="newStore.enabled" />
              <h3>Habilidato?</h3>
            </label>
            <button type="submit" class="submit-button">Crear Tienda</button>
            <button type="button" @click="showAddStoreForm = false" class="cancel-button">Cancelar</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import apiClient from '@/api/apiClient.ts';
  
  export default {
    data() {
      return {
        stores: [],
        showAddStoreForm: false,
        newStore: {
          code: '',
          address: '',
          city: '',
          state: '',
          enabled: true,
        },
        filterCode: '',
        filterState: ''
      };
    },
    methods: {
      async fetchStores() {
        try {
        const responseDisabled = await apiClient.searchStore({ enabled: false });
        const disabledStores = responseDisabled?.stores || [];
        const responseEnabled = await apiClient.searchStore({ enabled: true });
        const enabledStores = responseEnabled?.stores || [];

        const allStores = [...disabledStores, ...enabledStores];

        // Asigna la lista combinada a this.stores
        this.stores = allStores;
    } catch (error) {
        console.error('Error al obtener las tiendas:', error);
    }
      },
      async addStore() {
        try {
          const response = await apiClient.createStore(this.newStore);
          this.stores.push(response.store);
          this.showAddStoreForm = false;
        } catch (error) {
          console.error('Error al agregar la tienda:', error);
        }
      },
      async toggleStoreState(storeId) {
        try {
          const store = this.stores.find(s => s.id === storeId);
          const response = await apiClient.toggleStoreState(storeId, !store.enabled);
          store.enabled = response.enabled;
        } catch (error) {
          console.error('Error al cambiar el estado de la tienda:', error);
        }
      },
      async filterStores() {
        try {
          const response = await apiClient.searchStores(this.filterCode, this.filterState);
          this.stores = response.stores;
        } catch (error) {
          console.error('Error al filtrar las tiendas:', error);
        }
      }
    },
    mounted() {
      this.fetchStores();
    }
  };
  </script>
  
  <style scoped>
  .store-management {
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
    overflow-x: auto;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    background-color: #222;
    border-radius: 10px;
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
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .action-button:hover {
    background-color: #9b1c30;
  }
  
  .add-store-button {
    background-color: #444;
    font-size: large;
    border: none;
    border-radius: 5px;
    color: white;
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .add-store-button:hover {
    background-color: #9b1c30;
  }
  
  .modal {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    z-index: 1000;
  }
  
  .modal-content {
    background-color: #000;
    color: #fff;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    width: 400px;
    position: relative;
  }
  
  .close {
    position: absolute;
    top: 10px;
    right: 15px;
    color: #fff;
    font-size: 24px;
    cursor: pointer;
  }
  
  .submit-button, .cancel-button {
    background-color: #9b1b30;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-right: 10px;
  }
  
  .submit-button:hover, .cancel-button:hover {
    background-color: #7a1522;
  }



.filter-button:hover {
    background-color: #7a1522; /* Color más oscuro al pasar el mouse */
}
  


.filter-input::placeholder {
    color: #fff; /* Color del texto placeholder */
}

.filter-input:focus {
    outline: none; /* Eliminar borde azul al hacer foco */
    background-color: #7a1522; /* Color más oscuro al hacer foco */
}

.filter-container {
    display: flex; /* Usa flexbox */
    align-items: center; /* Centra verticalmente los elementos */
    gap: 10px; /* Espacio entre el input y el botón */
}

.filter-button {
    margin-left: 0; /* Asegúrate de que no haya margen izquierdo */
}

.filter-container {
    display: flex;
    align-items: center;
    gap: 10px;
}

.filter-input {
    border-radius: 5px; /* Bordes redondeados */
    background-color: #333; /* Fondo oscuro */
    color: #fff; /* Texto blanco */
    padding: 10px; /* Espaciado interno */
}

.filter-button {
    background-color: #9b1b30; /* Color granate */
    color: #fff; /* Texto blanco */
    border: none; /* Sin borde */
    border-radius: 5px; /* Bordes redondeados */
    padding: 10px 15px; /* Espaciado interno */
    cursor: pointer; /* Cambia el cursor al pasar el ratón */
}


  </style>
  