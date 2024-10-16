import { useState, useEffect } from "react";
import { User } from "../../../../core/domain/entities";
import UserService from "../../../../core/UserService";

const useUsers = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const getUserListEnabled = async () => {
    try {
      const { users: usersEnabled } = await UserService.listAllEnabled();
      return usersEnabled.users;
    } catch (error) {
      console.error("Error loading enabled users", error);
      return [];
    }
  };

  const loadUsers = async () => {
    setLoading(true);
    setError(null);

    const users = await getUserListEnabled();

    setUsers(users);
    setLoading(false);
  };

  const addUser = async (newUser: User) => {
    try {
      await UserService.create(newUser);
      setUsers([...users, newUser]);
    } catch (error) {
      setError("Error creating user");
      console.error(error);
    }
  };

  const switchStateUser = async (user: User) => {
    try {
      await UserService.disableUser(user.username, !user.enabled);
      setUsers(
        users.map((u) =>
          u.username === user.username ? { ...u, enabled: !u.enabled } : u
        )
      );
    } catch (error) {
      setError("Error switching user state");
      console.error(error);
    }
  };

  useEffect(() => {
    loadUsers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { users, addUser, switchStateUser, loading, error };
};

export default useUsers;
