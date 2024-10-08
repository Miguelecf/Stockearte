import { axiosInstance } from "../utils/axios";
import { User } from "./domain/entities";

class UserService {
  public static async loginRequest(username: string, password: string) {
    return axiosInstance
      .post(`/login`, {
        username: username,
        password: password,
      })
      .then((response) => {
        localStorage.setItem("username", username);
        return response.data;
      });
  }

  public static async create({
    username,
    password,
    firstName,
    lastName,
    enabled,
    isCentral,
  }: User) {
    return axiosInstance
      .post(`/create-user`, {
        username,
        password,
        firstName,
        lastName,
        enabled,
        isCentral,
      })
      .then((response) => {
        return response.data;
      });
  }

  public static async listAllEnabled() {
    return axiosInstance
      .get(`/search-user?enabled=true`, {})
      .then((response) => {
        return response.data;
      });
  }

  public static async listAllDisabled() {
    return axiosInstance
      .get(`/search-user?enabled=false`, {})
      .then((response) => {
        return response.data;
      });
  }

  public static async disableProduct(uniqueCode: string, newState: boolean) {
    return axiosInstance
      .post(`/disable-user`, {
        enabled: newState,
        uniqueCode,
      })
      .then((response) => {
        return response.data;
      });
  }
}

export default UserService;
