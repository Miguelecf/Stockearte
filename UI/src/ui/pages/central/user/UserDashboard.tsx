import React, { useState } from "react";
import DataList from "../../../common/components/DataList/DataList";
import Modal from "../../../common/components/Modal";
import ContentModal from "./ContentModal";
import { User } from "../../../../core/domain/entities";
import useUsers from "./useUsers";
import DashboardNav from "../../../common/components/DashboardNav";

const UserDashboard: React.FC = () => {
  const { users, addUser, switchStateUser, loading, error } = useUsers();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newUser, setNewUser] = useState<User>({
    username: "",
    password: "",
    firstName: "",
    lastName: "",
    enabled: false,
    isCentral: false,
  });

  const handleAddUser = () => {
    addUser(newUser);
    setIsModalOpen(false);
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Users Dashboard</h1>
      <DashboardNav />
      <DataList
        data={users}
        columns={["username", "firstName", "lastName", "enabled", "isCentral"]}
        type="table"
        onAdd={() => setIsModalOpen(true)}
        onSwitchState={undefined}
        onFilter={(filter) => console.log("Filtering by:", filter)}
      />

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleAddUser}
        title="Add New User"
      >
        <ContentModal newUser={newUser} setNewUser={setNewUser} />
      </Modal>
    </div>
  );
};

export default UserDashboard;
