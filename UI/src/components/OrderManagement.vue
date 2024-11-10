<template>
    <div class="main-page">
        <header>
            <img src="@/assets/logounla.png" alt="Logo de la Universidad" class="logo" />
            <h1>
                Sistema de Gestión<br />
                <span class="highlight">Crear Orden</span>
            </h1>
        </header>
        <main>
            <form @submit.prevent="submitOrder" class="form-container">

                <!-- Store ID -->
                <div class="form-group">
                    <label for="storeId" class="form-label">Store ID:</label>
                    <input type="number" v-model="orderData.storeId" class="form-control" required
                        placeholder="Enter Store ID" />
                </div>

                <!-- Observations -->
                <div class="form-group">
                    <label for="observations" class="form-label">Observations:</label>
                    <input type="text" v-model="orderData.observations" class="form-control"
                        placeholder="Enter any observations" />
                </div>

                <!-- Dispatch Order -->
                <div class="form-group">
                    <label for="dispatchOrder" class="form-label">Dispatch Order:</label>
                    <input type="text" v-model="orderData.dispatchOrder" class="form-control"
                        placeholder="Dispatch Order Code" />
                </div>

                <!-- Items Section -->
                <div v-for="(item, index) in orderData.items" :key="index" class="item-group">
                    <h5>Item {{ index + 1 }}</h5>

                    <div class="form-group">
                        <input type="text" v-model="item.itemCode" class="form-control" placeholder="Item Code"
                            required />
                    </div>
                    <div class="form-group">
                        <input type="text" v-model="item.color" class="form-control" placeholder="Color" />
                    </div>
                    <div class="form-group">
                        <input type="text" v-model="item.size" class="form-control" placeholder="Size" />
                    </div>
                    <div class="form-group">
                        <input type="number" v-model="item.quantity" class="form-control" placeholder="Quantity"
                            required />
                    </div>
                    <button type="button" class="btn-remove" @click="removeItem(index)">Remove Item</button>
                </div>

                <button type="button" class="btn-add" @click="addItem">Add Item</button>
                <button type="submit" class="btn-submit">Create Order</button>
            </form>
            <button @click="goToDashboard" class="back-button">Volver al Dashboard</button>
        </main>
    </div>
</template>

<script>
import apiClient from "@/api/apiClient.ts";

export default {
    data() {
        return {
            orderData: {
                storeId: null,
                observations: "",
                dispatchOrder: "",
                items: [
                    { itemCode: "", color: "", size: "", quantity: 1 }
                ]
            }
        };
    },
    methods: {
        addItem() {
            this.orderData.items.push({ itemCode: "", color: "", size: "", quantity: 1 });
        },
        removeItem(index) {
            this.orderData.items.splice(index, 1);
        },
        async submitOrder() {
            try {
                const response = await apiClient.createOrder(this.orderData);
                console.log("Order created successfully:", response);
                alert("Order created successfully!");

                // Resetear el formulario a sus valores iniciales
                this.orderData = {
                    storeId: null,
                    observations: "",
                    dispatchOrder: "",
                    items: [{ itemCode: "", color: "", size: "", quantity: 1 }]
                };
            } catch (error) {
                console.error("Error creating order:", error);
                alert("Failed to create order");
            }
        },
        goToDashboard() {
            this.$router.push('/main');
        }
    }
};
</script>

<style scoped>
.main-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background-color: #282c34;
    min-height: 100vh;
    color: white;
    font-family: 'Arial', sans-serif;
}

.logo {
    width: 150px;
    margin-bottom: 20px;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 20px;
    text-align: center;
}

.highlight {
    color: #9b1c30;
    font-weight: bold;
}

.form-container {
    display: flex;
    flex-direction: column;
    background-color: #444;
    border-radius: 10px;
    padding: 20px;
    width: 100%;
    max-width: 500px;
    border: 2px solid #9b1c30;
}

.form-group {
    margin-bottom: 15px;
}

.form-control {
    width: 100%;
    padding: 8px;
    border-radius: 5px;
    border: 1px solid #ddd;
}

.item-group {
    background-color: #333;
    border: 1px solid #9b1c30;
    border-radius: 8px;
    padding: 15px;
    margin-top: 10px;
}

h5 {
    color: #9b1c30;
}

.btn-add,
.btn-submit,
.btn-remove {
    background-color: #9b1c30;
    color: white;
    border: none;
    padding: 10px 15px;
    margin-top: 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn-add:hover,
.btn-submit:hover,
.btn-remove:hover {
    background-color: #7a1522;
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

.btn-remove {
    background-color: #d9534f;
}

.btn-remove:hover {
    background-color: #c9302c;
}
</style>