import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import { rejects } from "assert";
import * as path from "path";


// Paths to both .proto files
const userProtoPath = path.resolve(__dirname, "../proto/user.proto");
const storeProtoPath = path.resolve(__dirname, "../proto/store.proto");
const productProtoPath = path.resolve(__dirname, "../proto/product.proto");
const productStoreProtoPath = path.resolve(__dirname, "../proto/product_store.proto")
const orderProtoPath = path.resolve(__dirname, "../proto/order.proto");
// Load .proto files
const userPackageDefinition = protoLoader.loadSync(userProtoPath);
const storePackageDefinition = protoLoader.loadSync(storeProtoPath);
const productPackageDefinition = protoLoader.loadSync(productProtoPath);
const productStorePackageDefinition = protoLoader.loadSync(productStoreProtoPath);
const orderPackageDefinition = protoLoader.loadSync(orderProtoPath);

// Combine package definitions
const userProto = grpc.loadPackageDefinition(userPackageDefinition) as any;
const storeProto = grpc.loadPackageDefinition(storePackageDefinition) as any;
const productProto = grpc.loadPackageDefinition(productPackageDefinition) as any;
const productStoreProto = grpc.loadPackageDefinition(productStorePackageDefinition) as any;
const orderProto = grpc.loadPackageDefinition(orderPackageDefinition) as any; 
class Client {
    private userClient: any;
    private storeClient: any;
    private productClient: any;
    private productStoreClient: any;
    private orderClient: any; 

    constructor(host: string) {
        this.userClient = new userProto.user.UserService(host, grpc.credentials.createInsecure());
        this.storeClient = new storeProto.store.StoreService(host, grpc.credentials.createInsecure());
        this.productClient = new productProto.product.ProductService(host, grpc.credentials.createInsecure());
        this.productStoreClient = new productStoreProto.product_store.ProductStoreService(host, grpc.credentials.createInsecure());
        this.orderClient = new orderProto.order.OrderService (host, grpc.credentials.createInsecure());
    }

//-----------------------------------------------USER-------------------------------------------

    async createUser(username: string, password: string, firstName: string, lastName: string,
        enabled: boolean, isCentral: boolean, storeId?: number): Promise<string> {
        return new Promise((resolve, reject) => {
            this.userClient.CreateUser(
                {
                    username,
                    password,
                    firstName,
                    lastName,
                    enabled,
                    isCentral,
                    storeId: storeId !== undefined ? storeId : null // Handle undefined storeId
                },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("User creation failed!"));
                    } else {
                        resolve(response.message);
                    }
                }
            );
        });
    }

    async loginUser(username: string, password: string): Promise<any> {  // Cambia Promise<string> a Promise<any> para que acepte cualquier objeto
        return new Promise((resolve, reject) => {
            this.userClient.Login(
                { username, password },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("Login failed!"));
                    } else {
                        resolve(response);  // Devolver solo la respuesta
                    }
                }
            );
        });
    }

    async updateUser(username: string, password: string, firstName: string, lastName: string, enabled: boolean): Promise<any> {
        return new Promise((resolve, reject) => {
            this.userClient.UpdateUser(
                {
                    username,
                    password,
                    firstName,
                    lastName,
                    enabled
                },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("User update failed!"));
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response);
                    }
                }
            );
        });
    }

    async searchUser(username: string): Promise<any> {
        console.log("Searching for user:", username);
        return new Promise((resolve, reject) => {
            this.userClient.SearchUser(
                { username },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("User search failed!"));
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response); // Asegúrate de que este sea el campo correcto
                    }
                }
            );
        });
    }

    async assignStoreToUser(userId: number, storeCode: string): Promise<any> {
        return new Promise((resolve, reject) => {
            this.userClient.AssignStoreToUser({
                userId, storeCode
            },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("User search failed!"));
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response); // Asegúrate de que este sea el campo correcto
                    }
                })
        })
    }

    async searchUserByStore(storeCode: string): Promise<any> {
        return new Promise((resolve, reject) => {
            this.userClient.searchUserByStore({
                storeCode
            },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("User search failed!"));
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response); // Asegúrate de que este sea el campo correcto
                    }
                }); // Cierra el paréntesis de la llamada a la función
        }); // Cierra el paréntesis de la promesa
    }

    async listUsers(): Promise<any> {
        return new Promise((resolve, reject) => {
            this.userClient.listUsers(
                {}, // Enviar un request vacío, ya que no hay parámetros necesarios
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("User listing failed!"));
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response); // Asegúrate de que este sea el campo correcto
                    }
                }
            );
        });
    }
    


