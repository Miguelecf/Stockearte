import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import { rejects } from "assert";
import * as path from "path";

// Paths to both .proto files
const userProtoPath = path.resolve(__dirname, "../proto/user.proto");
const storeProtoPath = path.resolve(__dirname, "../proto/store.proto");

// Load .proto files
const userPackageDefinition = protoLoader.loadSync(userProtoPath);
const storePackageDefinition = protoLoader.loadSync(storeProtoPath);

// Combine package definitions
const userProto = grpc.loadPackageDefinition(userPackageDefinition) as any;
const storeProto = grpc.loadPackageDefinition(storePackageDefinition) as any;

class Client {
    private userClient: any;
    private storeClient: any;

    constructor(host: string) {
        this.userClient = new userProto.user.UserService(host, grpc.credentials.createInsecure());
        this.storeClient = new storeProto.store.StoreService(host, grpc.credentials.createInsecure());
    }

    async createUser(username: string, password: string, firstName: string, lastName: string, enabled: boolean, storeId?: number): Promise<string> {
        return new Promise((resolve, reject) => {
            this.userClient.CreateUser(
                {
                    username,
                    password,
                    firstName,
                    lastName,
                    enabled,
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

    async loginUser(username: string, password: string): Promise<string> {
        return new Promise((resolve, reject) => { // Use curly braces, not parentheses
            this.userClient.Login(
                { username, password },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        reject(new Error("Login failed!"));
                    } else {
                        resolve(`User ${response.username} logged in successfully!`);
                    }
                }
            );
        });
    }



    async getUserByUsername(username: string): Promise<string | null> {
        return new Promise((resolve, reject) => {
            this.userClient.GetUserByUsername(
                { username },
                (error: grpc.ServiceError | null, response: any) => {
                    if (error) {
                        console.error("Error in gRPC call:", error);
                        if (error.code === grpc.status.NOT_FOUND) {
                            resolve(null);
                        } else {
                            reject(new Error("An error occurred"));
                        }
                    } else {
                        resolve(response.message);
                    }
                }
            );
        });
    }

    async createStore(code: string, address: string, city: string, state: string, enabled: boolean): Promise<any> {
        // Validar código de la tienda
        if (!/^[a-zA-Z0-9]{3,50}$/.test(code)) {
            throw new Error("Store code must be alphanumeric and between 3 and 50 characters long.");
        }
    
        return new Promise((resolve, reject) => {
            this.storeClient.CreateStore(
                { code, address, city, state, enabled },
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

}

export default Client;
