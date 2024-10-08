import { useState, useEffect } from "react";
import { Product } from "../../../../core/domain/entities";
import ProductService from "../../../../core/ProductService";

const useProducts = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const getProductListEnabled = async () => {
    try {
      const { products: productsEnabled } =
        await ProductService.listAllEnabled();
      return productsEnabled;
    } catch (error) {
      console.error("Error loading enabled products", error);
      return [];
    }
  };

  const getProductListDisabled = async () => {
    try {
      const { products: productsDisabled } =
        await ProductService.listAllDisabled();
      return productsDisabled.map((product: Product) => ({
        ...product,
        enabled: false,
      }));
    } catch (error) {
      console.error("Error loading disabled products", error);
      return [];
    }
  };

  const loadProducts = async () => {
    setLoading(true);
    setError(null);

    const [productsEnabled, productsDisabled] = await Promise.all([
      getProductListEnabled(),
      getProductListDisabled(),
    ]);

    const combinedProducts = [
      ...productsEnabled,
      ...productsDisabled,
    ] as Product[];
    setProducts(combinedProducts);
    setLoading(false);
  };

  const addProduct = async (newProduct: Product) => {
    try {
      const product = await ProductService.create(newProduct);
      console.log(product);
      setProducts([...products, product]);
    } catch (error) {
      setError("Error creating product");
      console.error(error);
    }
  };

  const switchStateProduct = async (product: Product) => {
    try {
      await ProductService.disableProduct(product.uniqueCode, !product.enabled);
      setProducts(
        products.map((p) =>
          p.uniqueCode === product.uniqueCode
            ? { ...p, enabled: !p.enabled }
            : p
        )
      );
    } catch (error) {
      setError("Error switching product state");
      console.error(error);
    }
  };

  useEffect(() => {
    loadProducts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { products, addProduct, switchStateProduct, loading, error };
};

export default useProducts;
