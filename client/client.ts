import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import { rejects } from "assert";
import * as path from "path";

// Update the path to reflect the correct location
const protoRoute = "../proto/user.proto"; // Adjust the path based on the actual file location

const PROTO_PATH = path.resolve(__dirname, protoRoute);
const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const proto = grpc.loadPackageDefinition(packageDefinition) as any;

class Client {
    private client: any;

    constructor(host: string) {
        this.client = new proto.user.UserService(host, grpc.credentials.createInsecure());
    }

    async createUser(username: string, password: string, firstName: string, lastName: string, enabled: boolean, storeId?: number): Promise<string> {
        return new Promise((resolve, reject) => {
            this.client.CreateUser(
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
            this.client.Login(
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
            this.client.GetUserByUsername(
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
}

export default Client;
