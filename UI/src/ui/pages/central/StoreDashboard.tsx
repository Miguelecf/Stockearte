// src/pages/StoreDashboard.tsx

import React, { useState } from "react";
import DataList from "../../common/components/DataList/DataList";
import { Store } from "../../../core/domain/entities";

const StoreDashboard: React.FC = () => {
  const [stores, setStores] = useState<Store[]>([
    {
      code: "001",
      address: "123 Main St",
      city: "Springfield",
      state: "IL",
      enabled: true,
    },
    {
      code: "002",
      address: "456 Elm St",
      city: "Shelbyville",
      state: "IN",
      enabled: false,
    },
  ]);

  const addStore = () => {
    const newStore: Store = {
      code: "003",
      address: "789 Oak St",
      city: "Capital City",
      state: "CA",
      enabled: true,
    };
    setStores([...stores, newStore]);
  };

  const deleteStore = (store: Store) => {
    setStores(stores.filter((s) => s.code !== store.code));
  };

  const handleFilter = (filter: string) => {
    console.log("Filtrando por:", filter);
  };

  return (
    <div>
      <h1>Stores Dashboard</h1>
      <DataList<Store>
        data={stores}
        columns={["code", "address", "city", "state", "enabled"]}
        type="table"
        onAdd={addStore}
        onDelete={deleteStore}
        onFilter={handleFilter}
      />
    </div>
  );
};

export default StoreDashboard;
