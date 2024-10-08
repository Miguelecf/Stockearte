import { CardContainer, Card, Button } from "./DataListStyles";

interface DataListCardsProps<T> {
  columns: (keyof T)[];
  filteredData: T[];
  onSwitchState: (item: T) => void;
}

const DataListCards = <T,>({
  columns,
  filteredData,
  onSwitchState,
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
        <Button onClick={() => onSwitchState(item)}>Switch State</Button>
      </Card>
    ))}
  </CardContainer>
);

export default DataListCards;
