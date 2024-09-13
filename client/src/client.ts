import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import * as path from "path";

const protoRoute = "../../protos/user.proto";

const PROTO_PATH = path.resolve(__dirname, protoRoute);
const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const proto = grpc.loadPackageDefinition(packageDefinition) as any;

const client = new proto.user.UserService(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

const login = async (username: string, password: string): Promise<string> => {
  return new Promise((resolve, reject) => {
    client.Login(
      { username, password },
      (error: grpc.ServiceError | null, response: any) => {
        if (error) {
          console.error("Error en la llamada gRPC:", error);
          if (error.code === grpc.status.UNAUTHENTICATED) {
            reject(new Error("Login failed!"));
          } else {
            reject(new Error("An error occurred"));
          }
        } else {
          resolve(response.message);
        }
      }
    );
  });
};

const createUser = async (
  username: string,
  password: string
): Promise<string> => {
  return new Promise((resolve, reject) => {
    client.CreateUser(
      { username, password },
      (error: grpc.ServiceError | null, response: any) => {
        if (error) {
          console.error("Error en la llamada gRPC:", error);
          reject(new Error("User creation failed!"));
        } else {
          resolve(response.message);
        }
      }
    );
  });
};

export default {
  login,
  createUser,
};
