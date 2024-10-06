import styled from "styled-components";

export const TableContainer = styled.div`
  overflow-x: auto;
  padding: 20px;
`;

export const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden; /* For rounded corners */
`;

export const TableHeader = styled.th`
  padding: 12px;
  background-color: #f9f9f9;
  text-align: left;
  font-weight: bold;
  font-size: 1.1rem;
`;

export const TableRow = styled.tr`
  &:nth-child(even) {
    background-color: #f2f2f2;
  }
`;

export const TableCell = styled.td`
  padding: 12px;
  border-bottom: 1px solid #ddd;
`;

export const CardContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px;
`;

export const Card = styled.div`
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-5px);
  }
`;

export const Button = styled.button`
  margin: 5px;
  padding: 10px 15px;
  background-color: #007aff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s, transform 0.2s;

  &:hover {
    background-color: #005bb5;
    transform: scale(1.05);
  }
`;

export const Input = styled.input`
  margin-bottom: 20px;
  padding: 10px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;

  &:focus {
    border-color: #007aff;
    outline: none;
    box-shadow: 0 0 5px rgba(0, 122, 255, 0.5);
  }
`;
