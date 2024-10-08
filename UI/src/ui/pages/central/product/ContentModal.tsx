import { styled } from "styled-components";
import React from "react";
import { Product } from "../../../../core/domain/entities";

interface ContentModalProps {
  newProduct: Product;
  setNewProduct: React.Dispatch<React.SetStateAction<Product>>;
}

const ContentModal: React.FC<ContentModalProps> = ({
  newProduct,
  setNewProduct,
}) => {
  return (
    <InputContainer>
      <label>Product Name:</label>
      <input
        type="text"
        value={newProduct.name}
        onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
      />
      <label>Unique Code:</label>
      <input
        type="text"
        value={newProduct.uniqueCode}
        onChange={(e) =>
          setNewProduct({ ...newProduct, uniqueCode: e.target.value })
        }
      />
      <label>Size:</label>
      <input
        type="text"
        value={newProduct.size}
        onChange={(e) => setNewProduct({ ...newProduct, size: e.target.value })}
      />
      <label>Image URL:</label>
      <input
        type="text"
        value={newProduct.imageUrl}
        onChange={(e) =>
          setNewProduct({ ...newProduct, imageUrl: e.target.value })
        }
      />
      <label>Color:</label>
      <input
        type="text"
        value={newProduct.color}
        onChange={(e) =>
          setNewProduct({ ...newProduct, color: e.target.value })
        }
      />
      <label>Enabled:</label>
      <input
        type="checkbox"
        checked={newProduct.enabled}
        onChange={(e) =>
          setNewProduct({ ...newProduct, enabled: e.target.checked })
        }
      />
    </InputContainer>
  );
};

const InputContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;

  label {
    font-weight: bold;
  }

  input[type="text"] {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  input[type="checkbox"] {
    margin-top: 5px;
  }
`;

export default ContentModal;
