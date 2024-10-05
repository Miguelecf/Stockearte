import { axiosInstance } from "../utils/axios";

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
}

export default UserService;
