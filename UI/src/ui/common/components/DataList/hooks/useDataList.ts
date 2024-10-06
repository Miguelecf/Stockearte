import { useState } from "react";

interface UseDataListProps<T> {
  data: T[];
  onFilter?: (filter: string) => void;
}

const useDataList = <T>({ data, onFilter }: UseDataListProps<T>) => {
  const [filter, setFilter] = useState<string>("");

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setFilter(value);
    if (onFilter) {
      onFilter(value);
    }
  };

  const filteredData = data.filter((item) =>
    Object.values(item).some((value) =>
      value.toString().toLowerCase().includes(filter.toLowerCase())
    )
  );

  return { filter, handleFilterChange, filteredData };
};

export default useDataList;
