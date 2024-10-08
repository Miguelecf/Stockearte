import { styled } from "styled-components";
import React from "react";
import { User } from "../../../../core/domain/entities";

interface ContentModalProps {
  newUser: User;
  setNewUser: React.Dispatch<React.SetStateAction<User>>;
}

const ContentModal: React.FC<ContentModalProps> = ({ newUser, setNewUser }) => {
  return (
    <InputContainer>
      <label>Username:</label>
      <input
        type="text"
        value={newUser.username}
        onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
      />
      <label>Password:</label>
      <input
        type="password"
        value={newUser.password}
        onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
      />
      <label>First Name:</label>
      <input
        type="text"
        value={newUser.firstName}
        onChange={(e) => setNewUser({ ...newUser, firstName: e.target.value })}
      />
      <label>Last Name:</label>
      <input
        type="text"
        value={newUser.lastName}
        onChange={(e) => setNewUser({ ...newUser, lastName: e.target.value })}
      />
      <label>Enabled:</label>
      <input
        type="checkbox"
        checked={newUser.enabled}
        onChange={(e) => setNewUser({ ...newUser, enabled: e.target.checked })}
      />
      <label>Is Central:</label>
      <input
        type="checkbox"
        checked={newUser.isCentral}
        onChange={(e) =>
          setNewUser({ ...newUser, isCentral: e.target.checked })
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

  input[type="text"],
  input[type="password"] {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  input[type="checkbox"] {
    margin-top: 5px;
  }
`;

export default ContentModal;
