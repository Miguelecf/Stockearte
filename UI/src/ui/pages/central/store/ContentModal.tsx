import { styled } from "styled-components";
import React from "react";
import { Store } from "../../../../core/domain/entities"; // Asegúrate de que esta ruta es correcta.

interface ContentModalProps {
  newStore: Store;
  setNewStore: React.Dispatch<React.SetStateAction<Store>>;
}

const ContentModal: React.FC<ContentModalProps> = ({
  newStore,
  setNewStore,
}) => {
  return (
    <InputContainer>
      <label>Code:</label>
      <input
        type="text"
        value={newStore.code}
        onChange={(e) => setNewStore({ ...newStore, code: e.target.value })}
      />
      <label>Address:</label>
      <input
        type="text"
        value={newStore.address}
        onChange={(e) => setNewStore({ ...newStore, address: e.target.value })}
      />
      <label>City:</label>
      <input
        type="text"
        value={newStore.city}
        onChange={(e) => setNewStore({ ...newStore, city: e.target.value })}
      />
      <label>State:</label>
      <input
        type="text"
        value={newStore.state}
        onChange={(e) => setNewStore({ ...newStore, state: e.target.value })}
      />
      <label>Enabled:</label>
      <input
        type="checkbox"
        checked={newStore.enabled}
        onChange={(e) =>
          setNewStore({ ...newStore, enabled: e.target.checked })
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
