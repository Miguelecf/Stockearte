import useDataList from "./hooks/useDataList";
import { Input, Button } from "./DataListStyles";
import DataListTable from "./DataListTable";
import DataListCards from "./DataListCards";

interface DataListProps<T> {
  data: T[];
  columns: (keyof T)[];
  type?: "table" | "card";
  onAdd: () => void;
  onDelete: (item: T) => void;
  onFilter?: (filter: string) => void;
}

const DataList = <T,>({
  data,
  columns,
  type = "table",
  onAdd,
  onDelete,
  onFilter,
}: DataListProps<T>) => {
  const { filter, handleFilterChange, filteredData } = useDataList<T>({
    data,
    onFilter,
  });

  return (
    <div>
      <Input
        type="text"
        placeholder="Filter..."
        value={filter}
        onChange={handleFilterChange}
      />
      {type === "table" ? (
        <DataListTable
          columns={columns}
          filteredData={filteredData}
          onDelete={onDelete}
        />
      ) : (
        <DataListCards
          columns={columns}
          filteredData={filteredData}
          onDelete={onDelete}
        />
      )}
      <Button onClick={onAdd}>Add New</Button>
    </div>
  );
};

export default DataList;
