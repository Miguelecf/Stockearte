<template>
    <div class="product-management">
        <router-link to="/" class="back-button">Volver al Dashboard</router-link>
        <h2>Gestión de Productos</h2>
        <div class="filter-container">
            <input v-model="filter" placeholder="Filtrar..." class="filter-input" />
            <button @click="searchProducts" class="search-button">Buscar</button>
        </div>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Código Único</th>
                        <th>Tamaño</th>
                        <th>Color</th>
                        <th>Habilitado</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="product in filteredProducts" :key="product.id">
                        <td>{{ product.id }}</td>
                        <td>{{ product.name }}</td>
                        <td>{{ product.unique_code }}</td>
                        <td>{{ product.size }}</td>
                        <td>{{ product.color }}</td>
                        <td>{{ product.enabled ? 'Sí' : 'No' }}</td>
                        <td>
                            <button @click="editProduct(product.id)" class="action-button">Editar</button>
                            <button @click="deleteProduct(product.id)" class="action-button delete">Eliminar</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <button @click="showAddProductForm = true" class="add-product-button">Agregar Producto</button>
        <!-- Modal para agregar producto -->
        <div v-if="showAddProductForm" class="modal">
            <div class="modal-content">
                <span class="close" @click="showAddProductForm = false">&times;</span>
                <h3>Agregar Nuevo Producto</h3>
                <form @submit.prevent="addProduct">
                    <input v-model="newProduct.name" placeholder="Nombre del Producto" required />
                    <input v-model="newProduct.unique_code" placeholder="Código Único" required />
                    <input v-model="newProduct.size" placeholder="Tamaño" required />
                    <input v-model="newProduct.color" placeholder="Color" required />
                    <label>
                        Habilitado
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
    name: "ProductManagement",
    data() {
        return {
            products: [],
            showAddProductForm: false,
            newProduct: {
                name: '',
                unique_code: '',
                size: '',
                color: '',
                enabled: true, // Valor por defecto
            },
            filter: '',
        };
    },
    computed: {
        filteredProducts() {
            return this.products.filter(product =>
                product.name.toLowerCase().includes(this.filter.toLowerCase()) ||
                product.unique_code.toLowerCase().includes(this.filter.toLowerCase())
            );
        },
    },
    methods: {
        async fetchProducts() {
            try {
                const response = await apiClient.listProducts(); // Llama a la API para obtener productos
                this.products = response.products; // Ajusta esto según la estructura de la respuesta
                console.log("Productos cargados:", response);
            } catch (error) {
                console.error("Error al obtener los productos:", error);
            }
        },
        async addProduct() {
            try {
                const response = await apiClient.createProduct(this.newProduct);
                console.log("Producto creado:", response);
                this.showAddProductForm = false;

                await this.fetchProducts();
            } catch (error) {
                console.error("Error al agregar el producto:", error);
            }
        },
        editProduct(id) {
            console.log(`Editar producto con ID: ${id}`);
        },
        deleteProduct(id) {
            console.log(`Eliminar producto con ID: ${id}`);
        },
        searchProducts() {
            // Ya se filtra automáticamente con el input, no se requiere lógica adicional aquí
            console.log("Filtrando productos por:", this.filter);
        }
    },
    mounted() {
        this.fetchProducts(); // Carga los productos al montar el componente
    },
};
</script>

<style scoped>
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

.filter-container {
    display: flex;
    margin-bottom: 20px;
}

.filter-input {
    padding: 10px;
    border: 1px solid #333;
    border-radius: 5px;
    margin-right: 10px;
    background-color: #333;
    color: white;
}

.search-button {
    padding: 10px 20px;
    background-color: #9b1c30;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.search-button:hover {
    background-color: #7a1522;
}

.table-container {
    max-width: 800px;
    width: 100%;
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    background-color: #222;
    border-radius: 10px;
    overflow: hidden;
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

/* Modal Styles */
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

h3 {
    margin-bottom: 20px;
    font-size: 22px;
}

input[type="text"],
input[type="checkbox"] {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: none;
    border-radius: 5px;
    background-color: #333;
    color: #fff;
    font-size: 16px;
}

input[type="checkbox"] {
    width: auto;
    margin-right: 5px;
}

.submit-button,
.cancel-button {
    background-color: #9b1b30;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-right: 10px;
}

.submit-button:hover,
.cancel-button:hover {
    background-color: #7a1522;
}
</style>
