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
                            <button @click="editUser(user)" class="action-button">Editar</button>
                            <button @click="deleteUser(user.id)" class="action-button delete">Eliminar</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <button @click="showAddUserForm = true" class="add-user-button">Agregar Usuario</button>
        <!-- Modal -->
        <div v-if="showAddUserForm" class="modal">
            <div class="modal-content">
                <span class="close" @click="showAddUserForm = false">&times;</span>
                <h3>Agregar Nuevo Usuario</h3>
                <form @submit.prevent="addUser">
                    <input v-model="newUser.username" placeholder="Nombre de Usuario" required />
                    <input v-model="newUser.password" placeholder="Contraseña" required />
                    <input v-model="newUser.firstName" placeholder="Primer Nombre" required />
                    <input v-model="newUser.lastName" placeholder="Apellido" required />
                    <label>
                        Habilitado:
                        <input type="checkbox" v-model="newUser.enabled" />
                    </label>
                    <label>
                        Es Casa Central:
                        <input type="checkbox" v-model="newUser.isCentral" />
                    </label>
                    <input v-model="newUser.storeId" placeholder="ID de Tienda" />
                    <button type="submit" class="submit-button">Crear Usuario</button>
                    <button type="button" @click="showAddUserForm = false" class="cancel-button">Cancelar</button>
                </form>
            </div>

        </div>
        <!-- Modal para editar user-->
        <div v-if="showEditUserForm" class="modal">
            <div class="modal-content">
                <span class="close" @click="showEditUserForm = false">&times;</span>
                <h3>Editar Usuario</h3>
                <form @submit.prevent="updateUser">
                    <input v-model="editUserData.username" placeholder="Nombre de Usuario" required />
                    <input v-model="editUserData.password" placeholder="Contraseña" required />
                    <input v-model="editUserData.firstName" placeholder="Primer Nombre" required />
                    <input v-model="editUserData.lastName" placeholder="Apellido" required />
                    <label>
                        Habilitado:
                        <input type="checkbox" v-model="editUserData.enabled" />
                    </label>
                    <button type="submit" class="submit-button">Actualizar Usuario</button>
                    <button type="button" @click="showEditUserForm = false" class="cancel-button">Cancelar</button>
                </form>
            </div>
        </div>
    </div>
</template>

<!-- LOGICA-->
<script>
import apiClient from '@/api/apiClient.ts';

export default {
    name: "UserManagement",
    data() {
        return {
            users: [],
            showAddUserForm: false, // Asegúrate de que esté aquí
            newUser: {
                username: '',
                firstName: '',
                lastName: '',
                enabled: true, // Valor por defecto
                isCentral: false, // Valor por defecto
                storeId: null, // ID de tienda, puede ser null si no aplica
            },
            editUserData: {
                username: '',
                password: '',
                firstName: '',
                lastName: '',
                enabled: false,
            },
            showEditUserForm: false,
            selectedUser: null
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
        async addUser() {
            try {
                const response = await apiClient.createUser(this.newUser);
                console.log("Usuario creado:", response);
                this.showAddUserForm = false;

                await this.fetchUsers();

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
        editUser(user) { // Método para cargar los datos en el formulario
            this.selectedUser = user; // Almacena el usuario seleccionado
            // Precarga datos en editUserData
            this.editUserData.username = user.username;
            this.editUserData.password = user.password;
            this.editUserData.firstName = user.firstName;
            this.editUserData.lastName = user.lastName;
            this.editUserData.enabled = user.enabled;
            this.showEditUserForm = true; // Muestra el formulario de edición
        },

        async updateUser() {
            try {
                const response = await apiClient.updateUser({
                    username: this.editUserData.username,
                    password: this.editUserData.password,
                    firstName: this.editUserData.firstName,
                    lastName: this.editUserData.lastName,
                    enabled: this.editUserData.enabled,
                });
                console.log("Usuario actualizado:", response);

                // Actualizar la lista de usuarios
                await this.fetchUsers(); // Refresca la lista de usuarios
                this.showEditUserForm = false; // Oculta el formulario de edición
                this.resetEditUser(); // Reinicia el formulario de edición
            } catch (error) {
                console.error("Error al actualizar el usuario:", error);
                // Manejo de errores...
            }
        },

        resetEditUser() {
            this.editUserData = { // Reinicia editUserData
                username: '',
                password: '',
                firstName: '',
                lastName: '',
                enabled: false,
            };
            this.selectedUser = null; // Limpia el usuario seleccionado
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




<!--ESTILOS DE LA TABLA MEPA-->
<style scoped>
.user-management {
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
    /* Permite desplazamiento horizontal en caso de que la tabla sea más ancha que el contenedor */
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

/*MODAL STYLES DEL FORM DE AGREGAR USUARIO*/

.user-management {
    padding: 20px;
}

.table-container {
    margin-bottom: 20px;
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
    /* Fondo negro con opacidad */
    z-index: 1000;
    /* Asegura que el modal esté en la parte superior */
}

.modal-content {
    background-color: #000;
    /* Fondo negro para el contenido del modal */
    color: #fff;
    /* Texto blanco */
    padding: 30px;
    /* Espaciado interno */
    border-radius: 10px;
    /* Bordes redondeados */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    /* Sombra */
    width: 400px;
    /* Ancho del modal */
    position: relative;
    /* Para el botón de cerrar */
}

.close {
    position: absolute;
    /* Posicionamiento absoluto */
    top: 10px;
    /* Ajusta la posición superior */
    right: 15px;
    /* Ajusta la posición derecha */
    color: #fff;
    /* Color del botón de cerrar */
    font-size: 24px;
    /* Tamaño del texto */
    cursor: pointer;
    /* Cambia el cursor al pasar el ratón */
}

h3 {
    margin-bottom: 20px;
    /* Espaciado inferior */
    font-size: 22px;
    /* Tamaño del encabezado */
}

input[type="text"],
input[type="password"],
input[type="checkbox"] {
    width: 100%;
    /* Ancho completo */
    padding: 10px;
    /* Espaciado interno */
    margin-bottom: 15px;
    /* Espaciado inferior */
    border: none;
    /* Sin borde */
    border-radius: 5px;
    /* Bordes redondeados */
    background-color: #333;
    /* Fondo gris oscuro para los inputs */
    color: #fff;
    /* Texto blanco */
    font-size: 16px;
    /* Tamaño de fuente */
}

input[type="checkbox"] {
    width: auto;
    /* Ancho automático para los checkboxes */
    margin-right: 5px;
    /* Espaciado a la derecha */
}

.submit-button,
.cancel-button {
    background-color: #9b1b30;
    /* Color granate */
    color: #fff;
    /* Texto blanco */
    border: none;
    /* Sin borde */
    border-radius: 5px;
    /* Bordes redondeados */
    padding: 10px 15px;
    /* Espaciado interno */
    cursor: pointer;
    /* Cambia el cursor al pasar el ratón */
    transition: background-color 0.3s ease;
    /* Transición de fondo */
    margin-right: 10px;
    /* Espaciado entre botones */
}

.submit-button:hover,
.cancel-button:hover {
    background-color: #7a1522;
    /* Color más oscuro al pasar el ratón */
}
</style>