import { CardContainer, Card, Button } from "./DataListStyles";

interface DataListCardsProps<T> {
  columns: (keyof T)[];
  filteredData: T[];
  onDelete: (item: T) => void;
}

const DataListCards = <T,>({
  columns,
  filteredData,
  onDelete,
}: DataListCardsProps<T>) => (
  <CardContainer>
    {filteredData.map((item, index) => (
      <Card key={index}>
        {columns.map((column) => (
          <div key={String(column)}>
            <strong>{String(column)}: </strong>
            {String(item[column])}
          </div>
        ))}
        <Button onClick={() => onDelete(item)}>Delete</Button>
      </Card>
    ))}
  </CardContainer>
);

export default DataListCards;
