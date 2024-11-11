<template>
  <div class="product-management">
    <router-link to="/main" class="back-button">Volver al Dashboard</router-link>
    <h1>Gestión de Productos</h1>

    <!-- Formulario de búsqueda -->
    <form @submit.prevent="searchProducts" class="search-form">
      <div class="filter-container">
        <label for="name" class="filter-label">Nombre</label>
        <input type="text" v-model="filters.name" id="name" class="filter-input" />
      </div>
      <div class="filter-container">
        <label for="uniqueCode" class="filter-label">Código Único</label>
        <input type="text" v-model="filters.uniqueCode" id="uniqueCode" class="filter-input" />
      </div>
      <div class="filter-container">
        <label for="size" class="filter-label">Tamaño</label>
        <input type="text" v-model="filters.size" id="size" class="filter-input" />
      </div>
      <div class="filter-container">
        <label for="color" class="filter-label">Color</label>
        <input type="text" v-model="filters.color" id="color" class="filter-input" />
      </div>
      <button type="submit" class="filter-button">Buscar</button>
    </form>

    <!-- Mostrar los productos -->
    <div v-if="products.length" class="table-container">
      <h2>Resultados de la Búsqueda:</h2>
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Código Único</th>
            <th>Tamaño</th>
            <th>Color</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.name }}</td>
            <td>{{ product.uniqueCode }}</td>
            <td>{{ product.size }}</td>
            <td>{{ product.color }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No se encontraron productos.</p>
    </div>
    <div class="button-container">
        <button @click="showAddProductForm = true" class="export-button">Agregar Producto</button>
        <button @click.prevent="exportToPDF1" class="export-button">Exportar a PDF</button>
      </div>
  </div>

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
</template>

<script>
import apiClient from '@/api/apiClient.ts'; // Asegúrate de que la ruta es correcta
import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';

// Asignamos autoTable a jsPDF
jsPDF.autoTable = autoTable;

export default {
  data() {
    return {
      filters: {
        name: '',
        uniqueCode: '',
        size: '',
        color: ''
      },
      products: [],
      showAddProductForm: false,
      newProduct: {
        unique_code: '',
        name: '',
        size: '',
        color: '',
        enabled: false
      }
    };
  },
  methods: {       
    async searchProducts() {
      try {
        // Llamamos a la API de búsqueda de productos
        const response = await apiClient.searchProducts(this.filters);
        this.products = response; // Asumimos que la respuesta es un array de productos
      } catch (error) {
        console.error('Error buscando productos:', error);
      }
    },
    async addProduct() {
      try {
                const response = await apiClient.createProduct(this.newProduct);
                console.log("Producto creado:", response);
                this.showAddProductForm = false;

                //await this.fetchUsers();

            } catch (error) {
                console.error("Error al agregar el usuario:", error);
                if (error.response) {
                    console.error("Response data:", error.response.data);
                    console.error("Response status:", error.response.status);
                    console.error("Response headers:", error.response.headers);
                } else if (error.request) {
                    console.error("Request data:", error.request);
                } else {
                    console.error("Error", error.message);
                }
            }
    },
    exportToPDF() {
      const doc = new jsPDF();
      autoTable(doc, {
          head: [['Código', 'Nombre', 'Tamaño', 'Color', 'Habilitado']],
          body: this.products.map(product => [
            product?.unique_code || 'N/A',
            product?.name || 'N/A',
            product?.size || 'N/A',
            product?.color || 'N/A',
            product?.enabled ? 'Sí' : 'No',
          ]),
      });
      doc.save('products.pdf');
    },
    exportToPDF1() {
      console.log("Redirigiendo...");
      
      // Configuración del popup
      const width = 800;
      const height = 600;
      const left = (window.innerWidth / 2) - (width / 2);
      const top = (window.innerHeight / 2) - (height / 2);
      
      // Abrir el popup
      window.open(
        'http://127.0.0.1:9099/soap/export-pdf', 
        '_blank' 
        ,`width=${width},height=${height},top=${top},left=${left},resizable=yes,scrollbars=yes`
      );
    }
  },
  mounted() {
    // Llamada inicial cuando el componente se monte (si quieres cargar todos los productos al inicio)
    this.searchProducts();
  }
};
</script>

<style scoped>
/* Estilos existentes */
.product-management {
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

/* Aquí mantengo los estilos originales para la tabla y botones */

.table-container {
  max-width: 1000px;
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

th,
td {
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

.action-button:hover {
  background-color: #9b1c30;
}

.add-product-button {
  background-color: #444;
  font-size: large;
  border: none;
  border-radius: 5px;
  color: white;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-product-button:hover {
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
  right: 10px;
  font-size: 24px;
  cursor: pointer;
}

.submit-button,
.cancel-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
}

.submit-button {
  background-color: #444;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #9b1c30;
}

.cancel-button {
  background-color: transparent;
  border: none;
  color: white;
  cursor: pointer;
  text-decoration: underline;
}

.cancel-button:hover {
  color: #9b1c30;
}

.export-button {
  background-color: #444;
  font-size: large;
  border: none;
  border-radius: 5px;
  color: white;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.export-button:hover {
  background-color: #9b1c30;
}

.filter-container {
  display: flex;
  flex-direction: column;
  margin-right: 10px;
}

.filter-input {
  border-radius: 5px;
  background-color: #333;
  color: white;
  padding: 10px;
}

.filter-button {
  padding: 8px;
  font-size: 16px;
}

.filter-button {
  background-color: #444;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.filter-button:hover {
  background-color: #9b1c30;
}
</style>
