import React from "react";
import styled from "styled-components";

const Dashboard: React.FC = () => {
  return (
    <Container>
      <h1>Dashboard</h1>
      <p>Welcome to the dashboard!</p>
    </Container>
  );
};

export default Dashboard;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #e0f7fa;
  h1 {
    font-size: 3rem;
    color: #00796b;
  }
  p {
    font-size: 1.5rem;
    color: #004d40;
  }
`;
