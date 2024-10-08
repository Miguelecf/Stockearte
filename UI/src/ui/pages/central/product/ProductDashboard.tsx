import React, { useState } from "react";
import DataList from "../../../common/components/DataList/DataList";
import Modal from "../../../common/components/Modal";
import ContentModal from "./ContentModal";
import { Product } from "../../../../core/domain/entities";
import useProducts from "./useProducts";

const ProductDashboard: React.FC = () => {
  const { products, addProduct, switchStateProduct, loading, error } =
    useProducts();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newProduct, setNewProduct] = useState<Product>({
    name: "",
    uniqueCode: "",
    size: "",
    imageUrl: "",
    color: "",
    enabled: false,
  });

  const handleAddProduct = () => {
    addProduct(newProduct);
    setIsModalOpen(false);
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Products Dashboard</h1>
      <DataList
        data={products}
        columns={["name", "uniqueCode", "size", "color", "enabled"]}
        type="card"
        onAdd={() => setIsModalOpen(true)}
        onSwitchState={switchStateProduct}
        onFilter={(filter) => console.log("Filtering by:", filter)}
      />

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleAddProduct}
        title="Add New Product"
      >
        <ContentModal newProduct={newProduct} setNewProduct={setNewProduct} />
      </Modal>
    </div>
  );
};

export default ProductDashboard;
