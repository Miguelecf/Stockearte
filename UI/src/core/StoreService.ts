import { axiosInstance } from "../utils/axios";
import { Store } from "./domain/entities";

class StoreService {
  public static async create(store: Store) {
    return axiosInstance
      .post(`/create-store`, {
        code: store.code,
        address: store.address,
        city: store.city,
        state: store.state,
        enabled: true,
      })
      .then((response) => {
        return response.data;
      });
  }

  public static async listAllEnabled() {
    return axiosInstance
      .get(`/search-store?enabled=true`, {})
      .then((response) => {
        return response.data;
      });
  }

  public static async listAllDisabled() {
    return axiosInstance
      .get(`/search-store?enabled=false`, {})
      .then((response) => {
        return response.data;
      });
  }

  public static async disableStore(code: string, newState: boolean) {
    return axiosInstance
      .post(`/disable-store`, {
        enabled: newState,
        code,
      })
      .then((response) => {
        return response.data;
      });
  }
}

export default StoreService;
