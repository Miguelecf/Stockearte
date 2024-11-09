<template>
    <div class="store-management">
      <router-link to="/main" class="back-button">Volver al Dashboard</router-link>
      <h2>Gestión de productos</h2>
      <div class="filter-container">
    <input type="text" class="filter-input" v-model="storeCode" placeholder="Buscar por código de producto" />
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
              <th>Nombre</th>
              <th>Tamaño</th>
              <th>Color</th>
              <th>Habilitado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product?.id">
              <td>{{ product?.id || 'N/A' }}</td>
              <td>{{ product?.unique_code || 'N/A' }}</td>
              <td>{{ product?.name || 'N/A' }}</td>
              <td>{{ product?.size || 'N/A' }}</td>
              <td>{{ product?.color || 'N/A' }}</td>
              <td>{{ product?.enabled ? 'Sí' : 'No' }}</td>
              <td>
                <button @click="editProduct(product?.id)" class="action-button" v-if="product?.id">Editar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <button @click="showAddProductForm = true" class="add-store-button">Agregar Producto</button>
      
      <!-- Modal para agregar producto -->
      <div v-if="showAddProductForm" class="modal">
        <div class="modal-content">
          <span class="close" @click="showAddProductForm = false">&times;</span>
          <h3>Agregar Nuevo Producto</h3>
          <form @submit.prevent="addProduct">
            <input v-model="newProduct.unique_code" placeholder="Código Único del Producto" required />
            <input v-model="newProduct.name" placeholder="Nombre del Producto" required />
            <input v-model="newProduct.size" placeholder="Tamaño" required />
            <input v-model="newProduct.color" placeholder="Color" required />
            <label>
              Habilitado?
              <input type="checkbox" v-model="newProduct.enabled" />
            </label>
            <button type="submit" class="submit-button">Crear Producto</button>
            <button type="button" @click="showAddProductForm = false" class="cancel-button">Cancelar</button>
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
      products: [],
      showAddProductForm: false,
      newProduct: {
        unique_code: '',
        name: '',
        size: '',
        color: '',
        enabled: true,
      },
      productCode: '',
      enabled: false,
    };
  },
  methods: {
    async fetchProducts() {
      try {
        const responseDisabled = await apiClient.searchProduct({ enabled: false });
        const disabledProducts = responseDisabled?.products || [];
        const responseEnabled = await apiClient.searchProduct({ enabled: true });
        const enabledProducts = responseEnabled?.products || [];
        this.products = [...disabledProducts, ...enabledProducts];
      } catch (error) {
        console.error('Error al obtener los productos:', error);
      }
    },
    async addProduct() {
      try {
        const response = await apiClient.createProduct(this.newProduct);
        this.products.push(response.product);
        this.showAddProductForm = false;
      } catch (error) {
        console.error('Error al agregar el producto:', error);
      }
    },
    async toggleProductStatus(productId) {
      try {
        const product = this.products.find(p => p.id === productId);
        const response = await apiClient.toggleProductStatus(productId, !product.enabled);
        product.enabled = response.enabled;
      } catch (error) {
        console.error('Error al cambiar el estado del producto:', error);
      }
    },
    async searchProducts() {
      try {
        const response = await apiClient.searchProducts(this.productCode, this.enabled);
        this.products = response.products;
      } catch (error) {
        console.error('Error al filtrar los productos:', error);
      }
    },
  },
  mounted() {
    this.fetchProducts();
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