//-----------------------------------------------STORE-------------------------------------------
    async createStore(code: string, address: string, city: string, state: string, enabled: boolean): Promise<any> {
        // Validar código de la tienda
        if (!/^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{3,50}$/.test(code)) {
            throw new Error("Store code must contain both letters and numbers, and be between 3 and 50 characters long.");
        }

        return new Promise((resolve, reject) => {
            this.storeClient.CreateStore(
                {
                    code,
                    address,
                    city,
                    state,
                    enabled
                },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("Store creation failed!"));
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response); // Extraer el `store` de la respuesta
                    }
                }
            );
        });
    }


    async disableStore(code: string, enabled: boolean): Promise<any> {
        return new Promise((resolve, reject) => {
            this.storeClient.DisableStore({
                code,
                enabled
            }, (error: grpc.ServiceError | null, response: any) => {
                if (error) {
                    console.error("Error in gRPC call:", error);
                    reject(new Error("Store disabling failed!"));
                } else {
                    console.log("Received gRPC response:", response);
                    resolve(response);
                }
            });
        });
    }

    async searchStore(code: string, enabled: boolean): Promise<any> {
        return new Promise((resolve, reject) => {
            console.log("Request to gRPC:", { code, enabled }); // Log de solicitud
            this.storeClient.SearchStore(
                { code, enabled },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error(`Product search failed: ${error.message}`)); // Mensaje de error mejorado
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response.stores); // Cambiado a `stores`
                    }
                }
            );
        });
    }



//-----------------------------------------------PRODUCT-------------------------------------------

    async createProduct(name: string, size: string, imageUrl: string, color: string, enabled: boolean): Promise<any> {
        return new Promise((resolve, reject) => {
            this.productClient.CreateProduct(
                {
                    name,
                    size,
                    imageUrl,
                    color,
                    enabled
                },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("Product creation failed!"));
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response); // Extraer el `product` de la respuesta
                    }
                }
            );
        });
    }

    async disableProduct(uniqueCode: string, enabled: boolean): Promise<any> {
        return new Promise((resolve, reject) => {
            this.productClient.DisableProduct({
                uniqueCode,
                enabled
            }, (error: grpc.ServiceError | null, response: any) => {
                if (error) {
                    console.error("Error in gRPC call:", error);
                    reject(new Error("Product disabling failed!"));
                } else {
                    console.log("Received gRPC response:", response);
                    resolve(response);
                }
            });
        });
    }

    async updateProduct(name: string, uniqueCode: string, size: string, imageUrl: string, color: string, enabled: boolean): Promise<any> {
        return new Promise((resolve, reject) => {
            this.productClient.UpdateProduct(
                {
                    name,
                    uniqueCode,
                    size,
                    imageUrl,
                    color,
                    enabled
                },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error, 'El response:', response);
                        reject(new Error("Product update failed!"));
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response);
                    }
                }
            );
        });
    }


    async searchProduct(name?: string, uniqueCode?: string, size?: string, color?: string, enabled?: boolean): Promise<any> {
        return new Promise((resolve, reject) => {
            this.productClient.SearchProduct(
                { uniqueCode, name, size, color, enabled }, // Añadimos enabled al objeto
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("Product search failed!"));
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response.products); // Devolver la lista de productos
                    }
                }
            );
        });
    }

//-----------------------------PRODUCT_STORE--------------------------------------------------
    async createProductStore(storeCode?: string, productCode?: string, stock?: number, enabled?: boolean): Promise<any> {
        console.log("client.ts ---> ", storeCode, productCode, stock, enabled)
        return new Promise((resolve, reject) => {
            this.productStoreClient.CreateProductStore({
                storeCode,
                productCode,
                stock,
                enabled
            },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("ProductStore creation failed!"));
                    } else {
                        resolve(response.message);
                    }
                })
        })
    }
//-----------------------------ORDER--------------------------------------------
        async createOrder(
            storeId: number,
            observations: string,
            dispatchOrder: string
        ): Promise<any> {
            console.log("client.ts ---> ", storeId, observations, dispatchOrder);
        
            return new Promise((resolve, reject) => {
                const orderRequest = {
                    storeId,
                    observations,
                    dispatchOrder,
                    requestDate: new Date().toISOString(), // Genera la fecha actual en formato ISO
                };
        
                this.orderClient.CreateOrder(orderRequest, (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("Order creation failed!"));
                    } else {
                        console.log("Received gRPC response:", response);
                        resolve(response); // Assuming the response contains relevant order information
                    }
                });
            });
        }
        
}
       
export default Client;
