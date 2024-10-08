import React, { useState } from "react";
import DataList from "../../../common/components/DataList/DataList";
import Modal from "../../../common/components/Modal";
import ContentModal from "./ContentModal";
import useStores from "./useStores";

const StoreDashboard: React.FC = () => {
  const { stores, addStore, switchStateStore, loading, error } = useStores();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newStore, setNewStore] = useState({
    code: "",
    address: "",
    city: "",
    state: "",
    enabled: false,
  });

  const handleAddStore = () => {
    addStore(newStore);
    setIsModalOpen(false);
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Stores Dashboard</h1>
      <DataList
        data={stores}
        columns={["code", "address", "city", "state", "enabled"]}
        type="table"
        onAdd={() => setIsModalOpen(true)}
        onSwitchState={switchStateStore}
        onFilter={(filter) => console.log("Filtrando por:", filter)}
      />

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleAddStore}
        title="Add New Store"
      >
        <ContentModal newStore={newStore} setNewStore={setNewStore} />
      </Modal>
    </div>
  );
};

export default StoreDashboard;
