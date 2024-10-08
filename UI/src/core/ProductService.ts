import { axiosInstance } from "../utils/axios";
import { Product } from "./domain/entities";

class ProductService {
  public static async create(product: Product) {
    return axiosInstance
      .post(`/create-product`, {
        name: product.name,
        uniqueCode: product.uniqueCode,
        size: product.size,
        imageUrl: product.imageUrl,
        color: product.color,
        enabled: product.enabled,
      })
      .then((response) => {
        return response.data;
      });
  }

  public static async listAllEnabled() {
    return axiosInstance
      .get(`/search-product?enabled=true`, {})
      .then((response) => {
        return response.data;
      });
  }

  public static async listAllDisabled() {
    return axiosInstance
      .get(`/search-product?enabled=false`, {})
      .then((response) => {
        return response.data;
      });
  }

  public static async disableProduct(uniqueCode: string, newState: boolean) {
    return axiosInstance
      .post(`/disable-product`, {
        enabled: newState,
        uniqueCode,
      })
      .then((response) => {
        return response.data;
      });
  }
}

export default ProductService;
