import { useState, useEffect } from "react";
import { Store } from "../../../../core/domain/entities";
import StoreService from "../../../../core/StoreService";

const useStores = () => {
  const [stores, setStores] = useState<Store[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const getStoreListEnabled = async () => {
    try {
      const { stores: storesEnabled } = await StoreService.listAllEnabled();
      return storesEnabled;
    } catch (error) {
      console.error("Error loading enabled stores", error);
      return [];
    }
  };

  const getStoreListDisabled = async () => {
    try {
      const { stores: storesDisabled } = await StoreService.listAllDisabled();
      return storesDisabled.map((store: Store) => ({
        ...store,
        enabled: false,
      }));
    } catch (error) {
      console.error("Error loading disabled stores", error);
      return [];
    }
  };

  const loadStores = async () => {
    setLoading(true);
    setError(null);

    const [storeEnabled, storeDisabled] = await Promise.all([
      getStoreListEnabled(),
      getStoreListDisabled(),
    ]);

    const combinedStores = [...storeEnabled, ...storeDisabled] as Store[];
    setStores(combinedStores);

    setLoading(false);
  };

  const addStore = async (newStore: Store) => {
    try {
      await StoreService.create(newStore);
      setStores([...stores, newStore]);
    } catch (error) {
      setError("Error creating store");
      console.error(error);
    }
  };

  const switchStateStore = async (store: Store) => {
    try {
      await StoreService.disableStore(store.code, !store.enabled);
      setStores(
        stores.map((s) =>
          s.code === store.code ? { ...s, enabled: !s.enabled } : s
        )
      );
    } catch (error) {
      setError("Error switching store state");
      console.error(error);
    }
  };

  useEffect(() => {
    loadStores();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { stores, addStore, switchStateStore, loading, error };
};

export default useStores;
