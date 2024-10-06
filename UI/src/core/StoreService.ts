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
}

export default StoreService;
