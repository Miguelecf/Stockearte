import {
  TableContainer,
  Table,
  TableHeader,
  TableRow,
  TableCell,
  Button,
} from "./DataListStyles";

interface DataListTableProps<T> {
  columns: (keyof T)[];
  filteredData: T[];
  onDelete: (item: T) => void;
}

const DataListTable = <T,>({
  columns,
  filteredData,
  onDelete,
}: DataListTableProps<T>) => (
  <TableContainer>
    <Table>
      <thead>
        <tr>
          {columns.map((column) => (
            <TableHeader key={String(column)}>{String(column)}</TableHeader>
          ))}
          <TableHeader>Actions</TableHeader>
        </tr>
      </thead>
      <tbody>
        {filteredData.map((item, index) => (
          <TableRow key={index}>
            {columns.map((column) => (
              <TableCell key={String(column)}>{String(item[column])}</TableCell>
            ))}
            <TableCell>
              <Button onClick={() => onDelete(item)}>Delete</Button>
            </TableCell>
          </TableRow>
        ))}
      </tbody>
    </Table>
  </TableContainer>
);

export default DataListTable;
